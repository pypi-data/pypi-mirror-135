"""
:class:`ASE_OTF` is the on-the-fly training module for ASE, WITHOUT molecular dynamics engine. 
It needs to be used adjointly with ASE MD engine. 
"""
import os
import json
import sys
import inspect
import pickle
from time import time
from copy import deepcopy
import logging

import numpy as np
from flare.ase.npt import NPT_mod
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.nptberendsen import NPTBerendsen
from ase.md.verlet import VelocityVerlet
from ase.md.langevin import Langevin
from flare.ase.nosehoover import NoseHoover
from ase import units
from ase.io import read, write

import flare
from flare.otf import OTF
from flare.ase.atoms import FLARE_Atoms
from flare.ase.calculator import FLARE_Calculator
import flare.ase.dft as dft_source


class ASE_OTF(OTF):

    """
    On-the-fly training module using ASE MD engine, a subclass of OTF.

    Args:
        atoms (ASE Atoms): the ASE Atoms object for the on-the-fly MD run.
        calculator: ASE calculator. Must have "get_uncertainties" method
          implemented.
        timestep: the timestep in MD. Please use ASE units, e.g. if the
            timestep is 1 fs, then set `timestep = 1 * units.fs`
        number_of_steps (int): the total number of steps for MD.
        dft_calc (ASE Calculator): any ASE calculator is supported,
            e.g. Espresso, VASP etc.
        md_engine (str): the name of MD thermostat, only `VelocityVerlet`,
            `NVTBerendsen`, `NPTBerendsen`, `NPT` and `Langevin`, `NoseHoover`
            are supported.
        md_kwargs (dict): Specify the args for MD as a dictionary, the args are
            as required by the ASE MD modules consistent with the `md_engine`.
        trajectory (ASE Trajectory): default `None`, not recommended,
            currently in experiment.

    The following arguments are for on-the-fly training, the user can also
    refer to :class:`flare.otf.OTF`

    Args:
        prev_pos_init ([type], optional): Previous positions. Defaults
            to None.
        rescale_steps (List[int], optional): List of frames for which the
            velocities of the atoms are rescaled. Defaults to [].
        rescale_temps (List[int], optional): List of rescaled temperatures.
            Defaults to [].

        calculate_energy (bool, optional): If True, the energy of each
            frame is calculated with the GP. Defaults to False.
        write_model (int, optional): If 0, write never. If 1, write at
            end of run. If 2, write after each training and end of run.
            If 3, write after each time atoms are added and end of run.
            If 4, write after each training and end of run, and back up
            after each write.
        std_tolerance_factor (float, optional): Threshold that determines
            when DFT is called. Specifies a multiple of the current noise
            hyperparameter. If the epistemic uncertainty on a force
            component exceeds this value, DFT is called. Defaults to 1.
        skip (int, optional): Number of frames that are skipped when
            dumping to the output file. Defaults to 0.
        init_atoms (List[int], optional): List of atoms from the input
            structure whose local environments and force components are
            used to train the initial GP model. If None is specified, all
            atoms are used to train the initial GP. Defaults to None.
        output_name (str, optional): Name of the output file. Defaults to
            'otf_run'.
        max_atoms_added (int, optional): Number of atoms added each time
            DFT is called. Defaults to 1.
        freeze_hyps (int, optional): Specifies the number of times the
            hyperparameters of the GP are optimized. After this many
            updates to the GP, the hyperparameters are frozen.
            Defaults to 10.

        n_cpus (int, optional): Number of cpus used during training.
            Defaults to 1.
    """

    def __init__(
        self,
        atoms,
        timestep,
        number_of_steps,
        dft_calc,
        md_engine,
        md_kwargs,
        calculator=None,
        trajectory=None,
        **otf_kwargs,
    ):

        self.structure = FLARE_Atoms.from_ase_atoms(atoms)
        if calculator is not None:
            self.structure.calc = calculator
        self.timestep = timestep
        self.md_engine = md_engine
        self.md_kwargs = md_kwargs
        self._kernels = None

        if md_engine == "VelocityVerlet":
            MD = VelocityVerlet
        elif md_engine == "NVTBerendsen":
            MD = NVTBerendsen
        elif md_engine == "NPTBerendsen":
            MD = NPTBerendsen
        elif md_engine == "NPT":
            MD = NPT_mod
        elif md_engine == "Langevin":
            MD = Langevin
        elif md_engine == "NoseHoover":
            MD = NoseHoover
        else:
            raise NotImplementedError(md_engine + " is not implemented in ASE")

        self.md = MD(
            atoms=self.structure,
            timestep=timestep,
            trajectory=trajectory,
            **md_kwargs,
        )

        force_source = dft_source
        self.flare_calc = self.structure.calc

        # Convert ASE timestep to ps for the output file.
        flare_dt = timestep / (units.fs * 1e3)

        super().__init__(
            dt=flare_dt,
            number_of_steps=number_of_steps,
            gp=self.flare_calc.gp_model,
            force_source=force_source,
            dft_loc=dft_calc,
            dft_input=self.structure,
            **otf_kwargs,
        )

        self.flare_name = self.output_name + "_flare.json"
        self.dft_name = self.output_name + "_dft.pickle"
        self.structure_name = self.output_name + "_atoms.json"
        self.checkpt_files = [
            self.checkpt_name,
            self.flare_name,
            self.dft_name,
            self.structure_name,
            self.dft_xyz,
        ]

    def get_structure_from_input(self, prev_pos_init):
        if prev_pos_init is None:
            self.structure.prev_positions = np.copy(self.structure.positions)
        else:
            assert len(self.structure.positions) == len(
                self.structure.prev_positions
            ), "Previous positions and positions are not same length"
            self.structure.prev_positions = prev_pos_init

    def initialize_train(self):
        super().initialize_train()

        # TODO: Turn this into a "reset" method.
        if not isinstance(self.structure.calc, FLARE_Calculator):
            self.flare_calc.reset()
            self.structure.calc = self.flare_calc

        if self.md_engine == "NPT":
            if not self.md.initialized:
                self.md.initialize()
            else:
                if self.md.have_the_atoms_been_changed():
                    raise NotImplementedError(
                        "You have modified the atoms since the last timestep."
                    )

    def compute_properties(self):
        """
        Compute energies, forces, stresses, and their uncertainties with
            the FLARE ASE calcuator, and write the results to the
            OTF structure object.
        """

        # Change to FLARE calculator if necessary.
        if not isinstance(self.structure.calc, FLARE_Calculator):
            self.flare_calc.reset()
            self.structure.calc = self.flare_calc

        if not self.flare_calc.results:
            self.structure.calc.calculate(self.structure)

    def md_step(self):
        """
        Get new position in molecular dynamics based on the forces predicted by
        FLARE_Calculator or DFT calculator
        """
        # Update previous positions.
        self.structure.prev_positions = np.copy(self.structure.positions)

        # Reset FLARE calculator.
        if self.dft_step:
            self.flare_calc.reset()
            self.structure.calc = self.flare_calc

        # Take MD step.
        # Inside the step() function, get_forces() is called
        self.md.step()
        self.curr_step += 1

    def write_gp(self):
        self.flare_calc.write_model(self.flare_name)

    def rescale_temperature(self, new_pos):
        # call OTF method
        super().rescale_temperature(new_pos)

        # update ASE atoms
        if self.curr_step in self.rescale_steps:
            rescale_ind = self.rescale_steps.index(self.curr_step)
            new_temp = self.rescale_temps[rescale_ind]
            temp_fac = new_temp / self.temperature
            vel_fac = np.sqrt(temp_fac)
            curr_velocities = self.structure.get_velocities()
            self.structure.set_velocities(curr_velocities * vel_fac)

            # Reset thermostat parameters.
            if self.md_engine in ["NVTBerendsen", "NPTBerendsen", "NPT", "Langevin"]:
                self.md.set_temperature(temperature_K=new_temp)
                self.md_kwargs["temperature"] = new_temp * units.kB

    def update_temperature(self):
        self.KE = self.structure.get_kinetic_energy()
        self.temperature = self.structure.get_temperature()

        # Convert velocities to Angstrom / ps.
        self.velocities = self.structure.get_velocities() * units.fs * 1e3

    def update_gp(self, train_atoms, dft_frcs, dft_energy=None, dft_stress=None):
        stds = self.flare_calc.results.get("stds", np.zeros_like(dft_frcs))
        self.output.add_atom_info(train_atoms, stds)

        # Convert ASE stress (xx, yy, zz, yz, xz, xy) to FLARE stress
        # (xx, xy, xz, yy, yz, zz).
        flare_stress = None
        if dft_stress is not None:
            flare_stress = -np.array(
                [
                    dft_stress[0],
                    dft_stress[5],
                    dft_stress[4],
                    dft_stress[1],
                    dft_stress[3],
                    dft_stress[2],
                ]
            )

        if self.force_only:
            dft_energy = None
            flare_stress = None

        # The structure will be added to self.gp.training_structures (struc.Structure).
        # Create a new structure by deepcopy to avoid the forces of the saved
        # structure get modified.
        try:
            struc_to_add = deepcopy(self.structure)
        except TypeError:
            # The structure might be attached with a non-picklable calculator,
            # e.g., when we use LAMMPS empirical potential for training. 
            # When deepcopy fails, create a SinglePointCalculator to store results

            from ase.calculators.singlepoint import SinglePointCalculator

            properties = ["forces", "energy", "stress"]
            results = {
                "forces": self.structure.forces,
                "energy": self.structure.potential_energy,
                "stress": self.structure.stress,
            }

            calc = self.structure.calc
            self.structure.calc = None
            struc_to_add = deepcopy(self.structure)
            struc_to_add.calc = SinglePointCalculator(struc_to_add, **results)
            self.structure.calc = calc

        # update gp model
        self.gp.update_db(
            struc_to_add,
            dft_frcs,
            custom_range=train_atoms,
            energy=dft_energy,
            stress=flare_stress,
        )

        self.gp.set_L_alpha()

        # train model
        if (self.dft_count - 1) < self.freeze_hyps:
            self.train_gp()

        # update mgp model
        if self.flare_calc.use_mapping:
            self.flare_calc.build_map()

        # write model
        if (self.dft_count - 1) < self.freeze_hyps:
            if self.write_model == 2:
                self.write_gp()
        if self.write_model == 3:
            self.write_gp()

    def record_dft_data(self, structure, target_atoms):
        structure.info["target_atoms"] = np.array(target_atoms)
        write(self.dft_xyz, structure, append=True)

    def as_dict(self):

        # DFT module and Trajectory are not picklable
        self.dft_module = self.dft_module.__name__
        md = self.md
        self.md = None
        _kernels = self._kernels
        self._kernels = None
        dft_loc = self.dft_loc
        self.dft_loc = None
        calc = self.dft_input.calc
        self.dft_input.calc = None

        gp = self.gp
        self.gp = None

        # Deepcopy OTF object.
        dct = deepcopy(dict(vars(self)))

        # Reset attributes.
        self.dft_module = eval(self.dft_module)
        self.md = md
        self._kernels = _kernels
        self.dft_loc = dft_loc
        self.dft_input.calc = calc
        self.gp = gp

        # write atoms and flare calculator to separate files
        write(self.structure_name, self.structure)
        dct["atoms"] = self.structure_name

        self.flare_calc.write_model(self.flare_name)
        dct["flare_calc"] = self.flare_name

        # dump dft calculator as pickle
        with open(self.dft_name, "wb") as f:
            pickle.dump(self.dft_loc, f)  # dft_loc is the dft calculator
        dct["dft_loc"] = self.dft_name

        dct["gp"] = self.gp_name

        for key in ["output", "pred_func", "structure", "dft_input", "md"]:
            dct.pop(key)
        dct["md"] = self.md.todict()

        return dct

    @staticmethod
    def from_dict(dct):
        flare_calc_dict = json.load(open(dct["flare_calc"]))

        # Build FLARE_Calculator from dict 
        if flare_calc_dict["class"] == "FLARE_Calculator":
            flare_calc = FLARE_Calculator.from_file(dct["flare_calc"])
            _kernels = None
        # Build SGP_Calculator from dict
        # TODO: we still have the issue that the c++ kernel needs to be 
        # in the current space, otherwise there is Seg Fault
        # That's why there is the _kernels
        elif flare_calc_dict["class"] == "SGP_Calculator":
            from flare_pp.sparse_gp_calculator import SGP_Calculator
            flare_calc, _kernels = SGP_Calculator.from_file(dct["flare_calc"])
        else:
            raise TypeError(
                f"The calculator from {dct['flare_calc']} is not recognized."
            )

        flare_calc.reset()
        dct["atoms"] = read(dct["atoms"])
        dct["calculator"] = flare_calc
        dct.pop("gp")

        with open(dct["dft_loc"], "rb") as f:
            dct["dft_calc"] = pickle.load(f)

        for key in ["dt", "dft_loc"]:
            dct.pop(key)

        new_otf = ASE_OTF(**dct)
        new_otf._kernels = _kernels
        new_otf.dft_count = dct["dft_count"]
        new_otf.curr_step = dct["curr_step"]
        new_otf.std_tolerance = dct["std_tolerance"]

        if new_otf.md_engine == "NPT":
            if not new_otf.md.initialized:
                new_otf.md.initialize()
        return new_otf

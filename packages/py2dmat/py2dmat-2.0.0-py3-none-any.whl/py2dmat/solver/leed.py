from typing import List
import itertools
import os
import os.path
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path

import numpy as np

import py2dmat
from py2dmat import exception


class Solver(py2dmat.solver.SolverBase):
    path_to_solver: Path

    dimension: int

    def __init__(self, info: py2dmat.Info):
        super().__init__(info)

        self._name = "leed"
        info_s = info.solver

        # Check keywords
        def check_keywords(key, segment, registered_list):
            if (key in registered_list) is False:
                msg = "Error: {} in {} is not correct keyword.".format(key, segment)
                raise RuntimeError(msg)

        keywords_solver = ["name", "config", "reference"]
        keywords = {}
        keywords["config"] = ["path_to_solver"]
        keywords["reference"] = ["path_to_base_dir"]

        for key in info_s.keys():
            check_keywords(key, "solver", keywords_solver)
            if key == "name":
                continue
            for key_child in info_s[key].keys():
                check_keywords(key_child, key, keywords[key])

        # Set environment
        p2solver = info_s["config"].get("path_to_solver", "satl2.exe")
        if os.path.dirname(p2solver) != "":
            # ignore ENV[PATH]
            self.path_to_solver = self.root_dir / Path(p2solver).expanduser()
        else:
            for P in itertools.chain([self.root_dir], os.environ["PATH"].split(":")):
                self.path_to_solver = Path(P) / p2solver
                if os.access(self.path_to_solver, mode=os.X_OK):
                    break
        if not os.access(self.path_to_solver, mode=os.X_OK):
            raise exception.InputError(f"ERROR: solver ({p2solver}) is not found")

        self.path_to_base_dir = info_s["reference"]["path_to_base_dir"]
        # check files
        files = ["exp.d", "rfac.d", "tleed4.i", "tleed5.i", "tleed.o", "short.t"]
        for file in files:
            if not os.path.exists(os.path.join(self.path_to_base_dir, file)):
                raise exception.InputError(
                    f"ERROR: input file ({file}) is not found in ({self.path_to_base_dir})"
                )
        self.input = Solver.Input(info)

    def prepare(self, message: py2dmat.Message) -> None:
        self.work_dir = self.proc_dir
        for dir in [self.path_to_base_dir]:
            copy_tree(os.path.join(self.root_dir, dir), os.path.join(self.work_dir))
        self.input.prepare(message)

    def run(self, nprocs: int = 1, nthreads: int = 1) -> None:
        self._run_by_subprocess([str(self.path_to_solver)])

    def get_results(self) -> float:
        # Get R-factor
        rfactor = -1.0
        filename = os.path.join(self.work_dir, "search.s")
        with open(filename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                if "R-FACTOR" in line:
                    rfactor = float(line.split("=")[1])
                    break
        if rfactor == -1.0:
            msg = f"R-FACTOR cannot be found in {filename}"
            raise RuntimeError(msg)
        return rfactor

    class Input(object):
        root_dir: Path
        output_dir: Path
        dimension: int

        def __init__(self, info):
            self.dimension = info.base["dimension"]
            self.root_dir = info.base["root_dir"]
            self.output_dir = info.base["output_dir"]

        def prepare(self, message: py2dmat.Message):
            x_list = message.x
            step = message.step
            extra = message.set > 0
            # Delete output files
            delete_files = ["search.s", "gleed.o"]
            for file in delete_files:
                if os.path.exists(file):
                    os.remove(file)
            # Generate fit file
            # Add variables by numpy array.(Variables are updated in optimization process).
            self._write_fit_file(x_list)

        def _write_fit_file(self, variables):
            with open("tleed4.i", "r") as fr:
                contents = fr.read()
            for idx, variable in enumerate(variables):
                # FORTRAN format: F7.6
                svariable = str(variable).zfill(6)[:6]
                contents = contents.replace(
                    "opt{}".format(str(idx).zfill(3)), svariable
                )
            with open("tleed4.i", "w") as writer:
                writer.write(contents)

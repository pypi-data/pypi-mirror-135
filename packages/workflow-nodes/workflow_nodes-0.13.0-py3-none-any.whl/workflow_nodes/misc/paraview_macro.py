# Copyright 2021 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import subprocess
import sys

from xmlhelpy import argument
from xmlhelpy import option

from .main import misc


@misc.command(description="A node for executing Paraview macros with pvypthon.")
@argument("macroname", description="File name of the Paraview Macro.", required=True)
@option(
    "inputfile",
    char="i",
    description="Inputfile including extension which is processed within the macro.",
    required=False,
)
@option(
    "outputfile",
    char="o",
    description="Outputfile including extension which is created within the macro."
    " It has to match with what is defined in the macro;"
    " either screenshot (e.g. png) or field data (e.g. vtk).",
    required=False,
)
def paraview_macro(macroname, inputfile, outputfile):
    """Run a Paraview macro."""

    if inputfile:
        inputstr = inputfile.split(".")
        if len(inputstr) == 1:
            print("Inputfile extension is missing.")
            sys.exit(1)
        else:
            regex_input = r"(?<=FileNames=\[\').*?(?=\'\])"

    if outputfile:
        outputstr = outputfile.split(".")
        if len(outputstr) == 1:
            print("Outputfile extension is missing.")
            sys.exit(1)
        elif outputfile.endswith((".png", ".jpg", ".tif", ".bmp", "ppm")):
            regex_output = r"(?<=SaveScreenshot\(\').*?(?=\'\,)"
        elif outputfile.endswith((".stl", ".vtk", ".pvd", "vtp")):
            regex_output = r"(?<=SaveData\(\').*?(?=\'\,)"
        else:
            print("Outputfile format is not supported.")
            sys.exit(1)

    with open(macroname, encoding="utf-8") as f:
        macrolines = f.readlines()

    if inputfile:
        # for i in range(0, len(macrolines)):
        for i, line in enumerate(macrolines):
            if re.search("FileNames", line):
                macrolines[i] = re.sub(regex_input, inputfile, line)

    if outputfile:
        for i, line in enumerate(macrolines):
            if re.search("Save", line):
                macrolines[i] = re.sub(regex_output, outputfile, line)

    if inputfile or outputfile:
        with open(macroname, mode="w", encoding="utf-8") as f:
            for new_line in macrolines:
                f.write(new_line)

    cmd = ["pvpython", macroname]

    print(" ".join(cmd))
    sys.exit(subprocess.call(cmd))

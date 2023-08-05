# Copyright 2020 Karlsruhe Institute of Technology
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
import subprocess
import sys

from xmlhelpy import Integer
from xmlhelpy import option

from .main import simulation


@simulation.command(description="A mpipace3D node for starting simulations locally")
@option(
    "specificsolver",
    char="s",
    description="Specify a certain mpipace3D solver",
    required=False,
)
@option(
    "numofprocessors",
    char="n",
    param_type=Integer,
    description="Set the number of processors",
    required=True,
)
@option(
    "infile",
    char="I",
    required=True,
    description="Required to specify the starting calues of the simulation"
    " embedded Infile",
)
@option(
    "pathname",
    char="P",
    required=True,
    description="This path specifies the working path where all simulation files will"
    " be written to",
)
@option(
    "force",
    char="f",
    required=False,
    description="Force to remove existing outfiles",
    is_flag=True,
)
@option(
    "overwrite",
    char="o",
    required=False,
    description="Giva a list of key=value pairs separated by '|' for overwriting or"
    "appending values in the infile. If '|' is used the list has to be surrounded by."
    " This feature is useful for simulation series",
)
@option(
    "continuing",
    char="C",
    description="Continue a simulation starting with the last frame.",
    is_flag=True,
)
@option(
    "respawn",
    char="R",
    description="Specify a data set as a starting configuration for the simulation."
    " /path/to/simulation.p3simgeo represents the whole simulation data set to be used",
)
@option(
    "frame",
    char="F",
    description="Frame number to start the simulation for respawn. As a special value"
    " 'end' can be used for the last available frame of all data files.",
)
@option(
    "copy",
    char="c",
    description="Copy previous frames up to the respawn timestep into the outfiles,"
    " in case of a respawn.",
    is_flag=True,
)
@option(
    "append",
    char="a",
    required=False,
    is_flag=True,
    description="Append simulation to an existing one",
)
@option(
    "dopreconditioning",
    char="p",
    description="Preconditioning from infile should be used after respawn.",
    is_flag=True,
)
@option(
    "dofilling",
    char="d",
    description="Filling functions from infile should be used after loading the"
    " respawn data.",
    is_flag=True,
)
@option(
    "logfile",
    char="L",
    description="Specify a file to which the log output data is going to be written to,"
    " otherwise stdout/stderr is used.",
)
@option(
    "msgscript",
    char="M",
    description="Specify a script which will receive messages. This script should send"
    " the messages given as a parameter to the user.",
)
@option(
    "msglevel",
    char="m",
    description="How many messages should be send. 0: start/stop, 1: all",
    param_type=Integer,
)
@option(
    "info", char="i", description="Print program and system information.", is_flag=True
)
@option(
    "verbose",
    char="v",
    description="Enable the output (stderr) of some (helpful) log messages, a higher"
    " level will create more messages.",
    param_type=Integer,
)
@option("showhelp", char="h", description="print help", is_flag=True)
def mpipace3D(*args, **kwargs):
    """Start a simulation using multiple processors."""

    cmd = ["mpirun", "-np", str(kwargs["numofprocessors"])]

    if kwargs["specificsolver"]:
        cmd += [kwargs["specificsolver"]]
    else:
        cmd += ["mpipace3D"]

    cmd += ["-I", kwargs["infile"], "-P", kwargs["pathname"]]

    if kwargs["overwrite"]:
        cmd += ["-o", kwargs["overwrite"]]
    if kwargs["continuing"]:
        cmd += ["-C"]
    if kwargs["respawn"]:
        cmd += ["-R", kwargs["respawn"]]
    if kwargs["frame"]:
        cmd += ["-F", kwargs["frame"]]
    if kwargs["copy"]:
        cmd += ["-c"]
    if kwargs["append"]:
        cmd += ["-a"]
    if kwargs["dopreconditioning"]:
        cmd += ["-p"]
    if kwargs["dofilling"]:
        cmd += ["-d"]
    if kwargs["logfile"]:
        cmd += ["-L", kwargs["logfile"]]
    if kwargs["msgscript"]:
        cmd += ["-M", kwargs["msgscript"]]
    if kwargs["msglevel"]:
        cmd += ["-m", str(kwargs["msglevel"])]
    if kwargs["info"]:
        cmd += ["-i"]
    if kwargs["verbose"]:
        cmd += ["-v", str(kwargs["verbose"])]
    if kwargs["showhelp"]:
        cmd += ["-h"]
    if kwargs["force"]:
        cmd += ["-f"]

    print(" ".join(cmd))
    sys.exit(subprocess.call(cmd))

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

from .main import wsl


@wsl.command(description="Wrapper node for LabVIEWCLI on MS Windows")
@option(
    "operation-name",
    char="o",
    description="Name of LabVIEWCLI operation (eg: MassCompile, CloseLabVIEW, RunVI,"
    " ...)",
    required=False,
)
@option(
    "port-number",
    char="n",
    description="Port on which the remote LabVIEW application is listening",
    param_type=Integer,
    required=False,
)
@option(
    "labview-path",
    char="p",
    description="Path of the LabVIEW in which the operation will run",
    required=False,
)
@option(
    "logfile-path",
    char="l",
    description="Path of the LabVIEWCLI log file.",
    required=False,
)
@option(
    "no-log-to-console",
    char="c",
    description="If set, the output gets logged only to log file (otherwise log"
    " file and console)",
    is_flag=True,
    required=False,
)
@option(
    "verbosity",
    char="v",
    description="This command line argument is used to control the output being logged."
    ' Default is "Default". Possible values are Minimal, Default, Detailed,'
    " Diagnostic",
    default="Default",
    required=False,
)
@option(
    "additional-operation-directory",
    char="a",
    description="Additional directory where LabVIEWCLI will look for additional"
    " operation class other than default location",
    required=False,
)
def labview_cli(
    operation_name,
    port_number,
    labview_path,
    logfile_path,
    no_log_to_console,
    verbosity,
    additional_operation_directory,
):
    """Wrapper node for LabVIEWCLI on MS Windows."""

    cmd = ["LabVIEWCLI.exe"]
    if operation_name:
        cmd += ["-OperationName", operation_name]
    if port_number:
        cmd += ["-PortNumber", str(port_number)]
    if labview_path:
        cmd += ["-LabVIEWPath", labview_path]
    if logfile_path:
        cmd += ["-LogFilePath", logfile_path]
    if no_log_to_console:
        cmd += ["-LogToConsole", "False"]
    if verbosity:
        cmd += ["-Verbosity", verbosity]
    if additional_operation_directory:
        cmd += ["-AdditionalOperationalDirectory"]
    sys.exit(subprocess.call(cmd))

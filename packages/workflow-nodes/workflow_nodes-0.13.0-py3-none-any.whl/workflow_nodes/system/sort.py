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

from xmlhelpy import argument
from xmlhelpy import option

from .main import system


@system.command(description="Wrapper node for sort (GNU coreutils)")
@argument("file", description="file to sort", required=True)
@option("field-separator", char="t", description="separator of fields", required=False)
@option(
    "numeric-sort",
    char="n",
    description="compare according to string numerical value",
    is_flag=True,
)
@option("key", char="k", description="sort via a key", required=False)
def sort(*args, **kwargs):
    """Wrapper node for sort."""

    cmd = ["sort"]
    if "numeric_sort" in kwargs and kwargs["numeric_sort"] is not None:
        cmd.append("-n")
    if "field_separator" in kwargs and kwargs["field_separator"] is not None:
        cmd.append("-t")
        cmd.append(kwargs["field_separator"])
    if "key" in kwargs and kwargs["key"] is not None:
        cmd.append("-k")
        cmd.append(kwargs["key"])
    if "file" in kwargs and kwargs["file"] is not None:
        cmd.append(kwargs["file"])
    # Do not write to stdout to keep output intact for piping.
    print(" ".join(cmd), file=sys.stderr)
    sys.exit(subprocess.call(cmd))

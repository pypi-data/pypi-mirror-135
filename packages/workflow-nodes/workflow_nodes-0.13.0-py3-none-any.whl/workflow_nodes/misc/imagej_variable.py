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
import re
import sys
from pathlib import Path

from xmlhelpy import option

from .main import misc


@misc.command(
    description="Turn a string value into a variable which can be used together with"
    " the imagej_macro node, then store in a file.",
    example=(
        'imagej_variable --name "crop_selection" --variable "[53, 132, 150, 293]"'
        ' --outfile "myvariables.imjv"'
    ),
)
@option("name", char="n", description="The name of the variable", required=True)
@option("value", char="v", description="The value of the variable", required=True)
@option(
    "output_file",
    char="o",
    description=(
        "The file used as variable store, the new variable will be appended to it"
    ),
    default=".variables.ijmv",
    required=False,
)
@option(
    "split_vector",
    char="s",
    is_flag=True,
    description="Split the variable value into multiple variables. "
    "The format must be [a, b, c, d, e...] where each item will be "
    "treated as a variable itself with the name {$variable_name}_0, "
    "{$variable_name}_1 and so forth.",
)
def imagej_variable(*args, **kwargs):
    """Turn a string value into a variable."""

    name = kwargs["name"]
    value = kwargs["value"]
    outfile = kwargs["output_file"]
    split_vector = kwargs["split_vector"]

    if not name:
        print("Error: The variable name must not be empty.", file=sys.stderr)
        sys.exit(1)

    if split_vector:
        # assume the format "[a, b, c, e, f]"
        vector_str = value.strip('"')
        vector_str = vector_str.lstrip("[")
        vector_str = vector_str.rstrip("]")  # remove parantheses
        values = list(map(lambda a: a.strip(), vector_str.split(",")))
        if len(values) == 0:
            print(
                f"Error: Could not split vector {vector_str} (expected format:"
                " [a, b, c, ...].",
                file=sys.stderr,
            )
        for (i, v) in enumerate(values):
            store_variable(f"{name}_{i}", outfile, v)

    else:
        store_variable(name, outfile, value)


def store_variable(name, outfile, value):
    """function to store a variable"""

    if re.search("^[0-9.,]+$", value) is None:
        # this is not a number, wrap it in double quotes
        value = f'"{value}"'
    variable_str = f"{name}={value}\n"
    with Path(outfile).expanduser().open(mode="a+") as f:
        f.write(variable_str)
    print("Wrote {} to {}".format(variable_str.rstrip("\n"), outfile))

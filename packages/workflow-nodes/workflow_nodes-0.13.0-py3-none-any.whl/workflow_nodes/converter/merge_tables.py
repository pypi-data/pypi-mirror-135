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
import sys

import pandas as pd
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import option

from .main import converter


@converter.command()
@argument(
    "filenames",
    required=True,
    description="Name of the input files",
)
@option(
    "separator_in",
    char="s",
    description="Columns separator input table",
    default="tab",
    param_type=Choice(["space", "tab", "comma"]),
)
@option(
    "separator_out",
    char="S",
    description="Columns separator ouput table",
    default=None,
    param_type=Choice(["space", "tab", "comma"]),
)
@option(
    "columns",
    char="u",
    required=False,
    description="Specified columns from input file to be merged",
)
@option(
    "columns_x",
    char="x",
    default=None,
    description="Colums for x axsis data",
)
@option(
    "columns_y",
    char="y",
    default=None,
    description="Colums for x axsis data",
)
@option(
    "output_name",
    char="o",
    default="merged_table",
    description="Name of the new merged table",
)
@option(
    "output_format",
    char="O",
    default="csv",
    description="Format of the new merged table",
)
@option(
    "missing_number_fill_in",
    char="m",
    default="nan",
    description="Fill this in for missing numbers",
)
def merge_tables(*args, **kwargs):
    """Merge from different files two columns respectively."""

    filenames = kwargs["filenames"]
    separator_in = kwargs["separator_in"]
    separator_out = kwargs["separator_out"]
    output_name = kwargs["output_name"]
    output_format = kwargs["output_format"]
    missing_number_fill_in = kwargs["missing_number_fill_in"]
    columns = kwargs["columns"]

    columns_x = kwargs["columns_x"]
    columns_y = kwargs["columns_y"]

    if separator_in == "tab":
        separator_in_ = "\t"
    elif separator_in == "space":
        separator_in_ = r"\s+"
    else:
        separator_in_ = ","

    if separator_out is None:
        separator_out = separator_in

    if separator_out == "tab":
        separator_out = "\t"
    elif separator_out == "space":
        separator_out = " "
    else:
        separator_out = ","

    if columns is None:
        if (columns_x or columns_y) is None:
            print("Specify the columns to merge")
            sys.exit(1)

    filenames_list = filenames.split(",")

    if columns is not None:
        columns_list = columns.split(",")

    if (columns_x and columns_y) is not None:
        columns_x_list = columns_x.split(",")
        columns_y_list = columns_y.split(",")

    for loop_number, loop_name in enumerate(filenames_list):
        data = pd.read_csv(loop_name, sep=separator_in_)
        if columns is not None:
            columns_to_merge = columns_list[loop_number].split(":")
            new_table_data_x = data.columns[int(columns_to_merge[0])]
            new_table_data_y = data.columns[int(columns_to_merge[1])]

        if (columns_x and columns_y) is not None:
            new_table_data_x = columns_x_list[loop_number]
            new_table_data_y = columns_y_list[loop_number]

        print(
            f"Read columns {new_table_data_x} and {new_table_data_y} from {loop_name}"
        )

        data_new_table = data[[(new_table_data_x), (new_table_data_y)]]

        if loop_number == 0:
            new_data = data_new_table.copy()
        else:
            new_data = pd.concat([new_data, data_new_table], axis=1, ignore_index=False)

    output_name_file = output_name + "." + output_format
    new_data.to_csv(
        output_name_file,
        sep=separator_out,
        float_format="%.08f",
        index=False,
        na_rep=missing_number_fill_in,
    )
    print(f"Save new table: {output_name_file}")

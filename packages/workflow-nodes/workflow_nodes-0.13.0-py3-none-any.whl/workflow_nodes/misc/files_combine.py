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
import sys
from glob import glob

import pandas as pd
from xmlhelpy import Choice
from xmlhelpy import option

from .main import misc


@misc.command()
@option(
    "files",
    char="i",
    required=True,
    description="Inputfiles (tsv, csv); wildcard pattern is possible "
    "for file series.",
)
@option(
    "headerrow",
    char="r",
    required=False,
    default="0",
    param_type=Choice(["0", "None"]),
    description="Specify that the files have no header."
    "Per default they do have a header.",
)
@option(
    "outputfile",
    char="o",
    required=True,
    description="Name of the output file.",
)
@option(
    "row_col",
    char="d",
    required=True,
    description="Concatenate row-wise (same number of columns) "
    "or column-wise (same number of rows).",
    param_type=Choice(["rows", "columns"]),
)
@option(
    "separator",
    char="s",
    description="Columns separator.",
    default="space",
    param_type=Choice(["space", "tab", "comma"]),
)
def files_combine(*args, **kwargs):
    """Combines files row-wise OR column-wise."""

    inputlist = kwargs["files"]
    headerrow = kwargs["headerrow"]
    row_col = kwargs["row_col"]
    outputfile = kwargs["outputfile"]
    separator = kwargs["separator"]

    files = inputlist.split(",")
    for file_in in files:
        if "*" not in file_in and len(files) <= 1:
            print("At least two files or a file series is expected")
            sys.exit(1)

    if outputfile is None:
        print("Outputfile has to be specified")
        sys.exit(1)

    if headerrow == "0":
        headerrow = int(headerrow)
    else:
        headerrow = None

    if separator == "tab":
        separator = "\t"
        separator_out = "\t"
    elif separator == "space":
        separator = r"\s+"
        separator_out = " "
    else:
        separator = ","
        separator_out = ","

    tmp_files_list = []
    for file_in in files:
        if "*" in file_in:
            fileseries = glob(file_in)
            for tmp_file in fileseries:
                tmp_files_list.append(tmp_file)
        else:
            tmp_files_list.append(file_in)

    tmp_files_list.sort()

    list_of_df = []
    for file_in_list in tmp_files_list:
        df = pd.read_csv(file_in_list, sep=separator, header=headerrow)
        if df.columns[0] == "#":
            tmp = []
            tmp.append(df.columns[0] + df.columns[1])
            for i in range(2, len(df.columns)):
                tmp.append(df.columns[i])
            df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
            df.columns = tmp
        list_of_df.append(df)

    for df_n in list_of_df:
        if row_col == "rows" and list_of_df[0].shape[1] != df_n.shape[1]:
            print(
                "For rows to be combined properly, header names and number "
                "of columns in the files need to be the same"
            )
            sys.exit(1)
        elif row_col == "columns" and list_of_df[0].shape[0] != df_n.shape[0]:
            print(
                "For columns to be combined properly, number of rows "
                "in the files needs to be the same"
            )
            sys.exit(1)

    if row_col == "rows":
        df_to_write = pd.concat(list_of_df, axis=0)
    elif row_col == "columns":
        df_to_write = pd.concat(list_of_df, axis=1)
        df_to_write = df_to_write.T.drop_duplicates().T

    df_to_write.to_csv(
        outputfile, index=False, header=True, sep=separator_out, na_rep="NaN"
    )

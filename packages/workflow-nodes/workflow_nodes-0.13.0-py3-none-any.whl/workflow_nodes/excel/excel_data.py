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
import csv
import sys
from pathlib import Path

from xmlhelpy import option

from . import convert_number
from . import row_column_notation
from .main import excel


@excel.command(
    description="Prepares data to be added to an Excel document using ExcelAddData."
    " Appends data to a CSV file containing values with target cells."
)
@option(
    "file",
    char="f",
    description="File with values, will be read line by line",
    required=False,
)
@option(
    "single-value",
    char="s",
    description="Single value. Can not be used together with --file|-f",
    required=False,
)
@option("row", char="r", description="Row number", required=True)
@option("column", char="c", description="Column name (alphabetical)", required=True)
@option(
    "outfile",
    char="o",
    description="Output ",
    required=False,
    default=".excel-values.csv",
)
def excel_data(*args, **kwargs):
    """Prepares data to be added to an Excel document."""

    data = []
    if not (kwargs["file"] or kwargs["single_value"]):
        print("Error: No input value or file given.", file=sys.stderr)
        sys.exit(1)

    column = kwargs["column"]
    row = int(kwargs["row"])

    if kwargs["file"]:
        with Path(kwargs["file"]).expanduser().open() as f:
            for line in f:
                key = row_column_notation(row, column)
                value = line.strip("")
                value = convert_number(value)
                data.append([key, value])
                row += 1
    elif kwargs["single_value"]:
        key = row_column_notation(row, column)
        value = convert_number(kwargs["single_value"])
        data.append([key, value])

    write_csv(kwargs["outfile"], data)
    print(f"Excel data written to {kwargs['outfile']}.")


def write_csv(path, data):
    """Write in csv."""

    with Path(path).expanduser().open(mode="a") as result_file:
        writer = csv.writer(
            result_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_NONNUMERIC
        )

        for row in data:
            writer.writerow(row)

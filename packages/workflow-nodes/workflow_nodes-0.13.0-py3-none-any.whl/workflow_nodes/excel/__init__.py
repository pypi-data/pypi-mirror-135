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
# convert the string value to int or float if possible, keep the string value otherwise
def convert_number(value):
    """convert number"""

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def row_column_notation(row, column):
    """row_column_notation"""

    return column + str(row)

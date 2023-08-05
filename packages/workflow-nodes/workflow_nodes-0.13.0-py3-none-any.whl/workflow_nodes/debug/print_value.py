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
from xmlhelpy import Bool
from xmlhelpy import Float
from xmlhelpy import Integer
from xmlhelpy import option

from .main import debug


@debug.command()
@option("string_value", description="string to print", default=None)
@option(
    "integer_value", description="integer to print", default=None, param_type=Integer
)
@option("float_value", description="float to print", default=None, param_type=Float)
@option("bool_value", description="bool to print", default=None, param_type=Bool)
def print_value(string_value, integer_value, float_value, bool_value):
    """Function to print a value."""

    if string_value is not None:
        print(f"The input string is: {string_value}")

    if integer_value is not None:
        print(f"The input integer is: {integer_value}")

    if float_value is not None:
        print(f"The input float is: {float_value}")

    if bool_value is not None:
        print(f"The input bool is: {bool(bool_value)}")

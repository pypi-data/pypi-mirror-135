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
from workflow_nodes.main import workflow_nodes


@workflow_nodes.group()
def report():
    """Report tools."""
    # pylint: disable=unused-import


from .attachment_report import attachment_report
from .compile_latex_report import compile_latex_report
from .end_report import end_report
from .image_report import image_report
from .input_report import input_report
from .math_report import math_report
from .plot_report import plot_report
from .start_report import start_report
from .text_report import text_report

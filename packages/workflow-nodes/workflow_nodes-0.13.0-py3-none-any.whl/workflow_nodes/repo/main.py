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
def repo():
    """Tools that interact with the Kadi repo in a complex way."""
    # pylint: disable=unused-import


from .collection_visualize import collection_visualize
from .record_visualize import record_visualize
from .record_visualize_all import record_visualize_all

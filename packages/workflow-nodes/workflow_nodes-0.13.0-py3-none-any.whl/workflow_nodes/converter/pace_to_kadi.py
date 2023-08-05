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
from kadi_apy import apy_command
from kadi_apy import id_identifier_options
from xmlhelpy import option
from xmlhelpy import Path

from .main import converter


@converter.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to add the metadata")
@option(
    "infile_saved",
    char="S",
    required=True,
    param_type=Path(path_type="file", exists=True),
    description="Path to a file or directory.",
)
@option(
    "force",
    char="f",
    description="Force deleting and overwriting existing metadata",
    is_flag=True,
)
def pace_to_kadi(record, infile_saved, force):
    """Imports an infile saved and transfers the contained metadata into Kadi."""

    metadata = []

    with open(infile_saved, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                line = line.split("=")
                metadatum = line[0]
                value = line[1]
                unit = None
                metadatum_type = "str"

                metadatum_new = {
                    "type": metadatum_type,
                    "unit": unit,
                    "key": metadatum,
                    "value": value,
                }
                metadata.append(metadatum_new)

    record.add_metadata(metadata=metadata, force=force)

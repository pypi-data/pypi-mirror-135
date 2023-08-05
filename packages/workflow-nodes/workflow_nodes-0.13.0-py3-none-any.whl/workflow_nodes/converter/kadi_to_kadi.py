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
import json

from kadi_apy import apy_command
from kadi_apy import CLIKadiManager
from kadi_apy import id_identifier_options
from xmlhelpy import option
from xmlhelpy import Path

from .main import converter


@converter.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to copy to the second instance")
@option(
    "force",
    char="f",
    description="Force deleting and overwriting existing data",
    is_flag=True,
)
@option(
    "instance-2",
    char="T",
    description="Name of the second Kadi4Mat instance to use for the API.",
    required=True,
)
@option(
    "file-path",
    char="p",
    description="File path for downloading/uploading files.",
    required=True,
    param_type=Path(exists=True),
)
def kadi_to_kadi(record, instance_2, force, file_path):
    """Copy record data between two Kadi4Mat instances."""
    # pylint: disable=unexpected-keyword-arg

    meta = record.meta
    record.get_file(file_path, force)

    manager2 = CLIKadiManager(instance=instance_2)

    record_2 = manager2.record(
        identifier=meta["identifier"],
        title=meta["title"],
        create=True,
    )

    record_2.set_attribute(description=meta["description"])
    record_2.set_attribute(type=meta["type"])

    for tag in meta["tags"]:
        record_2.add_tag(tag)

    record_2.add_metadata(metadata=json.dumps(meta["extras"]), file=None, force=force)

    record_2.upload_file(file_name=file_path, force=force)

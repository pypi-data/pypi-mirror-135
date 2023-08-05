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
import shutil
import sys

import click
from graphviz import Digraph
from kadi_apy import apy_command
from kadi_apy import id_identifier_options
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import Integer
from xmlhelpy import option

from .main import repo


@repo.command()
@apy_command(use_kadi_manager=True)
@id_identifier_options(class_type="record", helptext="to start with", keep_manager=True)
@argument(
    "output_file",
    description="The filename of the resulting graph. The correct file extension is"
    " appended to the name depending on the format.",
)
@option(
    "output_format",
    char="f",
    description="Output format of the record graph.",
    default="pdf",
    param_type=Choice(["svg", "pdf", "png"]),
)
@option(
    "link_level",
    char="l",
    description="The maximum link distance to visualize.",
    default=2,
    param_type=Integer,
)
@option(
    "label_id",
    description="Use id and identifier to label the records.",
    is_flag=True,
)
def record_visualize(manager, record, output_file, output_format, link_level, label_id):
    """Visualize the links of a given record."""

    if not shutil.which("dot"):
        click.echo("'dot' not found in PATH, maybe Graphviz is not installed?")
        sys.exit(1)

    id_list = [record.id]
    id_list_current_level = [record.id]
    id_list_checked = []

    while link_level > 0:
        id_list_next_level = []

        for record_id in id_list_current_level:
            if record_id in id_list_checked:
                continue

            id_list_checked.append(record_id)
            current_record = manager.record(id=record_id, skip_request=True)
            items_to = current_record.get_record_links(direction="out").json()["items"]
            items_from = current_record.get_record_links(direction="in").json()["items"]

            for item in items_from:
                id_list_next_level.append(item["record_from"]["id"])
            for item in items_to:
                id_list_next_level.append(item["record_to"]["id"])

        id_list_current_level = list(set(id_list_next_level))
        id_list = id_list + id_list_next_level
        link_level = link_level - 1

    id_list = list(set(id_list))
    click.echo(f"Found {len(id_list)} record(s) to visualize.")

    dot = Digraph(
        format=output_format, node_attr={"color": "lightblue2", "style": "filled"}
    )

    for id in id_list:
        record = manager.record(id=id)
        meta = record.meta

        if label_id:
            label = f"@{meta['identifier']} (ID: {record.id})"
        else:
            label = meta["title"]

        dot.node(
            str(record.id),
            label,
            shape="ellipse",
            href=meta["_links"]["self"].replace("/api", ""),
        )
        response = record.get_record_links()

        if response.status_code == 200:
            payload = response.json()

            for results in payload["items"]:
                try:
                    if results["record_to"]["id"] in id_list and record.id in id_list:
                        dot.edge(
                            str(record.id),
                            str(results["record_to"]["id"]),
                            label=results["name"],
                        )
                    else:
                        pass
                except Exception as e:
                    click.echo(e)
        else:
            manager.raise_request_error(response)

    dot.render(output_file, cleanup=True)
    click.echo(f"Successfully created file '{output_file}.{output_format}'.")

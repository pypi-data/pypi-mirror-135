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
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import option

from .main import repo


@repo.command()
@apy_command(use_kadi_manager=True)
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
    "linked_only",
    char="l",
    is_flag=True,
    description="Flag indicating whether only records with at least one link should be"
    " shown.",
)
@option(
    "label_id",
    description="Use id and identifier to label the records.",
    is_flag=True,
)
def record_visualize_all(manager, output_file, output_format, linked_only, label_id):
    """Visualize a user's records and their links."""

    if not shutil.which("dot"):
        click.echo("'dot' not found in PATH, maybe Graphviz is not installed?")
        sys.exit(1)

    resource = manager.search_resource()
    responce = resource.search_items_user(
        item="record", user=resource.manager.pat_user_id
    )
    payload = responce.json()
    total_pages = payload["_pagination"]["total_pages"]

    record_ids = []
    for i in range(total_pages):
        response = resource.search_items_user(
            item="record", user=resource.manager.pat_user_id, page=i + 1
        )
        payload = response.json()
        for item in payload["items"]:
            record_id = item["id"]
            record = manager.record(id=record_id, skip_request=True)

            if linked_only:
                if (
                    not record.get_record_links(direction="out").json()["items"]
                    and not record.get_record_links(direction="in").json()["items"]
                ):
                    continue

                record_ids.append(item["id"])
            else:
                record_ids.append(item["id"])

    click.echo(f"Found {len(record_ids)} record(s) to visualize.")
    dot = Digraph(
        format=output_format, node_attr={"color": "lightblue2", "style": "filled"}
    )

    for id in record_ids:
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
                    dot.edge(
                        str(record.id),
                        str(results["record_to"]["id"]),
                        label=results["name"],
                    )
                except Exception as e:
                    click.echo(e)
        else:
            manager.raise_request_error(response)

    dot.render(output_file, cleanup=True)
    click.echo(f"Successfully created file '{output_file}.{output_format}'.")

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
import shutil
import sys

import click
from graphviz import Digraph
from kadi_apy import apy_command
from kadi_apy import id_identifier_options
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import option

from .main import repo


@repo.command()
@apy_command
@id_identifier_options(
    class_type="collection",
    helptext="to visualize (main collection)",
    keep_manager=True,
)
@argument(
    "output_file",
    description="The filename of the resulting graph. The correct file extension is"
    " appended to the name depending on the format.",
)
@option(
    "output_format",
    char="f",
    description="Output format of the collection graph.",
    default="pdf",
    param_type=Choice(["svg", "pdf", "png"]),
)
@option(
    "label_id",
    description="Use id and identifier to label the collection(s) and records.",
    is_flag=True,
)
@option(
    "vis_per",
    description="Visualize the peripheral collection(s) from the records.",
    is_flag=True,
)
def collection_visualize(
    manager, collection, output_file, output_format, label_id, vis_per
):
    """Visualize all the records within a given collection."""

    if not shutil.which("dot"):
        click.echo("'dot' not found in PATH, maybe Graphviz is not installed?")
        sys.exit(1)

    id_list_records = []
    id_list_collections = []
    main_collection_id = collection.id
    id_list_collections = [main_collection_id]

    page = 1
    response = collection.get_records(page=page, per_page=100)

    if response.status_code == 200:
        payload = response.json()

        total_pages = payload["_pagination"]["total_pages"]
        for page in range(1, total_pages + 1):
            if page != 1:
                payload = collection.get_records(page=page, per_page=100).json()
            for results in payload["items"]:
                id_list_records.append(results["id"])
    else:
        manager.raise_request_error(response)

    click.echo(
        f"Found {len(id_list_records)} record(s) in the {collection} to visualize."
    )

    if vis_per:
        for id in id_list_records:
            record = manager.record(id=id)
            payload = record.get_collection_links().json()
            total_items = payload["_pagination"]["total_items"]
            if total_items > 1:
                items = record.get_collection_links().json()["items"]
                for peri_collection in items:
                    if peri_collection["id"] is not collection.id:
                        id_list_collections.append(peri_collection["id"])
            else:
                continue
        click.echo(f"Found {len(id_list_collections)-1} peripheral collection(s).")

    dot = Digraph(
        format=output_format, node_attr={"color": "lightblue2", "style": "filled"}
    )

    for collection_id in id_list_collections:
        collection = manager.collection(id=collection_id)
        meta = collection.meta

        if label_id:
            label = f"@{meta['identifier']} (ID: {collection_id})"
        else:
            label = meta["title"]

        if vis_per and collection_id is not main_collection_id:
            dot.node(
                str(collection_id),
                label,
                shape="box",
                color="grey",
                peripheries="2",
                href=meta["_links"]["self"].replace("/api", ""),
            )
        else:
            dot.node(
                str(collection_id),
                label,
                shape="box",
                color="aquamarine3",
                peripheries="2",
                href=meta["_links"]["self"].replace("/api", ""),
            )

    for id in id_list_records:
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

        dot.edge(
            str(main_collection_id),
            str(record.id),
            style="dashed",
            color="aquamarine3",
        )
        response = record.get_record_links()

        if response.status_code == 200:
            payload = response.json()

            for results in payload["items"]:
                try:
                    if (
                        results["record_to"]["id"] in id_list_records
                        and record.id in id_list_records
                    ):
                        dot.edge(
                            str(record.id),
                            str(results["record_to"]["id"]),
                            label=results["name"],
                            color="lightblue2",
                        )
                    else:
                        pass
                except Exception as e:
                    click.echo(e)
        else:
            manager.raise_request_error(response)

        if vis_per:
            payload = record.get_collection_links().json()
            total_items = payload["_pagination"]["total_items"]
            if total_items > 1:
                items = record.get_collection_links().json()["items"]
                for peri_collection in items:
                    if peri_collection["id"] is not main_collection_id:
                        dot.edge(
                            str(record.id),
                            str(peri_collection["id"]),
                            style="dashed",
                            color="grey",
                        )

    dot.render(output_file, cleanup=True)
    click.echo(f"Successfully created file '{output_file}.{output_format}'.")

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
import copy
import sys

import click
from defusedxml.ElementTree import parse
from kadi_apy import apy_command
from kadi_apy import id_identifier_options
from xmlhelpy import option
from xmlhelpy import Path

from .main import converter


def _convert_type(convert, metadatum_value, metadatum_type=None):

    if metadatum_type is None:
        metadatum_type = "str"

    if convert:
        try:
            return int(metadatum_value), "int"
        except:
            pass

        try:
            return float(metadatum_value), "float"
        except:
            pass

        try:
            return _convert_bool(metadatum_value), "bool"
        except:
            pass

    return metadatum_value, metadatum_type


def _map_type(value, type):
    if type == "int":
        value = int(value)
    elif type == "float":
        value = float(value)
    elif type == "bool":
        value = _convert_bool(value)
    return value


def _convert_bool(value):
    if str(value).lower() == "true":
        return True
    if str(value).lower() == "false":
        return False
    raise ValueError("Not a bool:" + str(value))


def _convert_xml(element, convert=False):

    values_nested = []

    additional_parameter = dict(element.attrib)

    try:
        metadatum = element.text.strip()
    except:
        metadatum = None

    # Just a metadatum to add since no additional parameters and no children.
    if metadatum and not additional_parameter and len(element) == 0:
        metadatum, metadatum_type = _convert_type(convert, metadatum)
        return [{"type": metadatum_type, "key": element.tag, "value": metadatum}]

    # Can not be mapped.
    if metadatum and len(element) > 0:
        click.echo(
            f"You are using text ('{metadatum}') within element '{element.tag}' and"
            " further children. No mapping possible."
        )
        sys.exit(1)

    # If there are no more children and not metadatum, we can check if keys like unit or
    # type are available within the additional parameters.
    if len(element) == 0 and not metadatum:
        unit = None
        type = None
        value = None
        additional_parameter_try_convert = copy.deepcopy(additional_parameter)
        if "unit" in additional_parameter_try_convert:
            unit = additional_parameter_try_convert.get("unit")
            del additional_parameter_try_convert["unit"]
        if "type" in additional_parameter_try_convert:
            type = additional_parameter_try_convert.get("type")
            del additional_parameter_try_convert["type"]
        if "value" in additional_parameter_try_convert:
            value = additional_parameter_try_convert.get("value")
            del additional_parameter_try_convert["value"]

        # If there are no additional parameters any more, we just return the metadatum
        # with available information.
        if not additional_parameter_try_convert:
            if type is None:
                value, type = _convert_type(convert, value, type)
            else:
                try:
                    value = _map_type(value, type)
                except ValueError as e:
                    click.echo(e, err=True)
                    click.echo(f"Converting {value} into a {type} was not successful.")
                    sys.exit(1)
            return [{"type": type, "key": element.tag, "value": value, "unit": unit}]

    # We add the additional parameter to values_nested since we build a dict.
    if additional_parameter:
        if metadatum:
            temp = []
            for key, value in additional_parameter.items():
                value, metadatum_type = _convert_type(convert, value)
                temp.append({"type": metadatum_type, "key": key, "value": value})
            values_nested.append({"type": "dict", "key": metadatum, "value": temp})
        else:
            for key, value in additional_parameter.items():
                value, metadatum_type = _convert_type(convert, value)
                values_nested.append(
                    {"type": metadatum_type, "key": key, "value": value}
                )

    # Add more children to values_nested since we build a dict.
    for child in element:
        values_nested.extend(_convert_xml(child, convert))

    return [{"key": element.tag, "type": "dict", "value": values_nested}]


@converter.command()
@apy_command
@id_identifier_options(class_type="record", helptext="to add the metadata")
@option(
    "xml-file",
    char="x",
    required=True,
    param_type=Path(path_type="file", exists=True),
    description="Path to xml file.",
)
@option(
    "convert",
    char="c",
    description="Try to convert strings to integers, floats or bools.",
    is_flag=True,
)
@option(
    "force",
    char="f",
    description="Force deleting and overwriting existing metadata.",
    is_flag=True,
)
def xml_to_kadi(record, xml_file, convert, force):
    """Read an xml file and add the metadata to a record."""

    try:
        root = parse(xml_file).getroot()
    except Exception as e:
        click.echo(e, err=True)
        click.echo("During parsing of the xml file, an error occurred.")
        sys.exit(1)

    record.add_metadata(metadata=_convert_xml(root, convert), force=force)

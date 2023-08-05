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
import os.path

from qrcode import make
from qrcode.image import svg
from xmlhelpy import Choice
from xmlhelpy import option
from xmlhelpy import Path

from .main import misc


@misc.command(description="Create a QR-code")
@option("string", char="s", description="String to convert", required=True)
@option("filename", char="f", description="Name", default="output")
@option(
    "type",
    char="t",
    var_name="image_type",
    description="Type",
    default="png",
    param_type=Choice(["png", "jpg", "jpeg", "svg"]),
)
@option(
    "path",
    char="p",
    description="Path",
    param_type=Path(path_type="dir", exists=True),
)
def create_qr_code(string, filename, image_type, path):
    """Create a QR-code of a string and save it as an image."""

    filename = os.path.splitext(filename)[0]
    filename = f"{filename}.{image_type}"

    if path:
        filename = os.path.join(path, filename)

    if image_type == "svg":
        img = make(string, image_factory=svg.SvgPathImage)
    else:
        img = make(string)

    img.save(filename)

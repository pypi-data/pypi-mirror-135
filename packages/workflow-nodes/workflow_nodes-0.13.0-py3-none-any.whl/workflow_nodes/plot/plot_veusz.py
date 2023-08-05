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
import os
import subprocess
import sys

from xmlhelpy import option

from .main import plot


@plot.command()
@option(
    "pathfile",
    char="i",
    required=True,
    description="Name of the inputfile including import path to the file, header"
    " has to start with 'descriptor'",
)
@option(
    "plotoutput",
    char="p",
    required=True,
    default=None,
    description="Resulting plot, the format is controlled by file extension:"
    " *.bmp, *.eps, *.jpg, *.pdf, *.png *.svg, *.tiff, *.xpm",
)
@option(
    "columns",
    char="u",
    required=False,
    description="Specified columns from input file to be printed, e.g. -u 2:3",
)
@option(
    "output",
    char="o",
    required=False,
    description="Text file with Veusz commands, that can be used for reopening wit"
    " the Veusz GUI.",
)
@option(
    "parameter_x",
    char="x",
    required=False,
    default=None,
    description="Parameter for the x axis",
)
@option(
    "parameter_y",
    char="y",
    required=False,
    default=None,
    description="Parameter for the y axis",
)
@option(
    "keylabel",
    char="l",
    required=False,
    default=None,
    description="Key label for the curve",
)
@option(
    "font",
    char="s",
    required=False,
    default="cmr10",
    description="Font for axis label, numbers and key label",
)
def plot_veusz(*args, **kwargs):
    """A Veusz-1.21.1 based node for plotting columns from a text file."""

    pathfile = kwargs["pathfile"]
    output = kwargs["output"]
    columns = kwargs["columns"]
    parameter_x = kwargs["parameter_x"]
    parameter_y = kwargs["parameter_y"]
    keylabel = kwargs["keylabel"]
    plotoutput = kwargs["plotoutput"]
    font = kwargs["font"]

    path_file = os.path.split(pathfile)

    if output is None:
        output = os.path.splitext(plotoutput)[0]

    # Get column names of the specified columns
    new_linearray = []
    with open(pathfile, encoding="utf-8") as textfile:
        headerrow = textfile.readline()
        if headerrow.startswith("descriptor"):
            linearray = headerrow.replace("\t", " ").split(" ")
            for entry in linearray:
                if len(entry) == 0 or entry == "\n":
                    continue
                new_linearray.append(entry)
        else:
            sys.exit(
                "Header row of the inputfile has to start with descriptor;"
                " use the 'FileConverter' node."
            )
        textfile.close()

    if columns is not None and (parameter_x is None and parameter_y is None):
        columnname_x = new_linearray[int(columns[0])]
        columnname_x = columnname_x.strip()
        columnname_y = new_linearray[int(columns[2])]
        columnname_y = columnname_y.strip()
    elif columns is None and (parameter_x is not None and parameter_y is not None):
        if parameter_x in new_linearray:
            columnname_x = parameter_x.strip()
        else:
            print(
                f"Specified x parameter: {parameter_x} has not been found in"
                " the inputfile columns:"
            )
            print(new_linearray)
            sys.exit(1)

        if parameter_y in new_linearray:
            columnname_y = parameter_y.strip()
        else:
            print(
                f"Specified y parameter: {parameter_y} has not been found in the"
                " inputfile columns:"
            )
            print(new_linearray)
            sys.exit(1)
    else:
        sys.exit(" Either columns (-u) OR x,y column name have to be specified")

    with open(f"{output}.vsz", mode="w", encoding="utf-8") as f:
        f.write(f"AddImportPath(u'{path_file[0]}')\n")
        f.write(f"ImportFile(u'{path_file[1]}', u'', ignoretext=True, linked=True)\n")
        f.write(
            "Set('StyleSheet/axis/Label/offset', u'4pt')\n"
            "Set('StyleSheet/axis/TickLabels/offset', u'4pt')\n"
        )
        if font != "cmr10":
            f.write(f"Set('StyleSheet/Font/font', u'{font}')\n")

        f.write(
            "Add('page', name='page1', autoadd=False)\n"
            "To('page1')\n"
            "Set('height', u'11cm')\n"
            "Add('grid', name='grid1', autoadd=False)\n"
            "To('grid1')\n"
            "Set('leftMargin', '1.5cm')\n"
            "Set('rightMargin', '0.5cm')\n"
            "Set('topMargin', '0.5cm')\n"
            "Set('bottomMargin', '0cm')\n"
            "Add('graph', name='graph1', autoadd=False)\n"
            "To('graph1')\n"
            "Add('axis', name='x', autoadd=False)\n"
            "To('x')\n"
        )
        f.write(f"Set('label', u'{columnname_x}')\n")
        f.write(
            "Set('autoRange', u'+2%')\n"
            "To('..')\n"
            "Add('axis', name='y', autoadd=False)\n"
            "To('y')\n"
        )
        f.write(f"Set('label', u'{columnname_y}')\n")
        f.write(
            "Set('autoRange', u'+2%')\n"
            "Set('direction', 'vertical')\n"
            "To('..')\n"
            "Add('xy', name='xy1', autoadd=False)\n"
            "To('xy1')\n"
        )
        f.write(f"Set('xData', u'{columnname_x}')\n")
        f.write(f"Set('yData', u'{columnname_y}')\n")

        if keylabel is not None:
            f.write(f"Set('key', u'{keylabel}')\n")
            f.write(
                "To('..')\n"
                "Add('key', name='key1', autoadd=False)\n"
                "To('key1')\n"
                "Set('title', u'')\n"
                "To('..')\n"
            )
        f.write("To('..')\n" "To('..')\n")

        # Export plot and finish script; Last two commands should be removed,
        # if the Veusz-GUI wants to be used
        f.write(f'Export("{plotoutput}")\n')
        f.write("Quit()\n")
    f.close()

    # Execute veusz without GUI
    with open(f"{output}.vsz", encoding="utf-8") as f:
        subprocess.call(["veusz", "--listen", "--quiet"], stdin=f)

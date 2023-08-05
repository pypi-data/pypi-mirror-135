import sys

import pandas as pd
from xmlhelpy import Choice
from xmlhelpy import option

from .main import converter


def _read_csv(input_file, separator, header=True):
    df = pd.read_csv(input_file, sep=separator)
    return df


def _write_csv(output_data, output_file, header=True):
    output_data.to_csv(output_file, index=False, header=True, sep=",", na_rep="NaN")
    return output_file


def _write_tsv(output_data, output_file, header=True):
    output_data.to_csv(output_file, index=False, header=True, sep="\t", na_rep="NaN")
    return output_file


def _write_veusz(output_data, output_file, header=True):
    if "#" in output_data.columns[0]:
        tmp = []
        tmp.append("descriptor " + output_data.columns[0].split("#")[1])
        for i in range(1, len(output_data.columns)):
            tmp.append(output_data.columns[i])
    else:
        tmp = []
        tmp.append("descriptor " + output_data.columns[0])
        for i in range(1, len(output_data.columns)):
            tmp.append(output_data.columns[i])
    output_data.columns = tmp
    output_data.to_csv(output_file, index=False, header=True, sep="\t", na_rep="NaN")
    return output_file


def _write_json(output_data, output_file, header=True):
    if "#" in output_data.columns[0]:
        tmp = []
        tmp.append(output_data.columns[0].split("#")[1])
        for i in range(1, len(output_data.columns)):
            tmp.append(output_data.columns[i])
        output_data.columns = tmp
    output_data.to_json(output_file, indent=4)
    return output_file


@converter.command()
@option(
    "inputfile",
    char="i",
    required=True,
    description="Inputfile with extension (dat, csv)",
)
@option(
    "outputfile",
    char="o",
    required=True,
    description="Outputfile with extension (dat, csv, veusz_in, json, hdf5)",
)
@option(
    "separator",
    char="s",
    description="Columns separator for the inputfile",
    default="space",
    param_type=Choice(["space", "tab", "comma"]),
)
@option(
    "c_size",
    char="c",
    description="Chunk size in rows for reading in a big csv (dat) file, "
    "only supported for writing to HDF5",
    default=None,
)
def file_converter(*args, **kwargs):
    """Node for converting from various input formats into various output formats."""

    inputfile = kwargs["inputfile"]
    outputfile = kwargs["outputfile"]
    separator = kwargs["separator"]
    c_size = kwargs["c_size"]

    if separator == "tab":
        separator = "\t"
    elif separator == "space":
        separator = r"\s+"
    else:
        separator = ","

    ext_in = inputfile.split(".")[1]
    ext_out = outputfile.split(".")[1]

    def FileReader(ext, inputfile, separator):
        inputFunctionsDict = {"dat": _read_csv, "csv": _read_csv}
        if ext in inputFunctionsDict:
            return inputFunctionsDict[ext](inputfile, separator, True)
        sys.exit("Input format is not supported")

    def FileWriter(ext, inputfile, outputdata):
        outputFunctionsDict = {
            "csv": _write_csv,
            "dat": _write_tsv,
            "veusz_in": _write_veusz,
            "json": _write_json,
        }
        if ext in outputFunctionsDict:
            return outputFunctionsDict[ext](outputdata, inputfile, True)
        sys.exit("Output format is not supported")

    if c_size is None and ext_out != "hdf5":
        outputData = FileReader(ext_in, inputfile, separator)
        FileWriter(ext_out, outputfile, outputData)
    elif c_size is not None and ext_out == "hdf5":
        c_size = int(c_size)
        reader = pd.read_csv(inputfile, chunksize=c_size, sep=separator)
        with pd.HDFStore(outputfile, mode="w", complevel=9, complib="blosc") as store:
            for chunk in enumerate(reader):
                store.append("table", chunk, index=False)
    elif c_size is None and ext_out == "hdf5":
        sys.exit("For writing to HDF5, a chunk size is needed")
    else:
        sys.exit(
            "Reading and writing big files in chunks "
            "is only supported for the HDF5 output format"
        )

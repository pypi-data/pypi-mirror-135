#!/bin/sh

#
# Build data model files (like jsonschemas, elasticsearch mappings, ui config,...) from the source specification file.
#
# Run this script from the root of your project.
# e.g. ./nr_datasets/datamodels/build.sh
#

cd nr_datasets
models build -c config.json5 datamodels/nr-datasets-v1.0.0.json5

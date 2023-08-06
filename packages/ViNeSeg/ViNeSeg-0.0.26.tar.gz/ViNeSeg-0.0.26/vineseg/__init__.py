# flake8: noqa

import logging
import sys
from pathlib import Path
import json

from qtpy import QT_VERSION


__appname__ = "vineseg"


# Semantic Versioning 2.0.0: https://semver.org/
# 1. MAJOR version when you make incompatible API changes;
# 2. MINOR version when you add functionality in a backwards-compatible manner;
# 3. PATCH version when you make backwards-compatible bug fixes.
__version__ = "0.0.26"

QT4 = QT_VERSION[0] == "4"
QT5 = QT_VERSION[0] == "5"
del QT_VERSION

PY2 = sys.version[0] == "2"
PY3 = sys.version[0] == "3"
del sys

from .label_file import LabelFile
from . import testing
from . import utils

### Model version check
## TODO:
import os
import urllib.request

# check current version
script_dir = os.path.dirname(__file__)
model_path = os.path.join(script_dir, "experiments/")
path = Path(model_path)

model_list = [e for e in path.iterdir() if e.is_dir()]

#version_path = os.path.join(script_dir, "experiments/VERSION")
if model_list:
    print("Currently installed models:")
    for model in model_list:
        print(model)
else:
    print("Found no model locally installed! Download of the default model started.")

    if not os.path.exists(os.path.join(os.path.sep, script_dir, "experiments", "default_model", "trained_weights")):
        os.makedirs(os.path.join(os.path.sep, script_dir, "experiments", "default_model", "trained_weights"))
    if not os.path.exists(os.path.join(os.path.sep, script_dir, "experiments", "default_model", "trained_weights_swa")):
        os.makedirs(os.path.join(os.path.sep, script_dir, "experiments", "default_model", "trained_weights_swa"))

    f = open(model_path + "MANIFEST.json")
    model_dict = json.load(f)

    for model in model_dict["models"]:
        if model["name"] == "default_model":
            default_url = model["url"]


    print("Please wait.")
    print("Retrieving file 1 of 3.")
    urllib.request.urlretrieve(default_url + 'trained_weights/trained_weights.pth', os.path.join(script_dir, "experiments/default_model/trained_weights/trained_weights.pth"))
    print("Retrieving file 2 of 3.")
    urllib.request.urlretrieve(default_url + 'trained_weights_swa/trained_weights.pth', os.path.join(script_dir, "experiments/default_model/trained_weights_swa/trained_weights.pth"))
    print("Retrieving file 3 of 3.")
    urllib.request.urlretrieve(default_url + 'Experiment_parameter.json', os.path.join(script_dir, "experiments/default_model/Experiment_parameter.json"))
    print("Done \nDownloaded the default model.")

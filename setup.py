"""Setup script for anisoms"""

import os.path
from setuptools import setup

cwd = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(cwd, "README.md")) as fh:
    long_desc = fh.read()

setup(
    name="anisoms",
    version="1.0.0",
    author="Pontus Lurcock",
    author_email="pont@talvi.net",
    description="Read AMS (anisotropy of magnetic susceptibility) data",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/pont-us/anisoms",
    classifiers=[
        "License :: OSI Approved :: "
        "GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    packages=["anisoms"],
    install_requires=[
        "numpy", "pyx"
    ],
    entry_points={"console_scripts":
                    ["ams-plot=anisoms.plot:main",
                     "ams-asc-to-csv=anisoms.asc_to_csv:main",
                     "ams-print-ran-tensor=anisoms.print_ran_tensor:main",
                     "ams-tensor-to-dir=anisoms.tensor_to_dir:main",
                     "ams-params-from-asc=anisoms.params_from_asc:main"]
                  },
)

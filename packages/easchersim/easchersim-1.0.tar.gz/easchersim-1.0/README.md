# EASCherSim

![GitLab Release (latest by date)](https://img.shields.io/gitlab/v/release/c4341/easchersim)
[![PyPI](https://img.shields.io/pypi/v/easchersim)](https://pypi.org/project/easchersim/)
[![Conda](https://img.shields.io/conda/v/easchersim/easchersim)](https://anaconda.org/easchersim/easchersim)
[![pipeline status](https://gitlab.com/c4341/easchersim/badges/main/pipeline.svg)](https://gitlab.com/c4341/easchersim/-/commits/main)

This is the release of *EASCherSim*!

This tool simulates the cherenkov light emission for extensive airshowers with trajectories below and above the limb as a full Monte Carlo simulation.
As a result it provides the photon spatial, time and angular distribution at the detection plane. The tool has the option to take the effect of a magnetic field into account.
Various plots can be automatically produced and the results can be saved into root format.

# Installation

`EASCherSim` is available through [pip](https://pypi.org/project/easchersim/) or [conda](https://anaconda.org/easchersim/easchersim).

`python3 -m pip install easchersim`  
`conda install -c easchersim easchersim`

:warning: WARNING: root is **not** a dependency to keep the distribution light

*Note:* We recommand the conda install. This allows to easily install root for creating root output files via  
      `conda install -c conda-forge root`


# Usage

![EASCherSim Use Demo](docs/_static/usage_demo.svg)

### Create a configuration file

The command line simulator uses store simulation settings in an ini file (read by configparser). To
generate a configuration file run the following, with your choice of file name.
All option can be specified via argument as well (see help menu for details).

`easchersim make-config my_config_file.ini`

### Run cherenkov simulation

Simulate cherenkov photons at detection plane

`easchersim run my_config_file.ini`

# Documentation

The sphinx documentation is available at [GitLab](https://c4341.gitlab.io/easchersim/)


### Help Documentation

Use the `-h` flag for documentation.

```
$ easchersim --help
usage: easchersim [OPTIONS] COMMAND [ARGS]

OPTIONS:
  -h, --help         show this help message and exit

COMMANDS:
  {run,make-config}
    run              run easchersim for settings from configuration file
    make-config      Produce configuration file from default and/or given parameters.
```

Help documentation is also available for the commands (run and make-config).

`$  easchersim make-config -h`  
`$  easchersim run -h`
### Uninstall

`python3 -m pip uninstall easchersim`  
`conda uninstall easchersim`

# Download & Build

### Clone the Repository (for development)

1. `git clone https://gitlab.com/c4341/easchersim.git`
2. `cd easchersim`
3. `python3 -m pip install -e .`

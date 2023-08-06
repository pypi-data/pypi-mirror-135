# LSCSoft-GLUE: the LSCSoft Grid LSC User Environment

LSCSoft-GLUE is a collection of utilities for running data analysis pipelines
for online and offline analysis as well as accessing various grid utilities.

Please refer to the online documentation:

https://lscsoft.docs.ligo.org/glue/

GLUE is distributed under the GNU General Public License, version 3 (or later).
See the file `LICENSE` for more information.

## Installation

### Conda

LSCSoft-GLUE is available from conda-forge as
[`lscsoft-glue`](https://anaconda.org/conda-forge/lscsoft-glue/);
to install:

```shell
conda install -c conda-forge lscsoft-glue
```

### Debian Linux

LSCSoft-GLUE is distributed for Debian in the
[LSCSoft Debian Repositories](https://computing.docs.ligo.org/guide/software/installation/#lscdebian)
for Debian 10 (Buster) and Debian 11 (Bullseye); to install:

```shell
apt-get install lscsoft-glue-utils
```

for the full Python 3 library and scripts, or

```shell
apt-get install python3-lscsoft-glue
```

to install only the Python 3 library.

### Enterprise Linux

LSCSoft-GLUE is distributed for Enterprise Linux in the LSCSoft
[EL7](https://computing.docs.ligo.org/guide/software/installation/#sl7) and
[EL8](https://computing.docs.ligo.org/guide/software/installation/#el8)
repositories; to install:

```shell
yum install lscsoft-glue-utils
```

for the full Python 3 library and scripts, or

```shell
apt-get install python3-lscsoft-glue
```

to install only the Python 3 library.

### PyPI

LSCSoft-GLUE is available from PyPI as
[`lscsoft-glue`](https://pypi.org/project/lscsoft-glue);
to install:

```shell
python -m pip install lscsoft-glue
```

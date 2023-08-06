# IPyDrawio Widgets

[![docs][docs-badge]][docs] [![binder-badge][]][binder]
[![install from pypi][pypi-badge]][pypi] [![install from conda-forge][conda-badge]][conda]
[![build][workflow-badge]][workflow] [![coverage][cov-badge]][cov]

> The kernel-side classes for [ipydrawio](https://github.com/deathbeds/ipydrawio).

This package is useful in situations where your JupyterLab client is configured in another
environment than the kernel that might create widgets.

See the [main project repo](https://github.com/deathbeds/ipydrawio) for more
information.

## Installation

> _**Note:** Usually, you'll want the entire `ipydrawio` suite, replacing `ipydrawio-widgets`
> with `ipydrawio`!_

To install just the kernel-side widgets (without any of the front end assets):

```bash
pip install ipydrawio-widgets  # or...
mamba install -c conda-forge ipydrawio-widgets  # or...
conda install -c conda-forge ipydrawio-widgets
```

## Usage

Display a basic diagram:

```python
from ipydrawio_widgets import Diagram

diagram = Diagram()
diagram
```

Update the XML source:

```python
from pathlib import Path
diagram.source.value = Path("a-drawio.dio").read_text()
```

The `.source.value` will always contain the up-to-date XML.

For more, see the documentation

## Open Source

This work is licensed under the [Apache-2.0] License.

```
Copyright 2022 ipydrawio contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

[apache-2.0]:
  https://github.com/deathbeds/ipydrawio/blob/master/py_packages/ipydrawio-widgets/LICENSE.txt
[binder]:
  http://mybinder.org/v2/gh/deathbeds/ipydrawio/master?urlpath=lab/tree/docs/Poster.dio.svg
[binder-badge]: https://mybinder.org/badge_logo.svg
[cov-badge]:
  https://codecov.io/gh/deathbeds/ipydrawio/branch/master/graph/badge.svg?token=9B74VKHQDK
[binder-badge]: https://mybinder.org/badge_logo.svg
[pypi-badge]: https://img.shields.io/pypi/v/ipydrawio-widgets
[pypi]: https://pypi.org/project/ipydrawio-widgets
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/ipydrawio-widgets
[conda]: https://anaconda.org/conda-forge/ipydrawio-widgets
[workflow-badge]:
  https://github.com/deathbeds/ipydrawio/workflows/.github/workflows/ci.yml/badge.svg
[workflow]:
  https://github.com/deathbeds/ipydrawio/actions?query=branch%3Amaster+workflow%3A.github%2Fworkflows%2Fci.yml
[cov-badge]:
  https://codecov.io/gh/deathbeds/ipydrawio/branch/master/graph/badge.svg?token=9B74VKHQDK
[cov]: https://codecov.io/gh/deathbeds/ipydrawio
[docs-badge]: https://readthedocs.org/projects/ipydrawio/badge/?version=latest
[docs]: https://ipydrawio.rtfd.io

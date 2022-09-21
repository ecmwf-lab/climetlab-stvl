## climetlab-stvl

A source plugin for climetlab for the source stvl.


Features
--------

In this README is a description of how to use the source provided by the python package stvl.

## Source description

TODO: write documentation.

## Using climetlab to access the data

See the [demo notebooks](https://github.com/ecmwf-lab/climetlab-stvl/tree/main/notebooks)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecmwf-lab/climetlab-stvl/main?urlpath=lab)


- [demo.ipynb](https://github.com/ecmwf-lab/climetlab-stvl/tree/main/notebooks/demo.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/ecmwf-lab/climetlab-stvl/blob/main/notebooks/demo.ipynb) 
[![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ecmwf-lab/climetlab-stvl/blob/main/notebooks/demo.ipynb) 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ecmwf-lab/climetlab-stvl/main?filepath=notebooks/demo.ipynb)
[<img src="https://deepnote.com/buttons/launch-in-deepnote-small.svg">](https://deepnote.com/launch?name=MyProject&url=https://github.com/ecmwf-lab/climetlab-stvl/tree/main/notebooks/demo.ipynb)


- TODO.


The climetlab python package allows easy access to the data with a few lines of code such as:
``` python

!pip install climetlab climetlab-stvl
import climetlab as cml
ds = cml.load_source("stvl", arg1="1", arg2="2")
ds.to_pandas()
```


Support and contributing
------------------------

Either open a issue on github if this is a github repository, or send an email to email@example.com.

LICENSE
-------

See the LICENSE file.
(C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
This software is licensed under the terms of the Apache Licence Version 2.0
which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
In applying this licence, ECMWF does not waive the privileges and immunities
granted to it by virtue of its status as an intergovernmental organisation
nor does it submit to any jurisdiction.

Authors
-------

Martin Janousek and al.

See also the CONTRIBUTORS.md file.

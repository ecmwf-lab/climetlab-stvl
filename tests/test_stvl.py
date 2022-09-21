#!/usr/bin/env python3
# (C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import climetlab as cml


def test_source():
    import pandas as pd

    reference_datetimes = pd.date_range(
        "2015-12-01 12:00:00", "2015-12-31 12:00:00", freq="1D"
    )
    ds = cml.load_source(
        "stvl",
        parameter="tp",
        reference_datetimes=reference_datetimes,
    )
    df = ds.to_pandas()
    print(len(df))


if __name__ == "__main__":
    test_source()

#!/usr/bin/env python3
# (C) Copyright 2022 European Centre for Medium-Range Weather Forecasts.
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
import logging
import os

import pandas as pd
from climetlab import Source
from climetlab.decorators import alias_argument

LOG = logging.getLogger(__name__)


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "version")
    with open(version_file, "r") as f:
        version = f.readlines()
        version = version[0]
        version = version.strip()
    return version


__version__ = get_version()


class Stvl(Source):
    _cached_df = None

    @alias_argument("parameter", ["param", "variable"])
    def __init__(
        self,
        parameter,
        reference_datetimes,
        obs_period=24,
        table="observation",
        **kwargs,
    ):

        # TODO (in this plugin)
        # the period should not be longer than 100 observation times
        # if you need a longer one, split in by chunks of 100
        self.reference_datetimes = reference_datetimes

        kwargs["table"] = table
        kwargs["parameter"] = parameter
        kwargs["period"] = obs_period * 3600
        kwargs["reference_datetimes"] = self.reference_datetimes

        self.kwargs = kwargs

    @property
    def _dataframe(self):
        # TODO: add cache to climetlab disk. Or is it already done in stvl?
        from ecmp.tools import aligned_geodfs

        if self._cached_df is None:
            from ecmp.media import stvl

            # actual retrieve observations from STVL database
            LOG.debug(
                f"STVL request to the database: retrieve_to_geodfs({self.kwargs})"
            )

            dfs = []
            for df in stvl.retrieve_to_geodfs(**self.kwargs):
                dfs.append(df)

            # Not sure if this could be done after the loop below
            self._cached_df = aligned_geodfs(dfs, max_cluster_size=0.1)

            for reference_datetime, df in zip(self.reference_datetimes, dfs):
                df["reference_datetime"] = reference_datetime

            self._cached_df = pd.concat(dfs)

        return self._cached_df

    def to_pandas(self):
        return self._dataframe

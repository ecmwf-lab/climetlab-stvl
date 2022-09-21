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
from climetlab.core.caching import cache_file
from climetlab.decorators import alias_argument, normalize

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

    # written from https://confluence.ecmwf.int/display/VER/Retrieving+of+STVL+data+using+ecmp+functions

    @alias_argument("parameter", ["param", "variable"])
    @normalize("table", ["observation", "other_valid_table_name"])
    # @normalize("reference_datetimes", "date-list") # need to clarify if these are dates or dates+times
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
        def do_request(target, _):
            from ecmp.media import stvl
            from ecmp.tools import aligned_geodfs

            # actual retrieve observations from STVL database
            LOG.debug(f"STVL request: retrieve_to_geodfs({self.kwargs})")

            dfs = []
            for df in stvl.retrieve_to_geodfs(**self.kwargs):
                dfs.append(df)
            LOG.debug(f"Received {len(dfs)} dataframes.")

            # Not sure if this could be done after the loop below
            dfs = aligned_geodfs(dfs, max_cluster_size=0.1)

            for reference_datetime, df in zip(self.reference_datetimes, dfs):
                df["reference_datetime"] = reference_datetime

            df = pd.concat(dfs)
            df.to_pickle(target)

        # TODO these two lines will be useless with climetlab version >= 0.12
        kwargs = {k: v for k, v in self.kwargs.items()}
        kwargs["reference_datetimes"] = [
            _.isoformat() for _ in kwargs["reference_datetimes"]
        ]

        filename = cache_file("stvl", do_request, self.kwargs, extension=".pickle")
        return pd.read_pickle(filename)

    def to_pandas(self):
        return self._dataframe

from .filter import Filter
import numpy as _np
import pandas as _pd
import datetime


class Column():
    def __init__(self, dataframe, name):
        self._mf = dataframe
        self._name = name

    def _query_value(self, qt, value):

        if isinstance(value, _np.datetime64):
            value = _pd.Timestamp(value).to_pydatetime()

        if self._mf._array_expand and self._name in self._mf.list_columns:
            return {"$elemMatch": {qt: value}}
        return {qt: value}

    def isin(self, array):
        return Filter(self._mf, {self._name: self._query_value("$in", array)}, lambda x: x[self._name].isin(array))

    def __eq__(self, value):
        return Filter(self._mf, {self._name: self._query_value("$eq", value)}, lambda x: x[self._name] == value)

    def __ne__(self, value):
        return Filter(self._mf, {self._name: self._query_value("$ne", value)}, lambda x: x[self._name] != value)

    def __ge__(self, value):
        return Filter(self._mf, {self._name: self._query_value("$gte", value)}, lambda x: x[self._name] >= value)

    def __gt__(self, value):
        return Filter(self._mf, {self._name: self._query_value("$gt", value)}, lambda x: x[self._name] > value)

    def __lt__(self, value):
        return Filter(self._mf, {self._name: self._query_value("$lt", value)}, lambda x: x[self._name] < value)

    def __le__(self, value):
        return Filter(self._mf, {self._name: self._query_value("$lte", value)}, lambda x: x[self._name] <= value)

    def unique(self):

        return _np.array(
            self._mf._collection.distinct(
                self._name,
                self._mf._filter.config
            )
        )

    def agg(self, types):
        if isinstance(types, str):
            types = [types]

        pmap = {
            "mean": "$avg",
            "median": "$avg",
            "min": "$min",
            "max": "$max",
        }

        res = self._mf._collection.aggregate([
            {"$match": self._mf._filter.config},
            {"$group": {
                "_id": None,
                **{t: {pmap[t]: f"${self._name}"} for t in types}
            }}
        ])

        res = list(res)[0]
        res = {k: v for k, v in res.items() if k != "_id"}

        return _pd.Series(res, name=self._name)

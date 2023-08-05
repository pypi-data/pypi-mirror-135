import pandas as pd
from terality_serde import StructType

from . import ClassMethod, Struct
from .structure import StructIterator


class ClassMethodSeries(ClassMethod):
    _class_name: StructType = StructType.SERIES
    _pandas_class = pd.Series
    _additional_class_methods = ClassMethod._additional_class_methods | {
        "random",
        "random_integers",
    }


class Series(Struct, metaclass=ClassMethodSeries):
    _pandas_class_instance = pd.Series(dtype="float64")
    _accessors = {"str", "dt"}
    _additional_methods = Struct._additional_methods | {"get_range_auto", "random"}

    def __iter__(self):
        return StructIterator(self)

    def to_dict(self, into: type = dict):
        pd_series = self._call_method(None, "to_pandas")
        return pd_series.to_dict(into=into)

    def to_list(self):
        pd_series = self._call_method(None, "to_pandas")
        return pd_series.to_list()

    def tolist(self):
        return self.to_list()

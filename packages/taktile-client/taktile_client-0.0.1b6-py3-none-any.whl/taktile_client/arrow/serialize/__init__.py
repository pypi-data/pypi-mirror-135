"""
Arrow serialization
"""
import typing as t
from functools import singledispatch

import numpy as np
import numpy.typing as npt
import pandas as pd  # type: ignore
import pyarrow  # type: ignore

from taktile_client.exceptions import SerializationError

from .dataframe import dataframe_deserialize, dataframe_serialize
from .numpy import numpy_deserialize, numpy_serialize
from .series import series_deserialize, series_serialize

SerialType = t.Union[pyarrow.Table, pyarrow.Array, pyarrow.Tensor]
UserType = t.Union[npt.NDArray[t.Any], pd.Series, pd.DataFrame]


@singledispatch
def serialize(value: UserType) -> SerialType:
    """
    Serialize object for REST

    Parameters
    ----------
    value : t.Union[npt.NDArray[t.Any], pd.Series, pd.DataFrame]
        value to serialize

    Returns
    -------
    str
        serialized object
    """
    raise SerializationError(f"Can't serialize value of type {type(value)}")


@serialize.register
def _serialize_numpy(value: np.ndarray) -> pyarrow.Tensor:  # type: ignore
    return numpy_serialize(value=value)


@serialize.register
def _serialize_series(value: pd.Series) -> pyarrow.Array:
    return series_serialize(value=value)


@serialize.register
def _serialize_dataframe(value: pd.DataFrame) -> pyarrow.Table:
    return dataframe_serialize(value=value)


@singledispatch
def deserialize(
    value: SerialType,
) -> UserType:
    """
    Deserialize value

    Parameters
    ----------
    value : SerialType
        value to deserialize

    Returns
    -------
    UserType
        deserialized object
    """
    raise SerializationError(f"Can't deserialize value of type {type(value)}")


@deserialize.register
def _deserialize_numpy(value: pyarrow.Tensor) -> npt.NDArray[t.Any]:
    return numpy_deserialize(value=value)


@deserialize.register
def _deserialize_series(value: pyarrow.Array) -> pd.Series:
    return series_deserialize(value=value)


@deserialize.register
def _deserialize_dataframe(value: pyarrow.Table) -> pd.DataFrame:
    return dataframe_deserialize(value=value)

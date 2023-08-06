"""
REST serialization
"""
import typing as t
from functools import singledispatch

import numpy as np
import numpy.typing as npt
import pandas as pd  # type: ignore
import pydantic

from taktile_client.exceptions import SerializationError

from .dataframe import (
    dataframe_deserialize,
    dataframe_serialize,
    dataframe_to_example,
)
from .numpy import numpy_deserialize, numpy_serialize, numpy_to_example
from .pydantic_model import pydantic_model_serialize
from .series import series_deserialize, series_serialize, series_to_example
from .utils import JSONStructure


@singledispatch
def serialize(
    value: t.Union[
        npt.NDArray[t.Any], pd.Series, pd.DataFrame, pydantic.BaseModel
    ]
) -> str:
    """
    Serialize object for REST

    Parameters
    ----------
    value : t.Union[
        npt.NDArray[t.Any], pd.Series, pd.DataFrame, pydantic.BaseModel
    ]
        value to serialize

    Returns
    -------
    str
        serialized object
    """
    raise SerializationError(f"Can't serialize value of type {type(value)}")


@serialize.register
def _serialize_numpy(value: np.ndarray) -> str:  # type: ignore
    return numpy_serialize(value=value)


@serialize.register
def _serialize_series(value: pd.Series) -> str:
    return series_serialize(value=value)


@serialize.register
def _serialize_dataframe(value: pd.DataFrame) -> str:
    return dataframe_serialize(value=value)


@serialize.register
def _serialize_pydantic_model(value: pydantic.BaseModel) -> str:
    return pydantic_model_serialize(value=value)


@singledispatch
def deserialize(
    sample: t.Union[npt.NDArray[t.Any], pd.Series, pd.DataFrame],
    *,
    value: JSONStructure,
) -> t.Union[npt.NDArray[t.Any], pd.Series, pd.DataFrame]:
    """
    Deserialize object

    Parameters
    ----------
    sample : InputType
        sample object
    value : JSONStructure
        value to deserialize

    Returns
    -------
    InputType
        deserialized object
    """
    raise SerializationError(f"Can't deserialize value of type {type(sample)}")


@deserialize.register
def _deserialize_numpy(
    sample: np.ndarray, *, value: JSONStructure  # type: ignore
) -> npt.NDArray[t.Any]:
    return numpy_deserialize(value=value, sample=sample)


@deserialize.register
def _deserialize_series(
    sample: pd.Series, *, value: JSONStructure
) -> pd.Series:
    return series_deserialize(value=value, sample=sample)


@deserialize.register
def _deserialize_dataframe(
    sample: pd.DataFrame, *, value: JSONStructure
) -> pd.DataFrame:
    return dataframe_deserialize(value=value, sample=sample)


@singledispatch
def to_example(
    value: t.Union[npt.NDArray[t.Any], pd.Series, pd.DataFrame]
) -> str:
    """
    Produce serialized example of object

    Parameters
    ----------
    value : t.Union[npt.NDArray[t.Any], pd.Series, pd.DataFrame]
        value to produce an example of

    Returns
    -------
    str
        serialized example
    """
    raise SerializationError(
        f"Can't create example value of type {type(value)}"
    )


@to_example.register
def _to_example_numpy(value: np.ndarray) -> str:  # type: ignore
    return numpy_to_example(value=value)


@to_example.register
def _to_example_series(value: pd.Series) -> str:
    return series_to_example(value=value)


@to_example.register
def _to_example_dataframe(value: pd.DataFrame) -> str:
    return dataframe_to_example(value=value)

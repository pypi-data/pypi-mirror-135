"""
Dataframe numpy serialization
"""
import typing as t

import numpy.typing as npt
import pyarrow  # type: ignore


def numpy_deserialize(*, value: pyarrow.Tensor) -> npt.NDArray[t.Any]:
    """
    Deserialize a numpy array

    Parameters
    ----------
    value : pyarrow.Tensor
        value to deserialize

    Returns
    -------
    npt.NDArray[t.Any]
        deserialized numpy array
    """
    return t.cast(npt.NDArray[t.Any], value.to_numpy())


def numpy_serialize(*, value: npt.NDArray[t.Any]) -> pyarrow.Tensor:
    """
    Serialize a numpy array

    Parameters
    ----------
    value : npt.NDArray[t.Any]
        value to serialize

    Returns
    -------
    pyarrow.Tensor
        serialized numpy array
    """
    return pyarrow.Tensor.from_numpy(value)

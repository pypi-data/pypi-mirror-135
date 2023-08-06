"""
Series arrow serialization
"""
import pandas as pd  # type: ignore
import pyarrow  # type: ignore


def series_deserialize(*, value: pyarrow.Array) -> pd.Series:
    """
    Deserialize a series

    Parameters
    ----------
    value : pyarrow.Array
        value to deserialize

    Returns
    -------
    pd.Series
        deserialized series
    """
    return value.to_pandas()


def series_serialize(*, value: pd.Series) -> pyarrow.Array:
    """
    Serialize a Series

    Parameters
    ----------
    value : pd.Series
        value to serialize

    Returns
    -------
    pyarrow.Array
        serialized series
    """
    return pyarrow.Array.from_pandas(value)

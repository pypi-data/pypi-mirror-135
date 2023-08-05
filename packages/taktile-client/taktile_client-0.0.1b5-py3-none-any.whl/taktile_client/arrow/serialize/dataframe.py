"""
Dataframe arrow serialization
"""
import pandas as pd  # type: ignore
import pyarrow  # type: ignore


def dataframe_deserialize(*, value: pyarrow.Table) -> pd.DataFrame:
    """
    Deserialize a dataframe

    Parameters
    ----------
    value : pyarrow.Table
        value to deserialize

    Returns
    -------
    pd.DataFrame
        deserialized dataframe
    """
    return value.to_pandas()


def dataframe_serialize(*, value: pd.DataFrame) -> pyarrow.Table:
    """
    Serialize a dataframe

    Parameters
    ----------
    value : pd.DataFrame
        value to serialize

    Returns
    -------
    pyarrow.Table
        serialized dataframe
    """
    return pyarrow.Table.from_pandas(value, preserve_index=True)

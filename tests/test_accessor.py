import pandas as pd
import pytest

import awkward_pandas


def test_len():
    s = pd.Series(awkward_pandas.AwkwardExtensionArray([[6, 2, 3], [4, 5]]))
    assert s.ak.count() == 5
    s2 = s.ak.count(axis=1)
    assert s2.tolist() == [3, 2]


def test_no_access():
    s = pd.Series([1, 2])
    with pytest.raises(Exception):
        s.ak.count()


def test_getitem():
    s = pd.Series(awkward_pandas.AwkwardExtensionArray([[6, 2, 3], [4, 5]]))
    s2 = s.ak[:, :1]
    assert isinstance(s2, pd.Series)
    assert s2.dtype == "awkward"
    assert s2.tolist() == [[6], [4]]


def test_to_column():
    s = pd.Series(awkward_pandas.AwkwardExtensionArray([6, 2, 3]), name="test")
    s2 = s.ak.to_column()
    assert s2.dtype == "int64"

    s = pd.Series(awkward_pandas.AwkwardExtensionArray(["6", "2", "3"]), name="test")
    s2 = s.ak.to_column()
    assert s2.dtype == "string[pyarrow]"

    s = pd.Series(awkward_pandas.AwkwardExtensionArray([["6", "2", "3"]]), name="test")
    with pytest.raises(ValueError):
        s.ak.to_column()


def test_dir():
    s = pd.Series(awkward_pandas.AwkwardExtensionArray([6, 2, 3]), name="test")
    assert "sum" in dir(s.ak)
    assert "Array" not in dir(s.ak)
    assert "ak_num" not in dir(s.ak)
    assert "_util" not in dir(s.ak)

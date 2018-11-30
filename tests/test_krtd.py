import numpy as np
import pytest
from hypothesis import given
import hypothesis.strategies as st
from skbio import DNA, Sequence

from krtd import krtd

def test_1_mer_rtd_str_no_gap():
    x = krtd("AA", 1)
    assert np.array_equal(x["A"], np.array([0]))

    # by default, non represented k-mers are empty arrays
    assert "T" not in x
    assert "G" not in x
    assert "C" not in x
def test_1_mer_rtd_str_with_gap():
    x = krtd("AATTA", 1)
    assert np.array_equal(x["A"], np.array([0, 2]))
    assert np.array_equal(x["T"], np.array([0]))

    assert "G" not in x
    assert "C" not in x

def test_2_mer_rtd_str_with_gap():
    x = krtd("AATTAAT", 2)
    assert np.array_equal(x["AA"], np.array([3]))
    assert np.array_equal(x["AT"], np.array([3]))

@given(st.text(alphabet=["A", "T", "G", "C"]))
def test_verify_length(seq):
    for letter in ["A", "T", "G", "C"]:
        if letter in seq:
            assert len(krtd(seq, 1)[letter]) == seq.count(letter) - 1 # there are count - 1 k-mer distances


@given(st.text(alphabet=["A", "T", "G", "C"], min_size=3), st.integers(min_value=1, max_value=3))
def test_Sequence_DNA_and_str_equality(seq, k):
    _str = krtd(seq, k)
    _Sequence = krtd(Sequence(seq), k)
    _DNA = krtd(DNA(seq), k)

    for k_mer in _str.keys():
        assert np.array_equal(_str[k_mer], _Sequence[k_mer])
        assert np.array_equal(_str[k_mer], _DNA[k_mer])

@given(st.text(alphabet=["R", "Y", "S", "W", "K", "M", "B", "D", "H", "V"], min_size=3),
       st.integers(min_value=1, max_value=3))
def test_degenerate(seq, k):
    with pytest.raises(ValueError):
        krtd(seq, k)
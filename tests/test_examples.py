"""Example tests demonstrating pytest and hypothesis usage."""

from hypothesis import given, settings
from hypothesis import strategies as st


# =============================================================================
# Basic Unit Tests
# =============================================================================


def test_example_unit_test():
    """Example unit test - replace with real tests."""
    result = 1 + 1
    assert result == 2


def test_string_operations():
    """Example testing string operations."""
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert text.split() == ["hello", "world"]


# =============================================================================
# Property-Based Tests with Hypothesis
# =============================================================================


@given(st.integers(), st.integers())
def test_addition_commutative(a: int, b: int):
    """Property: addition is commutative (a + b == b + a)."""
    assert a + b == b + a


@given(st.integers(), st.integers(), st.integers())
def test_addition_associative(a: int, b: int, c: int):
    """Property: addition is associative ((a + b) + c == a + (b + c))."""
    assert (a + b) + c == a + (b + c)


@given(st.text())
def test_string_reverse_twice(s: str):
    """Property: reversing a string twice gives the original."""
    assert s[::-1][::-1] == s


@given(st.lists(st.integers()))
def test_list_length_after_reverse(lst: list[int]):
    """Property: reversing a list doesn't change its length."""
    assert len(lst[::-1]) == len(lst)


@given(st.lists(st.integers()))
def test_sorted_list_properties(lst: list[int]):
    """Property: sorted list has same length and elements."""
    sorted_lst = sorted(lst)
    assert len(sorted_lst) == len(lst)
    assert set(sorted_lst) == set(lst)
    # Sorted list should be monotonically increasing
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]


@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_dict_keys_values_length(d: dict[str, int]):
    """Property: dict keys and values have same length as dict."""
    assert len(d.keys()) == len(d)
    assert len(d.values()) == len(d)


# =============================================================================
# Hypothesis with Custom Settings
# =============================================================================


@settings(max_examples=200)
@given(st.integers(min_value=0, max_value=1000))
def test_with_custom_settings(n: int):
    """Example with custom hypothesis settings."""
    assert n * 2 >= n


# =============================================================================
# Hypothesis Strategies Examples
# =============================================================================


@given(st.emails())
def test_email_contains_at(email: str):
    """Property: generated emails contain @."""
    assert "@" in email


@given(st.datetimes())
def test_datetime_roundtrip(dt):
    """Property: datetime string roundtrip."""
    from datetime import datetime

    iso_str = dt.isoformat()
    parsed = datetime.fromisoformat(iso_str)
    assert parsed == dt

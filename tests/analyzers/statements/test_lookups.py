import re
import pytest
from beagle.analyzers.statements.lookups import (
    FieldLookup,
    Contains,
    IContains,
    Exact,
    IExact,
    StartsWith,
    EndsWith,
    Regex,
    And,
    Or,
)


@pytest.mark.parametrize(
    "cls,value,prop,result",
    [
        (Contains, "test", "test", True),
        (Contains, "test", "worst", False),
        (Contains, "test", "he is the test", True),
        (Contains, "test", "the test was bad", True),
        (Contains, "test", "the TEST was bad", False),
        (IContains, "test", "TEST", True),
        (IContains, "test", "tEsT", True),
        (IContains, "test", "worst", False),
        # Test we reject null value.
        (IContains, "test", None, False),
        (IContains, "test", "he is the test", True),
        (IContains, "test", "the test was bad", True),
        (Exact, "test", "test", True),
        (Exact, "test", " test ", False),
        (Exact, "test", "some test a", False),
        (IExact, "test", "test", True),
        (IExact, "test", "TEST", True),
        (IExact, "test", "tEst", True),
        (StartsWith, "test", "test", True),
        (StartsWith, "test", "not a test", False),
        (StartsWith, "test", "test is the best", True),
        (EndsWith, "test", "test", True),
        (EndsWith, "test", "not test but a nest", False),
        (EndsWith, "test", "the best test", True),
        (Regex, r"\d", "test 1 test", True),
        (Regex, re.compile(r"\d"), "test 1 test", True),
        (Regex, r"\d", "test test", False),
        (Regex, re.compile(r"\d"), "test test", False),
    ],
)
def test_lookups(cls: FieldLookup, value: str, prop: str, result: str):
    # prop -> value being tested again, value -> the thing we're looking up
    assert cls(value).test(prop) == result


def test_and():
    assert And(StartsWith("foo"), EndsWith("bar")).test("foo bar") is True
    assert And(StartsWith("foo"), EndsWith("bar")).test("foo nar bar") is True
    assert And(StartsWith("foo"), EndsWith("bar")).test("bar foo") is False


def test_or():
    assert Or(StartsWith("foo"), EndsWith("bar")).test("foo bar") is True
    assert Or(StartsWith("foo"), EndsWith("bar")).test("foo") is True
    assert Or(StartsWith("foo"), EndsWith("bar")).test("bar") is True
    assert Or(StartsWith("foo"), EndsWith("bar")).test("foo nar bar") is True
    assert Or(StartsWith("foo"), EndsWith("bar")).test("bar foo") is False
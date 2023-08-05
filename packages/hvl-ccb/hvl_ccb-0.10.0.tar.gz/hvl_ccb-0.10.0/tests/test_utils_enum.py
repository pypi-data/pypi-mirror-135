#  Copyright (c) 2019-2022 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Tests for Enum utils.
"""

import pytest

from hvl_ccb.utils.enum import (
    AutoNumberNameEnum,
    NameEnum,
    StrEnumBase,
    ValueEnum,
    unique,
)


def test_strenumbase():
    @unique
    class E(StrEnumBase):
        A = "a"

    with pytest.raises(NotImplementedError):
        E.A == "a"


def test_valueenum():

    with pytest.raises(ValueError):
        @unique
        class F(ValueEnum):
            A = "a"
            B = "a"

    @unique
    class E(ValueEnum):
        A = "a"
        B = "b"

    a = E("a")
    assert hash(a) == hash(a.value)
    assert a.value == a
    assert a == "a"
    assert str(a) == "a"
    assert a == E.A

    assert E["A"] is a
    with pytest.raises(KeyError):
        E["a"]
    with pytest.raises(KeyError):
        E[a]

    assert a != 0
    assert a != 1

    b = E("b")
    assert hash(b) == hash(b.value)
    assert a != b
    assert a != "b"
    assert a != E.B


def test_nameenum():

    class E(NameEnum):
        _init_ = 'custom_name'
        a = 2
        b = 4

    a = E("a")
    assert hash(a) == hash(a.name)
    assert a.name == a
    assert a == "a"
    assert str(a) == "a"
    assert a == E.a

    assert a != 2
    assert a.custom_name == 2

    assert E["a"] is a
    assert E[a] is a

    b = E("b")
    assert hash(b) == hash(b.name)
    assert a != b
    assert a != "b"
    assert a != E.b


def test_autonumbernameenum():

    class E(AutoNumberNameEnum):
        a = ()
        b = ()

    a = E("a")
    assert hash(a) == hash(a.name)
    assert a.name == a
    assert a == "a"
    assert str(a) == "a"
    assert a == E.a

    assert a != 0
    assert a != 1

    assert E["a"] is a
    assert E[a] is a

    b = E("b")
    assert hash(b) == hash(b.name)
    assert a != b
    assert a != "b"
    assert a != E.b

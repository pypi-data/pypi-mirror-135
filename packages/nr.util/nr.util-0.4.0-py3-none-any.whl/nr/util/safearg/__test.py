
import pytest

from . import Arg, Safe, Unsafe


def test_create_arg():
  with pytest.raises(RuntimeError):
    Arg(31)


def test_create_safe():
  Safe('Hello, World')


def test_create_unsafe():
  Unsafe('TOKEN')
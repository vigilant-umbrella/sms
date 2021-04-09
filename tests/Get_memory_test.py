import core

g = core.Get()


def test_memory():
    assert type(g.memory()) is dict


def test_memory_total():
    assert type(g.memory()['total']) is int


def test_memory_available():
    assert type(g.memory()['available']) is int


def test_memory_used_excl():
    assert type(g.memory()['used_excl']) is int


def test_memory_used_incl():
    assert type(g.memory()['used_incl']) is int


def test_memory_percent():
    assert type(g.memory()['percent']) is float


def test_memory_free():
    assert type(g.memory()['free']) is int

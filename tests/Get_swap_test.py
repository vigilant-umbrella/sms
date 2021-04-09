import core

g = core.Get()


def test_swap():
    assert type(g.swap()) is dict


def test_swap_total():
    assert type(g.swap()['total']) is int


def test_swap_used():
    assert type(g.swap()['used']) is int


def test_swap_free():
    assert type(g.swap()['free']) is int


def test_swap_percent():
    assert type(g.swap()['percent']) is float


def test_swap_sin():
    assert type(g.swap()['sin']) is int


def test_swap_sout():
    assert type(g.swap()['sout']) is int

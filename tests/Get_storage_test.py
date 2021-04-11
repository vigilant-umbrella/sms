import core

g = core.Get()


def test_storage_1():
    assert type(g.storage()) is tuple


def test_storage_2():
    assert len(g.storage()) > 0


def test_storage_3():
    assert type(g.storage()[0]) is dict


def test_storage_device():
    assert type(g.storage()[0]['device']) is str


def test_storage_mountpoint():
    assert type(g.storage()[0]['mountpoint']) is str


def test_storage_fstype():
    assert type(g.storage()[0]['fstype']) is str


def test_storage_options():
    assert type(g.storage()[0]['options']) is str


def test_storage_total():
    assert type(g.storage()[0]['total']) is int


def test_storage_used():
    assert type(g.storage()[0]['used']) is int


def test_storage_free():
    assert type(g.storage()[0]['free']) is int


def test_storage_percent():
    assert type(g.storage()[0]['percent']) is float

import core

g = core.Get()


def test_network_1():
    assert type(g.network()) is tuple


def test_network_2():
    assert len(g.network()) > 0


def test_network_3():
    assert type(g.network()[0]) is dict


def test_network_interface():
    assert type(g.network()[0]['interface']) is str


def test_network_ip():
    assert type(g.network()[0]['ip']) is str


def test_network_bytes_sent():
    assert type(g.network()[0]['bytes_sent']) is int


def test_network_bytes_recv():
    assert type(g.network()[0]['bytes_recv']) is int


def test_network_packets_sent():
    assert type(g.network()[0]['packets_sent']) is int


def test_network_packets_recv():
    assert type(g.network()[0]['packets_recv']) is int


def test_network_errin():
    assert type(g.network()[0]['errin']) is int


def test_network_errout():
    assert type(g.network()[0]['errout']) is int


def test_network_dropin():
    assert type(g.network()[0]['dropin']) is int


def test_network_dropout():
    assert type(g.network()[0]['dropout']) is int

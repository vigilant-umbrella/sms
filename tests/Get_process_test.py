import core

g = core.Get()


def test_process_1():
    assert type(g.process()) is tuple


def test_process_2():
    assert len(g.process()) > 0


def test_process_3():
    assert type(g.process()[0]) is dict


def test_process_pid():
    assert type(g.process()[0]['pid']) is int


def test_process_name():
    assert type(g.process()[0]['name']) is str


def test_process_user():
    assert type(g.process()[0]['user']) is str


def test_process_status():
    assert type(g.process()[0]['status']) is str


def test_process_created():
    assert type(g.process()[0]['created']) is float


def test_process_memory():
    assert type(g.process()[0]['memory']) is float


def test_process_cpu():
    assert type(g.process()[0]['cpu']) is float

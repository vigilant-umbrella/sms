import core

g = core.Get()


def test_cpu():
    assert type(g.cpu()) is dict


def test_cpu_load_avg():
    assert type(g.cpu()['load_avg']) is tuple


def test_cpu_user():
    assert type(g.cpu()['user']) is float


def test_cpu_system():
    assert type(g.cpu()['system']) is float


def test_cpu_idle():
    assert type(g.cpu()['idle']) is float


def test_cpu_iowait():
    assert type(g.cpu()['iowait']) is float


def test_cpu_num_cores():
    assert type(g.cpu()['num_cores']) is int


def test_cpu_cores():
    assert type(g.cpu()['cores']) is tuple

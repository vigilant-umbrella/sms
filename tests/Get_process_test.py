import core

g = core.Get()
process = next(g.process())
print(process)


def test_process():
    assert type(process) is dict


def test_process_pid():
    assert type(process['pid']) is int


def test_process_name():
    assert type(process['name']) is str


def test_process_user():
    assert type(process['user']) is str


def test_process_status():
    assert type(process['status']) is str


def test_process_created():
    assert type(process['created']) is float


def test_process_memory():
    assert type(process['memory']) is float


def test_process_cpu():
    assert type(process['cpu']) is float

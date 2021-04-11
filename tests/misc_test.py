import core

g = core.Get()


def test_os():
    assert type(g.os()) is str


def test_uptime():
    assert type(g.uptime()) is int


if __name__ == '__main__':
    exit()

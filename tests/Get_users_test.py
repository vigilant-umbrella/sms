import core
import datetime

g = core.Get()


def test_users_1():
    assert type(g.users()) is tuple


def test_users_2():
    assert len(g.users()) > 0


def test_users_3():
    assert type(g.users()[0]) is dict


def test_users_name():
    assert type(g.users()[0]['name']) is str


def test_users_sess_started():
    assert type(g.users()[0]['sess_started']) is datetime.datetime


def test_users_host():
    assert type(g.users()[0]['host']) is str

import pytest

from .. import KSComCheck as ks

# testing func readProjectLinks
def test_readProjectLinks_returns_dict():
    projects = ks.readProjectLinks('test_projects.conf')

    assert type(projects) is dict

def test_readProjectLinks_does_not_return_if_empty():
    projects = ks.readProjectLinks('test_doesnotexist.conf')

    assert type(projects) is dict
    assert len(projects.keys()) == 0


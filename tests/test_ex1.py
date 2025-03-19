import pytest
@pytest.mark.skip
def test_example():
    assert 1==1

@pytest.mark.xfail
def test_example():
    assert 2==5

@pytest.mark.slow
def test_example():
    assert 4==5

def test_example():
    assert 4==4

def test_example():
    assert 4==4

def test_example():
    assert 4==4
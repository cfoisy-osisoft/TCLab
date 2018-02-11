import pytest

from tclab import TCLabModel, TCLab
import os

TRAVIS = "TRAVIS" in os.environ
skip_on_travis = pytest.mark.skipif(TRAVIS,
                                    reason="Can't run this test on Travis")

def test_travis():
    assert "TRAVIS" in os.environ

@pytest.fixture(scope="module",
                params=[TCLab,
                        TCLabModel])
def lab(request):
    if TRAVIS and request.param is TCLab:
        pytest.skip("Can't use real TCLab on Travis")
    a = request.param()
    yield a
    a.close()


@skip_on_travis
def test_constructor_port():
        """Raise RuntimeError for an unrecognized port."""
        print("TRAVIS" in os.environ)
        with pytest.raises(RuntimeError):
            with TCLab(port='nonsense') as a:
                pass


@skip_on_travis
def test_context():
    with TCLab() as _:
        pass


def test_T1(lab):
    assert -10 < lab.T1 < 110


def test_T2(lab):
    assert -10 < lab.T2 < 110

    
def test_P1(lab):
    assert lab.P1 == 200
    lab.P1 = 100
    assert lab.P1 == 100

    
def test_P2(lab):
    assert lab.P2 == 100
    lab.P2 = 200
    assert lab.P2 == 200    


def test_LED(lab):
    assert lab.LED(50) == 50


def settertests(method):
    assert method(-10) == 0
    assert method(50) == 50
    assert method(120) == 100
    assert 0 <= method() <= 100


def test_Q1(lab):
    settertests(lab.Q1)


def test_Q2(lab):
    settertests(lab.Q2)


def test_U1(lab):
    lab.U1 = -10
    assert lab.U1 == 0
    lab.U1 = 50
    assert lab.U1 == 50
    lab.U1 = 120
    assert lab.U1 == 100


def test_U2(lab):
    lab.U2 = -10
    assert lab.U2 == 0
    lab.U2 = 50
    assert lab.U2 == 50
    lab.U2 = 120
    assert lab.U2 == 100


def test_scan(lab):
    lab.Q1(10)
    lab.Q2(20)

    T1, T2, Q1, Q2 = lab.scan()

    assert 0 < T1 < 200
    assert 0 < T2 < 200
    assert Q1 == 10
    assert Q2 == 20
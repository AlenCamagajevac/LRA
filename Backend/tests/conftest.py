from pytest import fixture
from _pytest.monkeypatch import MonkeyPatch


@fixture(scope='session', autouse=True)
def testing_evironemnt():
    monkeypatch = MonkeyPatch()
    monkeypatch.setenv("FLASK_ENV", "testing")
    yield monkeypatch
    monkeypatch.undo()

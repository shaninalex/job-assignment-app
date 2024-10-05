from pkg.settings import Config


def test_config_is_not_none(test_config: Config):
    config_not_none = test_config is not None
    assert config_not_none, "Configuration should not be None"

def test_async_engine(async_engine):
    assert async_engine

def test_async_session(async_session):
    assert async_session
from DASiGraph.app import create_app
from DASiGraph.config import DevConfig, ProdConfig

def test_production_config():
    """Production config."""
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'prod'
    assert not app.config['DEBUG']


def test_default_config():
    app = create_app()
    assert app.config['ENV'] == 'prod'


def test_dev_config():
    """Development config."""
    app = create_app(DevConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG']
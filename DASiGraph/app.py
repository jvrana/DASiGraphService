from flask import Blueprint, Flask
from flask_restful import Api
from DASiGraph.resources.GraphAnalyzer import GraphAnalyzer
from DASiGraph.config import ProdConfig


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(GraphAnalyzer, '/graphanalyzer')

def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    # register_extensions(app)
    register_blueprints(app)
    # register_errorhandlers(app)
    # register_shellcontext(app)
    # register_commands(app)
    return app


def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')
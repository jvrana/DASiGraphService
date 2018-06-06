from marshmallow import Schema, fields, ValidationError, validates
from graph_tool import load_graph
from io import StringIO


class GraphSchema(Schema):

    graph = fields.Method(required=True, load_only=True, deserialize="load_graph")

    def load_graph(self, value):
        stream = StringIO(value)
        try:
            g = load_graph(stream, fmt="graphml")
        except OSError as err:
            raise ValidationError("data is not correctly formatted as graphml (xml)")
        return g


class CostSchema(Schema):

    linear = fields.Float()
    closing = fields.Float()
    total = fields.Float()



class ResultSchema(Schema):
    ["vertex index 1", "vertex index 2", "vertex bp pos 1", "vertex bp pos2",
     "linear cost", "closing_cost", "min_path_length", "total_cost", "djk_path", "djk_pos",
     "djk_path_length",
     "djk_cost", "djk_efficiency", "djk_final_cost"]


class Result(object):

    pass
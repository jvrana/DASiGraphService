import pytest
from webtest.app import AppError
from flask import url_for, jsonify
import os
import graph_tool as gt
import io
from DASiGraph.models.graph import GraphSchema

class TestGraphTool:

    def test_load_graph_from_file(self, here):
        """Should load the graph from the test.graphml file in tests/data/test.graphml"""
        filepath = os.path.abspath(os.path.join(here, 'data', 'test.graphml'))
        fmt = filepath.split('.')[-1].strip()
        with open(filepath, 'rb') as f:
            g = gt.load_graph(f, fmt=fmt)

            # make sure there are vertices
            vertices = list(g.vertices())
            assert len(vertices) > 200

    def test_load_graph_from_stream(self, here):
        """Should load the graph from the test.graphml from bytes"""

        # get bytes from file
        filepath = os.path.join(here, 'data', 'test.graphml')
        fmt = filepath.split('.')[-1].strip()
        with open(filepath, 'rb') as f:
            graph_txt = f.read()

            # create stream from bytes and load graph
            stream = io.BytesIO(graph_txt)
            g = gt.load_graph(stream, fmt=fmt)

            # make sure there are vertices
            vertices = list(g.vertices())
            assert len(vertices) > 200

# class TestGraphModel:
#
#     def test_load(self):
#         schema = GraphSchema()
#         json_data = {}
#         try:
#             graph = schema.load(json_data)
#         except ValidationError as err:
#             pass
#         g = schema.load({})
#         d = schema.dump(g)


class TestApi:

    def test_get_graph(self, testapp):
        resp = testapp.get(url_for('api.graphanalyzer'))
        assert resp.json == {"message": "Hello, World!"}
        assert resp.status_int == 200

    def test_post_graph_empty(self, testapp):
        """Expect a 422 response when sending empty data"""
        resp = testapp.post(url_for('api.graphanalyzer'), {}, expect_errors=True)
        assert resp.status_int == 400

    def test_post_graph_malformed_data(self, testapp):
        """Expect a 400 response when sending malformed data"""
        resp = testapp.post(url_for('api.graphanalyzer'), {"graph": "this is some data"}, expect_errors=True)
        assert resp.status_int == 422

    def test_post_graph_correct(self, testapp, here):
        filepath = os.path.abspath(os.path.join(here, 'data', 'test.graphml'))
        with open(filepath, 'r') as f:
            graph_data = f.read()
        resp = testapp.post(url_for('api.graphanalyzer'), {"graph": graph_data})
        assert resp.status_int == 200

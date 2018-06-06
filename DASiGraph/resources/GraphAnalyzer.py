from flask import request, jsonify
from flask_restful import Resource
from DASiGraph.models.graph import GraphSchema
from DASiGraph.utils import clean_dict
from marshmallow import ValidationError

graph_schema = GraphSchema()

import numpy as np
import graph_tool.all as gt

def efficiency_function(a):
    d = {
        1: 1.0,
        2: 0.9,
        3: 0.75,
        4: 0.5,
        5: 0.3,
        6: 0.1,
    }
    if a in d:
        return d[a]
    else:
        return 0.0


feff = np.vectorize(efficiency_function)

class GraphAnalyzer(Resource):
    def get(self):
        return {"message": "Hello, World!"}

    def post(self):
        json_data = request.form
        if not json_data:
            return {'message': 'No input data provided'}, 400

        try:
            graph = graph_schema.load(json_data)
        except ValidationError as err:
            return {"error": err.message}, 422
        errors = graph.errors

        if len(errors) > 0:
            return {"errors": errors}, 422

        g = graph.data['graph']

        dist_map, gap_map = self.compute_distance_map(g)
        efficiency_map = self.compute_efficiency_map(gap_map)
        # cost_map = np.array(list(dist_map)) / efficiency_map
        cost_array = self.calculate_cost_array(g, dist_map, gap_map)
        cost_array = self.refine_cost_array(g, cost_array)

        labels = ["vertex index 1", "vertex index 2", "vertex bp pos 1", "vertex bp pos2",
                  "linear cost", "closing_cost", "min_path_length", "total_cost", "djk_path", "djk_pos",
                  "djk_path_length",
                  "djk_cost", "djk_efficiency", "djk_final_cost"]

        result = dict(zip(labels, cost_array[0]))
        return {"result": result}

    def compute_distance_map(self, g):
        dist_map = gt.shortest_distance(g, directed=True, return_reached=False, weights=g.edge_properties['weight'])
        gap_map = gt.shortest_distance(g, directed=True)
        return dist_map, gap_map

    def compute_efficiency_map(self, gap_map):
        # add one because this doesn't take into account the closing gap
        num_frag_map = (np.array(list(gap_map)) + 1) / 2.0
        efficiency_map = feff(num_frag_map)
        return efficiency_map

    def cost_of_path(self, graph, path):
        w = graph.edge_properties['weight']
        pairs = list(zip(path[:-1], path[1:]))
        pairs.append([path[-1], path[0]])
        edges = [graph.edge(x, y) for x, y in pairs]
        weights = [w[e] for e in edges]
        return sum(weights)

    def calculate_cost_array(self, g, cost_map, gap_map):
        cost_array = []
        x = g.vertex_properties['x']
        for e in g.edges():
            tp = g.edge_properties['type'][e]
            if tp == "closing_gap":
                x1 = x[e.source()]
                x2 = x[e.target()]

                i1 = g.vertex_index[e.source()]
                i2 = g.vertex_index[e.target()]
                closing_cost = g.edge_properties['weight'][e]
                linear_cost = cost_map[i2][i1]
                path_length = gap_map[i2][i1] + 1
                total_cost = linear_cost + closing_cost
                d = [i2, i1, x2, x1, linear_cost, closing_cost, path_length, total_cost]
                cost_array.append(d)
        cost_array = np.array(cost_array)
        args = cost_array.T[7].argsort()
        return cost_array[args]

    def refine_cost_array(self, g, cost_array, num=100):
        final_cost_array = []
        for data in cost_array[:num]:
            v1 = data[0]
            v2 = data[1]
            paths = list(gt.all_shortest_paths(g, v1, v2, weights=g.edge_properties['weight']))
            paths = sorted(paths, key=lambda x: len(list(x)))
            path = paths[0]
            djk_path = [int(x) for x in path]
            djk_pos = [g.vertex_properties['x'][v] for v in djk_path]
            djk_path_length = len(path)
            djk_cost = self.cost_of_path(g, path)
            djk_efficiency = float(feff(djk_path_length / 2.0))
            djk_final_cost = float(djk_cost / djk_efficiency)
            d = [djk_path, djk_pos, djk_path_length, djk_cost, djk_efficiency, djk_final_cost]
            final_cost_array.append(np.concatenate((data, d)))
        # data_copy = data[:]
        #         data_copy = data_copy + d
        #         final_cost_array.append(data_copy)
        final_cost_array = np.array(final_cost_array)
        args = final_cost_array.T[-1].argsort()
        final_cost_array = final_cost_array[args]
        return final_cost_array


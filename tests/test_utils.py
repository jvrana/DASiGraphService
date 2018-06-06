from DASiGraph.utils import clean_dict
import numpy as np

def test_clean_dict():

    data = {
        'a': np.array([1,2,3]),
        'b': '5',
        'c': '5.32',
        'd': '5.4.3'
    }

    cleaned = clean_dict(data)
    expected = {
        'a': [1,2,3],
        'b': 5,
        'c': 5.32,
        'd': '5.4.3'
    }

    assert cleaned == expected
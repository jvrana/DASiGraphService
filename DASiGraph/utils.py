from numpy import ndarray


def clean_dict(data, in_place=False):
    if type(data) is dict:
        if not in_place:
            data = dict(data)
        for k, v in data.items():
            data[k] = clean_dict(v)

    else:
        # try int
        try:
            return int(data)
        except ValueError:
            pass
        except TypeError:
            pass

        # try float
        try:
            return float(data)
        except TypeError:
            pass
        except ValueError:
            pass

        # try list
        if type(data) is ndarray:
            return list(data)

    return data

def flatten_dict(d: dict, parent: str = None) -> dict:
    r = {}
    for k, v in d.items():
        if isinstance(v, dict):
            kp = k if parent is None else parent + '.' + k
            r.update(flatten_dict(v, kp))
        else:
            if parent is None:
                r[k] = v
            else:
                r[f'{parent}.{k}'] = v
    return r

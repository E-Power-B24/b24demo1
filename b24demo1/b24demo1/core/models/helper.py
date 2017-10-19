from psycopg2 import extras

update_ignores = ['id', 'created_date', 'created_by', 'last_modified', 'last_modified_by', 'is_active']
json_ignores = ['created_date', 'created_by', 'last_modified', 'last_modified_by', 'is_active']


def copy(from_obj, to_obj, ignores=[]):
    """copy all properties from one oject to another object in the same sqlalchemy class.

    :param from_obj: source object that will copy attribue to destination object.

    :param to_obj: destination object tha will copy from source object.

    :param ignores: list of columns that will not override value from source object to destination object.

    """
    for key in [k for k in from_obj.__table__.columns.keys() if k not in ignores]:
        setattr(to_obj, key, getattr(from_obj, key))
    return to_obj


def copyupdate(from_obj, to_obj):
    copy(from_obj, to_obj, ignores=update_ignores)


def from_dict(data, to_cls, ignores=[], defaults={}):
    if (defaults):
        data.update(defaults)
    result = to_cls()
    for key, val in data.iteritems():
        if key in to_cls.__table__.columns.keys() and key not in ignores:
            setattr(result, key, val)
    return result


def from_obj(obj, to_cls, ignores=[], defaults={}):
    if not ignores:
        ignores = []
    result = to_cls()
    copy(obj, result, ignores=ignores)
    for key, val in defaults.iteritems():
        if key in to_cls.__table__.columns.keys():
            setattr(result, key, val)
    return result


def to_dict(obj, ignores=[], defaults={}):
    if not ignores:
        ignores = []
    dict = {key: getattr(obj, key, None) for key in obj.__table__.columns.keys() if key not in ignores}
    if (defaults):
        dict.update(extras)
    return dict;


def get_dict(dic, key, default=None):
    if key not in dic:
        return default
    else:
        return dic[key]

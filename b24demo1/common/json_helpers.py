from decimal import Decimal
from datetime import datetime, date
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


# json.dumps(obj,cls=ExtEncoder)
# json.loads(text,object_pairs_hook=load_with_datetime)

# json encoding support Decimal and SqlAlchemy
class ExtEncoder(json.JSONEncoder):
    def default(self, obj):
        # decimal instance
        if isinstance(obj, Decimal):
            return str(obj)
        # datetime
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")

        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data.__class__, DeclarativeMeta):
                        data = ExtEncoder().encode(data)
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def load_with_datetime(pairs, format='%Y-%m-%d'):
    """Load with dates"""
    d = {}
    for k, v in pairs:
        if isinstance(v, basestring):
            try:
                d[k] = datetime.strptime(v, format).date()
            except ValueError:
                d[k] = v
        else:
            d[k] = v
    return d
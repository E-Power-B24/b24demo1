from b24demo1.core.database import db
from b24demo1.core.models.helper import *
from sqlalchemy import func, desc, asc, and_, or_, not_


class LogicError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """

    def __init__(self, message='', field='', *args, **kwargs):
        self.field = field
        ValueError.__init__(self, message, *args, **kwargs)


class LogicBase(object):
    __classname__ = None;

    # def __init__(self, *args, **kw_args):
    #    self.__classname__ = kw_args['__classname__']

    def new(self):
        result = self.__classname__()
        return result

    def all(self):
        result = db.query(self.__classname__)
        if result.count():
            if hasattr(result[0], 'is_active'):
                result = result.filter_by(is_active=True)
        return result.all()

    def actives(self):
        q = db.query(self.__classname__).filter_by(is_active=True)
        return q

    def search(self, **kwargs):
        # search = kwargs['search'] if 'search' in kwargs else ''
        search = kwargs.get('search') or ''
        q = self.actives()
        if search:
            if hasattr(self.__classname__, 'name') and hasattr(self.__classname__, 'code'):
                q = q.filter(
                    or_(func.lower(self.__classname__.code).like('%' + search.lower() + '%'),
                        func.lower(self.__classname__.name).like('%' + search.lower() + '%')
                        )
                )
            elif hasattr(self.__classname__, 'code'):
                q = q.filter(func.lower(self.__classname__.code).like('%' + search.lower() + '%'))
            elif hasattr(self.__classname__, 'name'):
                q = q.filter(func.lower(self.__classname__.name).like('%' + search.lower() + '%'))
        return q

    def find(self, id, update=False):
        result = db.query(self.__classname__).filter_by(id=id).first()
        return result

    def count(self):
        c = self.actives().count()
        return c

    def add(self, obj):
        db.add(obj)
        db.commit()

    def update(self, obj):
        db.commit()

    def remove(self, obj):
        if hasattr(obj, 'is_active'):
            obj.is_active = False
        else:
            db.remove(obj)
        db.commit()
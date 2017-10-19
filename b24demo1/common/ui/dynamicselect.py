# required 'WTForms'+'Flask-WTF' 
# code customize 
# by : RY Rith
# date : 2016-04-01 

from __future__ import unicode_literals

import operator

from wtforms import widgets
from wtforms.compat import text_type, string_types
from wtforms.fields import SelectFieldBase
from wtforms.validators import ValidationError

try:
    from sqlalchemy.orm.util import identity_key
    has_identity_key = True
except ImportError:
    has_identity_key = False

__all__ = ( 
    'DynamicSelectField',
)

class DynamicSelectField(SelectFieldBase):
    widget = widgets.Select()
     
    def __init__(self, 
                label=None, validators=None,
                query = None, query_factory=None,get_pk=None,get_label=None, 
                allow_blank=False,blank_text='',**kwargs):
        super(DynamicSelectField, self).__init__(label, validators, **kwargs)
        self._object_list = None
        self.query = query  
        self.query_factory = query_factory
        if get_pk is None:
            if not has_identity_key:
                raise Exception('The sqlalchemy identity_key function could not be imported.')
            self.get_pk = get_pk_from_identity
        elif isinstance(get_pk, string_types):
            self.get_pk = operator.attrgetter(get_pk)
        else:
            self.get_pk = get_pk

        if get_label is None:
            self.get_label = lambda x: x
        elif isinstance(get_label, string_types):
            self.get_label = operator.attrgetter(get_label)
        else:
            self.get_label = get_label

        self.allow_blank = allow_blank
        self.blank_text = blank_text

    def _get_object_list(self):
        if self._object_list is None:
            query = self.query or self.query_factory()
            get_pk = self.get_pk
            self._object_list = list((text_type(get_pk(obj)), obj) for obj in query)
        return self._object_list

    def iter_choices(self):
        if self.allow_blank:
            yield ('__None', self.blank_text, self.data is None)

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), pk == self.data)

    def process_data(self, value):
        try:
            self.data = text_type(value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            if self.allow_blank and valuelist[0] == '__None':
                self.data = None
            else:
                self.data = text_type(valuelist[0]) 

    def pre_validate(self, form):
        data = self.data
        if data is not None:
            for pk, obj in self._get_object_list():
                if data == pk:
                    break
            else:
                raise ValidationError(self.gettext('Not a valid choice'))
        elif not self.allow_blank:
            raise ValidationError(self.gettext('Not a valid choice'))

def get_pk_from_identity(obj):
    cls, key = identity_key(instance=obj)
    return ':'.join(text_type(x) for x in key)

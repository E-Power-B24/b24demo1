import sys
import os.path

current_dir = os.path.dirname(os.path.realpath(__file__))
target_dir = "\\".join(current_dir.split("\\")[0:-2])
sys.path.insert(0, target_dir)

from common.compat import OrderedDict, iteritems, itervalues, with_metaclass, text_type, escape

def html_params(**kwargs):
    params = []
    for k, v in sorted(iteritems(kwargs)):
        if k in ('class_', 'class__', 'for_'):
            k = k[:-1]
        elif k.startswith('data_'):
            k = k.replace('_', '-', 1)
        if v is True:
            params.append(k)
        elif v is False:
            pass
        else:
            params.append('%s="%s"' % (text_type(k), escape(text_type(v), quote=True)))
    return ' '.join(params)

class HTMLString(text_type):
    def __html__(self):
        return self

class TableMeta(type):
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls._fields = None

    def __call__(cls, *args, **kwargs):
        if cls._fields is None:
            fields = []
            for name in dir(cls):
                if not name.startswith('_'):
                    field = getattr(cls, name)
                    if hasattr(field, '_creation_counter'):
                        setattr(field,'_id',name)
                        fields.append((name, field))
            fields.sort(key=lambda x: (x[1]._creation_counter, x[0]))
            cls._fields = OrderedDict()
            for field in fields:
                cls._fields[field[0]]=field[1]

        return type.__call__(cls, *args, **kwargs)

class ColumnBase(object):
    _creation_counter = 0

    def __init__(self, *args, **kwargs):
        ColumnBase._creation_counter += 1
        self._creation_counter = ColumnBase._creation_counter

class Column(ColumnBase):

    label = ''
    align = 'left'
    visible = True
    format = ''
    render_kw = {}
    kwargs = {}

    def __init__(self,label='',align='left',visible=True,format='',render_kw={}):
        super(Column, self).__init__()
        self.label = label
        self.align = align
        self.visible = visible
        self.format = format
        self.render_kw = render_kw.copy()

    def value(self,row):
        if hasattr(row,self._id):
            return getattr(row,self._id)
        elif isinstance(row,dict) and self._id in row:
            return row[self._id]
        #elif row:
        #    return str(row)
        else:
            return None

    def render(self,row,tag='td'):
        data = self.value(row)
        if not data:
            data=''
        if not self.visible:
            self.render_kw['style']='display:none;'
        if self.format:
            self.render_kw['format']=format
        result = '<%s %s >%s</%s>'%(tag,html_params(**self.render_kw),data,tag)
        return HTMLString(result)

    def render_header(self,tag='th'):
        if not self.visible:
            self.render_kw['style']='display:none;'
        if self.format:
            self.render_kw['format']=format
        result = '<%s %s >%s</%s>'%(tag,html_params(**self.render_kw),self.label,tag)
        return HTMLString(result)


class CheckColumn(Column):

    def value(self, row):
        return None

    def render(self,row=None,tag='td'):
        result = '<td><input class="checkbox checkth" type="checkbox" name="check"/></td>'
        return HTMLString(result)

    def render_header(self):
        result = '<th><input class="checkbox checktd" type="checkbox" name="check"/></th>'
        return HTMLString(result)
        return self.render(row=self.label,tag='th')

class RowNumberColumn(Column):

    def value(self, row):
        key = "_row_number"
        if hasattr(row,key):
            return getattr(row,key)
        elif  "_row_number" in row:
            return row["_row_number"]
        elif row:
            return row
        else:
            return None

class LamdaColumn(Column):
    def __init__(self, label = '', align = 'left', visible = True, format = '', render_kw = {},get_value=None):
        self.get_value = get_value
        return super(LamdaColumn, self).__init__(label, align, visible, format, render_kw)

    def value(self,row):
        if self.get_value:
            return self.get_value(row)
        else:
            return None

class DateColumn(Column):
    def render(self, row, tag = 'td'):
        return '<td>%s</td>'%self.value(row).strftime('%Y-%m-%d')

class ActionColumn(Column):
    def __init__(self, label="", render_kw={}, endpoint="", modal_content="", hidden_edit=False, hidden_delete=False,hidden_detail=False):
        self.endpoint = endpoint
        self.modal_content = modal_content
        self.hidden_edit = hidden_edit
        self.hidden_delete = hidden_delete
        self.hidden_detail = hidden_detail
        return super(ActionColumn, self).__init__(label, render_kw)

    def render(self, row):
        from flask import url_for

        detail_action = """
                        <a href="{detail_url}" class="btn btn-default btn-sm">Detail</a>
                        """.format(detail_url=url_for(self.endpoint + ":detail", id=row.id)) if not self.hidden_detail else ""

        edit_action = """
                      <a href="{edit_url}" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-pencil"></span></a>
                      """.format(edit_url=url_for(self.endpoint + ":edit", id=row.id)) if not self.hidden_edit else ""
        
        delete_action = """
                      <a href="{delete_url}" class="btn btn-danger btn-sm"><span class="glyphicon glyphicon-trash"></span></a>
                      """.format(delete_url=url_for(self.endpoint + ":delete", id=row.id))

        modal_action = """
                        <button type="button" class="btn btn-default btn-sm" data-toggle="modal" data-target="#{data_target}" title="More Actions">
                            <span class="glyphicon glyphicon-option-horizontal"></span>
                        </button>
                       """.format(data_target="modal-%s" % row.id)
        modal_detail_action = """
                                <a href="{detail_url}" class="btn btn-default btn-block" data-dismiss="modal">Detail</a>
                              """.format(detail_url=url_for(self.endpoint + ":detail", id=row.id))
        modal_edit_action = """
                            <a href="{edit_url}" class="btn btn-default btn-block" data-dismiss="modal">Edit</a>
                            """.format(edit_url=url_for(self.endpoint + ":edit", id=row.id)) if not self.hidden_edit else ""
        modal_delete_action = """
                                <a href="{delete_url}" class="btn btn-danger btn-block" data-dismiss="modal">Delete</a>
                              """.format(delete_url=url_for(self.endpoint + ":delete", id=row.id)) if not self.hidden_delete else ""
        modal = """
                <div id="{modal_id}" class="modal fade text-left" role="dialog">
                    <div class="modal-dialog modal-sm">
                        <div class="modal-content">
                            <div class="modal-header">
                                <button type="button" class="close" data-dismiss="modal">&times;</button>
                                <h4 class="modal-title">{modal_title}</h4>
                                <span>{modal_sub_title}</span>
                            </div>
                            <div class="modal-body">
                                {modal_content}
                                {modal_detail_action}
                                {modal_edit_action}
                                {modal_delete_action}
                            </div>
                        </div>
                    </div>
                </div>
                """.format(modal_id = "modal-%s" % row.id,
                           modal_title = "Actions",
                           modal_sub_title = row,
                           modal_content = self.modal_content + "<hr />" if self.modal_content else self.modal_content,
                           modal_detail_action = modal_detail_action,
                           modal_edit_action = modal_edit_action,
                           modal_delete_action = modal_delete_action)

        return """
                <td class="text-right" style="width:1%;">
                    <div class="btn-group hidden-xs" style="display:flex;float:right;">
                        {detail_action}
                        {edit_action}
                        {delete_action}
                    </div>
                    <div class="btn-group hidden-sm hidden-md hidden-lg">
                        {modal_action_xs}
                    </div>
                    {modal}
                </td>
               """.format(detail_action = detail_action,
                          edit_action = edit_action,
                          delete_action = delete_action,
                          modal_action = modal_action if self.modal_content or not self.hidden_edit or not self.hidden_delete else "",
                          modal_action_xs = modal_action,
                          modal = modal)

class DateTimeColumn(Column):
    def render(self,row, tag = 'td'):
        return '<td>%s</td>'%self.value(row).strftime('%Y-%m-%d %H:%M:%S')

class DecimalColumn(Column):
    def render(self, row, tag = 'td'):
        return '<td class="decimal">%.2f</td>'% self.value(row)


class TableBase(with_metaclass(TableMeta)):
    def __iter__(self):
        return iter(itervalues(self._fields))

    def __contains__(self, name):
        return (name in self._fields)

    def __getitem__(self, name):
        return self._fields[name]

    def __setitem__(self, name, value):
        self._fields[name] = value.bind(form=self, name=name, prefix=self._prefix)

    def __delitem__(self, name):
        del self._fields[name]


    def render_header(self):
        results = ['<tr>']
        for column in itervalues(self._fields):
            results.append(column.render_header())
        results.append('</tr>')
        return HTMLString(''.join(results))

    def render_row(self,row):
        tds=['<tr>']
        for column in itervalues(self._fields):
            tds.append(column.render(row))
        tds.append('</tr>')
        return HTMLString(''.join(tds))

    def render_rows(self,html_tag ='tr'):
        trs =[]
        row_number = 0
        for row in self.data:
            row_number += 1
            try:
                setattr(row,'_row_number',row_number)
            except:
                row['_row_number']=row_number
            trs.append(self.render_row(row))
        if not row_number:
            trs.append('<tr><td colspan="100%">No row found!</td></tr>')
        return HTMLString(''.join(trs))


class Table(TableBase):

    def __init__(self, data = [],render_kw={}):

        if not hasattr(self,'data'):
            self.data  = data

        if not hasattr(self,'render_kw'):
            self.render_kw = render_kw.copy()
from wtforms.widgets import HTMLString, html_params
# from flask.ext.wtf import fields, widgets, TextField
from wtforms import widgets


# Obtained from:
# https://github.com/dpgaspar/Flask-AppBuilder/blob/master/flask_appbuilder/fieldwidgets.py#L5
# Usage: Details can be found on accepted answer in below stackoverflow answer
# http://stackoverflow.com/questions/26821713/how-to-display-a-date-time-field-in-jinja2-template-flask
class DatePickerWidget(object):
    """
    Date Time picker from Eonasdan GitHub
    """
    data_template = ('<div class="input-group date" %(id_text)s>'
                     '<span class="input-group-addon"><i class="fa fa-calendar cursor-hand"></i>'
                     '</span>'
                     '<input class="form-control" data-format="yyyy-MM-dd" %(text)s/>'
                     '</div>'
                     )

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        if not field.data:
            field.data = ""
        template = self.data_template

        return HTMLString(template % {'text': html_params(type='text',
                                      value=field.data,
                                      **kwargs),
                                      # Example: id will be "opening_time_datepicker" for the
                                      # opening_time field in BusinessForm
                                      'id_text': html_params(id=field.id+'_datepicker')
                                      })


class DateTimePickerWidget(object):
    """
    Date Time picker from Eonasdan GitHub
    """
    data_template = (
                     "<div class='input-group date' %(id_text)s>"
                     "<input type='text' class='form-control' />"
                     "<span class='input-group-addon'>"
                     "<span class='glyphicon glyphicon-calendar'></span>"
                     "</span>"
                     "</div>"
                     )

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        if not field.data:
            field.data = ""
        template = self.data_template

        return HTMLString(
                template % {
                    'text': html_params(
                        type='text',
                        value=field.data,
                        **kwargs),
                    # Example: id will be "opening_time_datetimepicker" for the
                    # opening_time field in BusinessForm
                    'id_text': html_params(id=field.id+'_datetimepicker')
                    }
                )


class BS3TextFieldWidget(widgets.TextInput):
    def __call__(self, field, **kwargs):
        kwargs['class'] = u'form-control'
        if field.label:
            kwargs['placeholder'] = field.label.text
        if 'name_' in kwargs:
            field.name = kwargs['name_']
        return super(BS3TextFieldWidget, self).__call__(field, **kwargs)


class BS3TextAreaFieldWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs['class'] = u'form-control'
        kwargs['rows'] = 3
        if field.label:
            kwargs['placeholder'] = field.label.text
        return super(BS3TextAreaFieldWidget, self).__call__(field, **kwargs)


class BS3PasswordFieldWidget(widgets.PasswordInput):
    def __call__(self, field, **kwargs):
        kwargs['class'] = u'form-control'
        if field.label:
            kwargs['placeholder'] = field.label.text
        return super(BS3PasswordFieldWidget, self).__call__(field, **kwargs)


class Select2Widget(widgets.Select):
    extra_classes = None

    def __init__(self, extra_classes=None):
        self.extra_classes = extra_classes
        return super(Select2Widget, self).__init__()

    def __call__(self, field, **kwargs):
        kwargs['class'] = u'my_select2 form-control'
        if self.extra_classes:
            kwargs['class'] = kwargs['class'] + ' ' + self.extra_classes
        kwargs['style'] = u'width:250px'
        kwargs['data-placeholder'] = u'Select Value'
        if 'name_' in kwargs:
            field.name = kwargs['name_']
        return super(Select2Widget, self).__call__(field, **kwargs)


class Select2ManyWidget(widgets.Select):
    extra_classes = None

    def __init__(self, extra_classes=None):
        self.extra_classes = extra_classes
        return super(Select2ManyWidget, self).__init__()

    def __call__(self, field, **kwargs):
        kwargs['class'] = u'my_select2 form-control'
        if self.extra_classes:
            kwargs['class'] = kwargs['class'] + ' ' + self.extra_classes
        kwargs['style'] = u'width:250px'
        kwargs['data-placeholder'] = u'Select Value'
        kwargs['multiple'] = u'true'
        if 'name_' in kwargs:
            field.name = kwargs['name_']
        return super(Select2ManyWidget, self).__call__(field, **kwargs)

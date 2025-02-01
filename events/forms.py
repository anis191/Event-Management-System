from django import forms
from events.models import *

class StyleFormMixin:
    common_class = "border-2 rounded-lg border-gray-300 px-3" 
    def apply_style(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class' : f"{self.common_class} w-full focus:bg-red-50 p-1",
                    'placeholder' : f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    # 'class' : f"{self.common_class} w-full focus:bg-red-50",
                    # 'class': 'text-red border rounded-md p-2 focus:ring focus:ring-blue-500'
                    'class' : self.common_class
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class' : f"{self.common_class} w-full focus:bg-red-50",
                    'placeholder' : f"Enter {field.label.lower()}",
                    'rows' : 4
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : self.common_class
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : self.common_class
                })
            else:
                field.widget.attrs.update({
                    'class' : self.common_class
                })

class EventModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category','assign_to']
        widgets = {
            'date' : forms.SelectDateWidget,
            'time' : forms.TimeInput(attrs={'type': 'time'}),
            'category' : forms.Select,
            'assign_to' : forms.CheckboxSelectMultiple
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style()
# Name: Nichols Hennigar
# Class: CSCI E-33a
# Assigment: Final Project

from django.forms import ModelForm

from .models import Todo, Observation


class TodoForm(ModelForm):
    """
    Form for creating a new todo (Inherits from ModelForm)
    """

    class Meta:
        model = Todo
        # Todo properties that we want to include in the form
        fields = ['type', 'title', 'comment', 'observation', 'peace', 'rescue', ]


    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ObservationForm(ModelForm):
    """
    Form for creating a new observation (Inherits from ModelForm)
    """

    class Meta:
        model = Observation
        # Todo properties that we want to include in the form
        fields = ['type', 'component', 'status', 'procedure', ]


    def __init__(self, *args, **kwargs):
        super(ObservationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

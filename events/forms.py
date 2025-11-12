from django import forms
from django.contrib.auth.models import User
from events.models import Event, Category, RSVP


class StyledFormMixin:
    base_input = (
        "w-full px-4 py-2 mt-1 border border-gray-300 rounded-xl shadow-sm "
        "focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 "
        "transition duration-150 ease-in-out text-sm bg-white"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            placeholder_text = f"Enter {field.label.lower()}"

            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    "class": self.base_input,
                    "placeholder": placeholder_text
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": f"{self.base_input} resize-none",
                    "placeholder": placeholder_text,
                    "rows": 5
                })
            elif isinstance(field.widget, forms.DateInput) or isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs.update({
                    "class": self.base_input,
                    "type": "datetime-local"
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    "class": self.base_input
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "flex flex-col gap-2 mt-2"
                })
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({
                    "class": self.base_input
                })
            else:
                field.widget.attrs.update({
                    "class": self.base_input
                })


# Category Form
class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Category Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


# Event Form
class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'category', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Event Name',
            'description': 'Event Description',
            'date': 'Event Date & Time',
            'location': 'Event Location',
            'category': 'Event Category',
            'image': 'Event Image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


# RSVP Form (Optional)
class RSVPModelForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['user', 'event']
        labels = {
            'user': 'Participant',
            'event': 'Event',
        }

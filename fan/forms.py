from django import forms

class ConsumptionForm(forms.Form):
    start_time = forms.DateTimeField(label='Start Time', input_formats=['%Y-%m-%dT%H:%M:%S'])
    end_time = forms.DateTimeField(label='End Time', input_formats=['%Y-%m-%dT%H:%M:%S'])

from django import forms
from highcharts.models import Fingerprint


class FingerprintForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='File name')
    file = forms.FileField(label='Upload a CSV')

    class Meta:
        model = Fingerprint
        fields = ('title', 'file',)

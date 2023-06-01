from django import forms


class ClassifyTextForm(forms.Form):
    name = forms.CharField(required=False)
    text = forms.CharField(required=True, widget=forms.Textarea)


class ClassifyDocumentForm(forms.Form):
    pass

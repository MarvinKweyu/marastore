from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        label="",
        max_length=80,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Search ..."}),
    )

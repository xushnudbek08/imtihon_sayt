from django import forms

class RegisterStepOneForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Parollar mos emas")
        return cleaned_data

class EmailCodeForm(forms.Form):
    code = forms.CharField(max_length=6)



class UploadTestForm(forms.Form):
    category = forms.CharField(max_length=100)
    file = forms.FileField()



class TimeSelectForm(forms.Form):
    duration = forms.ChoiceField(choices=[
        (30, '30 daqiqa'),
        (60, '1 soat'),
        (80, '1.2 soat'),
    ])
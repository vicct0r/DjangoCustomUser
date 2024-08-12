from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Aluno

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['nome_completo', 'is_funcionario']
        labels = {'username':'Email'}

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.email = self.cleaned_data['username']
            if commit:
                user.save()
            return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['nome_completo', 'is_funcionario']


class AlunoModelForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['curso']
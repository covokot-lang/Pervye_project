from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Material

class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового участника Движения."""
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class UserLoginForm(forms.Form):
    """Форма авторизации."""
    username = forms.CharField(max_length=150, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        return self.cleaned_data

class MaterialForm(forms.ModelForm):
    """Форма отправки пользовательских материалов на модерацию (UGC)."""
    class Meta:
        model = Material
        # Изменено с 'content' на 'text' для точного соответствия вашей модели
        fields = ['title', 'text']
        labels = {
            'title': 'Заголовок материала',
            'text': 'Текст публикации / Статьи',
        }


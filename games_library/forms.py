from django import forms
from .models import Game, Comment, CustomUser
from django.contrib.auth.forms import UserCreationForm
# Importa a classe base para criar formulários de criação de usuário
from django.contrib.auth.models import User
# Importa o modelo User, que é o modelo padrão de usuários do Django
from django.contrib.auth.forms import AuthenticationForm
# Importa a classe base para formulários de autenticação
from django.core.exceptions import ValidationError
# Importa a exceção para validação de dados
from django.core.validators import EmailValidator
# Importa o validador de email padrão
from .validators import validate_common_password, validate_numeric_password
# Importa os validadores personalizados para senhas
from .models import CustomUser  # Importa o modelo CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'price', 'category', 'description', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escreva seu comentário...'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'postal_code', 'region', 'city', 'street', 'street_number', 'cpf', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}))
    display_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de exibição'}))
    address = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}))
    postal_code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}))
    region = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Região'}))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}))
    street = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}))
    street_number = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número da Rua'}))
    cpf = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}))
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'postal_code', 'region', 'city', 'street', 'street_number', 'cpf', 'profile_picture', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("A senha deve conter pelo menos 8 caracteres.")
        return password1

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise ValidationError("Por favor, insira um e-mail válido.")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email
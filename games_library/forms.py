from django import forms
from .models import Game
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

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'price', 'category', 'description', 'image']


class LoginForm(AuthenticationForm):
    # Formulário para autenticação de usuários
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário'})
    )
    # Campo de entrada para o nome de usuário com um texto de placeholder
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )
    # Campo de entrada para a senha com um texto de placeholder

class RegisterForm(UserCreationForm):
    # Formulário para criação de novos usuários
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Seu email'})
    )
    # Campo de entrada para o e-mail com um texto de placeholder
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário'})
    )
    # Campo de entrada para o nome de usuário com um texto de placeholder
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}),
        validators=[validate_common_password, validate_numeric_password]
    )
    # Campo de entrada para a senha com um texto de placeholder e validadores personalizados
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirme a senha'})
    )
    # Campo de entrada para confirmação da senha com um texto de placeholder

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Define o modelo a ser usado e os campos a serem incluídos no formulário

    def clean_password2(self):
        # Valida se as senhas inseridas são iguais
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")
        return password2

    def clean_password1(self):
        # Valida se a senha tem pelo menos 8 caracteres
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("A senha deve conter pelo menos 8 caracteres.")
        return password1
    
    def clean_username(self):
        # Valida se o nome de usuário já está em uso
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean_email(self):
        # Valida se o e-mail é válido e se já está em uso
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise ValidationError("Por favor, insira um e-mail válido.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # Importa o módulo para adicionar mensagens (como sucesso ou erro) que são exibidas para o usuário
from .forms import RegisterForm 
from .models import Game

# View para listar todos os jogos
def home(request):
    games = Game.objects.all()
    return render(request, 'home.html', {'games': games})

def game_list(request):
    games = Game.objects.all()
    return render(request, 'Detalhes_lista/game_list.html', {'games': games})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'Detalhes_lista/game_detail.html', {'game': game})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')  # Redireciona para a página de login ou qualquer outra página

def cadastro(request):
    if request.method == 'POST':
        # Se o método da requisição for POST, cria uma instância do formulário com os dados enviados
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Se o formulário for válido, salva os dados do novo usuário
            form.save()
            # Obtém o nome de usuário do formulário
            username = form.cleaned_data.get('username')
            # Adiciona uma mensagem de sucesso indicando que a conta foi criada
            messages.success(request, f'Conta criada com sucesso para {username}!')
            # Redireciona o usuário para a página de login após o registro
            return redirect('login')
    else:
        # Se o método da requisição não for POST, cria um formulário vazio
        form = RegisterForm()
    # Renderiza a página de registro com o formulário
    return render(request, 'User/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        # Se o método da requisição for POST, cria uma instância do formulário de autenticação com os dados enviados
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Se o formulário for válido, obtém o nome de usuário e a senha
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Autentica o usuário com base no nome de usuário e na senha
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Se o usuário for autenticado com sucesso, faz o login
                login(request, user)
                # Adiciona uma mensagem de sucesso ao usuário
                messages.success(request, f'Bem-vindo, {username}!')
                # Redireciona o usuário para a página principal
                return redirect('home')
            else:
                # Se as credenciais forem inválidas, adiciona uma mensagem de erro
                messages.error(request, 'Credenciais inválidas.')
        else:
            # Se o formulário não for válido, adiciona uma mensagem de erro
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Se o método da requisição não for POST, cria um formulário vazio
        form = AuthenticationForm()
    
    # Renderiza a página de login com o formulário
    return render(request, 'User/login.html', {'form': form})
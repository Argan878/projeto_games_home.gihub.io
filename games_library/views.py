from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # Importa o módulo para adicionar mensagens (como sucesso ou erro) que são exibidas para o usuário
from .forms import CommentForm,CustomUserCreationForm, CustomUserChangeForm  # Certifique-se de que você tem um formulário para editar informações do usuário
from .models import Game, Comment
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')  # Redireciona para o dashboard após a mudança de senha
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'User/change_password.html', {'form': form})

@login_required
def user_dashboard(request):
    user = request.user  # Obtém o usuário autenticado
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações atualizadas com sucesso!')
            return redirect('user_dashboard')  # Redireciona para a mesma página após a atualização
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'User/dashboard.html', {'form': form})


# View para listar todos os jogos
def home(request):
    games = Game.objects.all()
    return render(request, 'home.html', {'games': games})

def game_list(request):
    games = Game.objects.all()
    return render(request, 'Detalhes_lista/game_list.html', {'games': games})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    comments = game.comments.all()
    comment_form = CommentForm()

    # Variável para identificar se o usuário está editando um comentário
    comment_to_edit = None

    # Criar novo comentário
    if request.method == 'POST' and 'new_comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.game = game
            new_comment.user = request.user
            new_comment.save()
            return redirect('game_detail', pk=game.pk)

    # Editar comentário existente
    elif request.method == 'POST' and 'edit_comment' in request.POST:
        comment_to_edit = get_object_or_404(Comment, id=request.POST.get('comment_id'))
        if comment_to_edit.user == request.user:  # Verifica se o usuário é o autor
            comment_form = CommentForm(request.POST, instance=comment_to_edit)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('game_detail', pk=game.pk)
        else:
            return HttpResponseForbidden("Você não tem permissão para editar este comentário.")

    # Excluir comentário existente
    elif request.method == 'POST' and 'delete_comment' in request.POST:
        comment_to_delete = get_object_or_404(Comment, id=request.POST.get('comment_id'))
        if comment_to_delete.user == request.user:  # Verifica se o usuário é o autor
            comment_to_delete.delete()
            return redirect('game_detail', pk=game.pk)
        else:
            return HttpResponseForbidden("Você não tem permissão para excluir este comentário.")

    return render(request, 'Detalhes_lista/game_detail.html', {
        'game': game,
        'comments': comments,
        'comment_form': comment_form,
        'comment_to_edit': comment_to_edit
    })

    

def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('home')  # Redireciona para a página de login ou qualquer outra página

def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso para {user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
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
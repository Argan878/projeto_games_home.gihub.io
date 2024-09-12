from django.core.exceptions import ValidationError
# Importa a classe para lançar exceções de validação

from django.utils.translation import gettext as _
# Importa a função para marcar mensagens de texto para tradução

def validate_common_password(value):
    # Função para validar se a senha é comum
    common_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123']  # Lista de senhas comuns
    # Verifica se a senha fornecida está na lista de senhas comuns
    if value in common_passwords:
        # Se a senha for comum, levanta uma exceção de validação com a mensagem traduzida
        raise ValidationError(_('Essa senha é muito comum.'))

def validate_numeric_password(value):
    # Função para validar se a senha é inteiramente numérica
    if value.isdigit():
        # Se a senha for composta apenas por números, levanta uma exceção de validação com a mensagem traduzida
        raise ValidationError(_('Essa senha é inteiramente numérica.'))
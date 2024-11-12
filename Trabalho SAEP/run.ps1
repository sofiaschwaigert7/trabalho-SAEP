# Nome do script: run.ps1

# Verifica se o ambiente virtual 'venv' existe
if (-not (Test-Path -Path "./venv")) {
    Write-Output "[RUN.PS1] O ambiente virtual 'venv' não foi encontrado. Criando um novo ambiente virtual..."
    python -m venv venv

    # Ativa o ambiente virtual e instala as dependências
    .\venv\Scripts\Activate
    Write-Output "[RUN.PS1] Instalando dependências do requirements.txt..."
    pip install -r requirements.txt
} else {
    # Ativa o ambiente virtual
    Write-Output "[RUN.PS1] Ativando o ambiente virtual 'venv'..."
    .\venv\Scripts\Activate
}

# Verifica se a ativação foi bem-sucedida
if (-not $env:VIRTUAL_ENV) {
    Write-Output "[RUN.PS1] Erro ao ativar o ambiente virtual."
    exit 1
}

# Executa o comando Flask com argumentos passados ao script
Write-Output "[RUN.PS1] Iniciando o servidor Flask..."
flask run @Args

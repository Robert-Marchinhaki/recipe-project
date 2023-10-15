# Projeto de Receitas com Django e Django REST Framework

## Introdução
Este projeto é uma aplicação de receitas construída com Django e Django REST Framework. O objetivo deste guia é ajudá-lo a configurar e executar o projeto em sua máquina local.

### Pré-requisitos
- Python instalado em sua máquina (versão recomendada: Python 3.x).
- Um ambiente virtual (recomendado, mas opcional).
- Visual Studio Code (ou a IDE de sua preferência).

## Clonando o Projeto
Clone o projeto do repositório Git ou faça o download do arquivo ZIP e descompacte-o em seu computador.
git clone https://github.com/Robert-Marchinhaki/recipe-project

## Configurando o Ambiente de Desenvolvimento
1. Instalando Extensão Python no Visual Studio Code
Abra o Visual Studio Code e instale a extensão **Python** (id: ms-python.python).

2. Configurando o Ambiente Virtual
No Windows:
Abra o terminal no Visual Studio Code (ou qualquer terminal de sua escolha).
Crie um ambiente virtual usando o comando:
**python -m venv venv**
Certifique-se de que o Python esteja instalado na sua máquina e configurado nas variáveis de ambiente do Windows.

3. Ative o ambiente virtual:
No Prompt de Comando:
**.\venv\Scripts\Activate.bat**
No PowerShell (habilitar a execução de scripts):
**Set-ExecutionPolicy Unrestricted**
**.\venv\Scripts\Activate.ps1**
Verifique se o interpretador virtual foi detectado pelo Visual Studio Code.

4. Instalando Dependências
No terminal, dentro da pasta do projeto, execute o seguinte comando para instalar as dependências do projeto:
**pip install -r requirements.txt**

5. Configurando o arquivo .env
Faça uma cópia do arquivo **.env-example** e renomeie-o para **.env**. No arquivo .env, **defina a variável DEBUG como 1** para ativar o modo de depuração (usado apenas para desenvolvimento local).

5. Aplicando Migrações
Aplique as migrações para configurar o banco de dados:
**python manage.py migrate**

6. Executando o Projeto
Agora que tudo está configurado, você pode iniciar o servidor de desenvolvimento com o seguinte comando:
**python manage.py runserver**
O servidor será executado em http://127.0.0.1:8000/.
---

## Tecnologias utilizadas
- Testes unitários com Pytest e Unitest
- Testes de integração
- Testes funcionais com selenium e chromedriver
- TDD (Test Driven Development)
- MVC Pattern (MTV no Django)
- ORM
- PostgreSQL
- API


---
Contato
Para dúvidas ou problemas, sinta-se à vontade para entrar em contato:

Autor: Robert Adrian
E-mail: adrianrobert288@gmail.com
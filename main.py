import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os
import re

# Load environment variables from .env file
load_dotenv()

# Replace with your API keys
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        # Testa a conexão com a OpenAI fazendo uma chamada válida.
        response = openai.Model.list()
        print("OpenAI connection succeeded.")
    except Exception as e:
        print("Failed to connect to OpenAI:", e)
    if not DISCORD_TOKEN:
        print("Discord token is missing or invalid.")
    if not OPENAI_API_KEY:
        print("OpenAI API key is missing or invalid.")
    print(f"We have logged in as {bot.user}")

@bot.command(name="help")
async def help_command(ctx):
    """Displays a help message with all commands."""
    help_message = (
        "**Available Commands:**\n"
        "`!help` - Show this help message.\n"
        "`!review <GitHub link>` - Review a GitHub repository for code quality.\n"
        "`!improve <code>` - Suggest improvements for a code snippet."
    )
    await ctx.send(help_message)

@bot.command(name="improve")
async def improve_command(ctx, *, code: str = None):
    """Suggests improvements for a given code snippet."""
    if not code:
        await ctx.send("Please provide a code snippet. Usage: `!improve <code>`")
        return

    try:
        prompt = f"Here is some code:\n```\n{code}\n```\nPlease suggest improvements or optimizations for it."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a programming expert."},
                {"role": "user", "content": prompt},
            ],
        )
        await ctx.send(response["choices"][0]["message"]["content"])
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.event
async def on_message(message):

    print("enviou mensagem")

    if message.author == bot.user:
        print("message")
        return

    if message.content.startswith('review!') or message.content == "review!":
        print("print")
        args = message.content.split(' ')
        if len(args) == 1:
            await message.channel.send("Please provide a GitHub link for review.")
        elif len(args) > 1:
            github_link_regex = re.compile(
                r'^(https?:\/\/)?(www\.)?github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?$'
            )
            if not github_link_regex.match(args[1]):
                await message.channel.send("Invalid GitHub link. Please provide a valid GitHub repository link.")
            review_by_gpt4_response = review_by_gpt4(args[1])
            await message.channel.send(review_by_gpt4_response)

        return

import requests
import base64
import re
import os

def get_all_files(owner, repo, path="", headers=None):
    files = []
    contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if headers is None:
        headers = {'Accept': 'application/vnd.github.v3+json'}
    contents_response = requests.get(contents_url, headers=headers)
    if contents_response.status_code != 200:
        return []
    contents_data = contents_response.json()
    for item in contents_data:
        if item['type'] == 'file':
            files.append(item['path'])
        elif item['type'] == 'dir':
            files.extend(get_all_files(owner, repo, item['path'], headers=headers))
    return files

def review_by_gpt4(github_link):
    try:
        # Extrai o proprietário e o repositório do link
        match = re.match(r'https?://github\.com/([^/]+)/([^/]+)/?', github_link)
        if not match:
            return "Link de repositório GitHub inválido."
        owner, repo = match.groups()

        # Configura os cabeçalhos para a API do GitHub
        headers = {'Accept': 'application/vnd.github.v3+json'}
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'

        # Obtém o conteúdo do README.md
        readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        readme_response = requests.get(readme_url, headers=headers)
        if readme_response.status_code != 200:
            return "Não foi possível obter o README.md do repositório."

        readme_data = readme_response.json()
        readme_content_base64 = readme_data.get('content')
        if not readme_content_base64:
            return "O repositório não contém um README.md válido."
        readme_content = base64.b64decode(readme_content_base64).decode('utf-8')

        # Obtém a lista de arquivos recursivamente
        file_names = get_all_files(owner, repo, headers=headers)

        # Prepara o prompt para o modelo
        system_prompt = (
            "Você é um revisor de código que verifica cada arquivo em um repositório GitHub e indica se eles correspondem ou não ao README.md. "
            "Este sinal é uma resposta binária em markdown, na forma de uma lista de verificação.\n"
            "Por exemplo, se o README.md se refere a uma API e modelo:\n"
            "arquivo | corresponde\n"
            "model.py sim/não\n"
            "main.py sim/não\n"
            "Sempre siga estritamente esta estrutura."
        )

        # Trunca o README se for muito longo
        max_readme_length = 1500
        if len(readme_content) > max_readme_length:
            readme_content = readme_content[:max_readme_length] + "\n... (conteúdo do README.md truncado devido ao comprimento)"

        # Trunca a lista de arquivos se for muito longa
        max_files = 100
        if len(file_names) > max_files:
            file_names = file_names[:max_files]
            file_names.append("... (lista de arquivos truncada devido ao comprimento)")

        user_prompt = (
            f"Aqui está o conteúdo do README.md:\n{readme_content}\n\n"
            f"Aqui está a lista de arquivos no repositório:\n{', '.join(file_names)}\n\n"
            "Por favor, verifique se cada arquivo corresponde ao README.md."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ocorreu um erro ao obter a resposta: {e}"


# Run the bot
bot.run(DISCORD_TOKEN)

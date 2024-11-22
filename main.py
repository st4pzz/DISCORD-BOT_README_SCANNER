import json
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os
import re

import requests
import base64

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Load the JSON file with hardcoded texts
with open("text.json", "r") as file:
    TEXTS = json.load(file)

# Set up Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        # Test connection to OpenAI
        response = openai.Model.list()
        print(TEXTS["on_ready"]["openai_success"])
    except Exception as e:
        print(TEXTS["on_ready"]["openai_fail"].format(error=e))
    if not DISCORD_TOKEN:
        print(TEXTS["on_ready"]["discord_token_missing"])
    if not OPENAI_API_KEY:
        print(TEXTS["on_ready"]["openai_key_missing"])
    print(TEXTS["on_ready"]["logged_in"].format(bot_user=bot.user))

bot.remove_command('help')
@bot.command(name="help")
async def help_command(ctx):
    """Displays a help message with all commands."""
    await ctx.send(TEXTS["commands"]["help"]["message"])

@bot.command(name="improve")
async def suggest_optimizations(ctx):
    try:
        args = ctx.message.content.split(' ')
        if len(args) < 2:
            await ctx.send(TEXTS["commands"]["improve"]["missing_link"])
            return
        
        owner, repo = git_link_val(args[1])
        if not owner or not repo:
            await ctx.send(TEXTS["commands"]["improve"]["invalid_link"])
            return

        headers = {'Accept': 'application/vnd.github.v3+json'}
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'

        file_names = get_all_files(owner, repo, headers=headers)
        max_files = TEXTS["constants"]["max_files"]
        if len(file_names) > max_files:
            file_names = file_names[:max_files]
            file_names.append(TEXTS["commands"]["improve"]["truncated_files"])

        system_prompt = TEXTS["commands"]["improve"]["system_prompt"]
        user_prompt = TEXTS["commands"]["improve"]["user_prompt"].format(file_list=", ".join(file_names))

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        response_content = response["choices"][0]["message"]["content"]
        max_message_length = TEXTS["constants"]["max_message_length"]
        for i in range(0, len(response_content), max_message_length):
            await ctx.send(response_content[i:i + max_message_length])
    except Exception as e:
        await ctx.send(TEXTS["commands"]["improve"]["error"].format(error=e))

@bot.command(name="review")
async def review_repository(ctx):
    try:
        args = ctx.message.content.split(' ')
        if len(args) < 2:
            await ctx.send(TEXTS["commands"]["review"]["missing_link"])
            return

        owner, repo = git_link_val(args[1])
        if not owner or not repo:
            await ctx.send(TEXTS["commands"]["review"]["invalid_link"])
            return
        elif len(args) > 1:
            github_link_regex = re.compile(
                r'^(https?:\/\/)?(www\.)?github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?$'
            )
            if not github_link_regex.match(args[1]):
                await ctx.channel.send(TEXTS["commands"]["review"]["regex_invalid"])
            review_by_gpt4_response = review_by_gpt4(args[1])
            await ctx.channel.send(review_by_gpt4_response)
    except Exception as e:
        await ctx.send(TEXTS["commands"]["review"]["error"].format(error=e))
   
@bot.event
async def on_message(message):

    print("enviou mensagem")

    if message.author == bot.user:
        print("message")
        return
    
    await bot.process_commands(message)

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
        match = re.match(r'https?://github\.com/([^/]+)/([^/]+)/?', github_link)
        if not match:
            return TEXTS["review_by_gpt4"]["invalid_github_link"]
        owner, repo = match.groups()

        headers = {'Accept': 'application/vnd.github.v3+json'}
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if GITHUB_TOKEN:
            headers['Authorization'] = f'token {GITHUB_TOKEN}'

        readme_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        readme_response = requests.get(readme_url, headers=headers)
        if readme_response.status_code != 200:
            return TEXTS["review_by_gpt4"]["readme_fail"]

        readme_data = readme_response.json()
        readme_content_base64 = readme_data.get('content')
        if not readme_content_base64:
            return TEXTS["review_by_gpt4"]["invalid_readme"]
        readme_content = base64.b64decode(readme_content_base64).decode('utf-8')

        file_names = get_all_files(owner, repo, headers=headers)
        max_readme_length = TEXTS["constants"]["max_readme_length"]
        if len(readme_content) > max_readme_length:
            readme_content = readme_content[:max_readme_length] + TEXTS["review_by_gpt4"]["truncated_readme"]

        max_files = TEXTS["constants"]["max_files"]
        if len(file_names) > max_files:
            file_names = file_names[:max_files]
            file_names.append(TEXTS["review_by_gpt4"]["truncated_files"])

        system_prompt = TEXTS["review_by_gpt4"]["system_prompt"]
        user_prompt = TEXTS["review_by_gpt4"]["user_prompt"].format(
            readme_content=readme_content, file_list=", ".join(file_names)
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
        return TEXTS["review_by_gpt4"]["error"].format(error=e)

def git_link_val(github_link):
    match = re.match(r'https?://github\.com/([^/]+)/([^/]+)/?', github_link)
    if not match:
        return None, None
    owner, repo = match.groups()
    return owner, repo

bot.run(DISCORD_TOKEN)

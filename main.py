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
        openai.Engine.list()
        print("OpenAI connection succeeded.")
    except Exception as e:
        print("Failed to connect to OpenAI:", e)
    if not DISCORD_TOKEN:
        print("Discord token is missing or invalid.")
    if not OPENAI_API_KEY:
        print("OpenAI API key is missing or invalid.")
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.content.startswith('review!') or message.content == "review!":
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

def review_by_gpt4(github_link):
    try:
        system_prompt = (
            "You are a Code reviewer that checks each file in a GitHub repository and signals if they match or not the README.md, this signal is a binary markdown answer, in the form of a checklist\n"
            "For instance, if the README.md refers to an API and model\n"
            "file | match\n"
            "model.py yes/no\n"
            "main.py yes/no\n"
            "Always follow this structure strictly."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Review the repository at {github_link}"},
            ],
        )

        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "An error occurred while fetching the response."

# Run the bot
bot.run(DISCORD_TOKEN)

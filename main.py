import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Replace with your API keys
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Enable privileged message content
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def review(ctx, github_link):
    """Command to review a GitHub repository based on the README.md"""
    try:
        # Define the system message to enforce a specific pattern
        system_prompt = (
            "You are a Code reviewer that checks each file in a GitHub repository and signals if they match or not the README.md, this signal is a binary markdown answer, in the form of a checklist\n"
            "For instance, if the README.md refers to an API and model\n"
            "file | match\n"
            "model.py yes/no\n"
            "main.py yes/no\n"
            "Always follow this structure strictly."
        )

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Review the repository at {github_link}"},
            ],
        )

        # Extract and send the response
        reply = response["choices"][0]["message"]["content"]
        await ctx.send(reply)
    except Exception as e:
        await ctx.send("An error occurred while fetching the response.")
        print(e)

# Run the bot
bot.run(DISCORD_TOKEN)

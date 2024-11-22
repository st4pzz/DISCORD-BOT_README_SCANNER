# ChatGPT Code Reviewer Bot  

Welcome to the **ChatGPT Code Reviewer Bot**, a Python-based Discord bot designed to bridge the gap between collaborative coding and accessible, dynamic code insights.

This bot connects seamlessly to OpenAI's ChatGPT API to review and analyze code directly from GitHub links shared in a Discord server.

## Authors

This project is maintained by:

- **Pedro Antônio**
- **Sergio Ramella**

---
## Why Use the ChatGPT Code Reviewer Bot?

### Code Speaks Louder When It's Understood

In the fast-paced world of coding, explanations often fall by the wayside.

- A **2020 survey by Stack Overflow** revealed that poor documentation is one of the **top obstacles for developers**, with nearly **60% of professionals citing it as a significant challenge**. [Read more](https://insights.stackoverflow.com/survey/2020#developer-profile-working-remote)
- Research published by **IEEE Software** highlights that inadequate documentation increases onboarding time and leads to misunderstandings in collaborative environments. [Read more](https://ieeexplore.ieee.org/document/9145199)

By integrating this bot into your Discord server, you can ensure clarity and accessibility in coding projects, helping everyone from beginners to experts work more effectively.

---

### A Home for Coders Everywhere

Discord has become a vibrant hub for:
- Collaborative projects.
- Coding clubs.
- Ethical hacking groups.
- Open source development communities.

According to **Discord’s own statistics**, **30% of its active servers are focused on hobbies like programming and modding**.

These informal teaching and learning spaces are ideal for exploring creative ideas. However, their fast-paced nature often leaves critical code explanations behind. This bot simplifies understanding and participation by:

- Making code insights easily shareable.
- Avoiding clutter in discussion channels.
- Helping newcomers join projects faster.

---

## How It Works

### 1. Share a GitHub Link
Drop a GitHub repository or file link in a designated Discord channel.

### 2. Code Review at Your Fingertips
The bot fetches the code, analyzes it using OpenAI's ChatGPT, and provides:
- **Comments on functionality.**
- **Suggestions for improvement.**
- **Explanations of overall code structure.**

### 3. Engage and Learn
Server members can discuss the reviews in real time, fostering a collaborative and dynamic learning atmosphere.

---

## Why This Matters

Every coder has encountered projects where the **"what"** is clear, but the **"why"** remains a mystery.

- A **GitHub survey** revealed that **documentation gaps are among the most common developer pain points**, even in top-tier open-source projects.
- In communities such as **game modding** or **peer coding groups**, documentation often takes a backseat to rapid iteration and experimentation.

The ChatGPT Code Reviewer Bot solves these issues by:
- Making code more approachable.
- Promoting a culture of shared understanding and learning.

---

## Setup

To set up the ChatGPT Code Reviewer Bot, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/chatgpt-code-reviewer-bot.git
cd chatgpt-code-reviewer-bot
```

### 2. Install Dependencies
Run the following command to install all required Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Add Your API Key
Create a `.env` file in the project directory and include your OpenAI API key and Discord bot token:
```env
OPENAI_API_KEY=your_api_key_here  
DISCORD_BOT_TOKEN=your_discord_bot_token_here  
```

### 4. Run the Bot
To start the bot, execute the following command:
```bash
python main.py  
```

---

## File Structure

Here’s a brief description of the key files in the repository:

- **main.py**: This is the main script that initializes the Discord bot, handles events, and integrates with the OpenAI API.
- **requirements.txt**: A file listing the Python dependencies needed to run the bot. Use `pip install -r requirements.txt` to install them.
- **.env**: A configuration file storing the OpenAI API key and Discord bot token. Ensure this file is securely configured.
- **README.md**: The file you're currently reading, which provides setup instructions and information about the bot.

---

## Features

- **Dynamic Code Reviews**: Instant feedback on GitHub-hosted code.
- **Context-Aware Suggestions**: Comments tailored to the code's intent and structure.
- **Condensed Feedback**: Listing of files described in the readme and if they match their description.

---

## Join the Movement

Let’s create a world where coding isn’t just about solving problems but sharing solutions!

Whether you're debugging a mod, teaching a friend, or brainstorming the next big project, the ChatGPT Code Reviewer Bot is your companion for clarity and collaboration.
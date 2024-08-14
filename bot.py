import discord
from discord.ext import commands
from groq import Groq

# Set up Groq client
groq_client = Groq(api_key="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")

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# System message for the AI
sys_msg = (
    'You are a multi-modal AI voice assistant. Generate the most useful and '
    'factual response possible, carefully considering all previous generated text in your response before '
    'adding new tokens to the response. Use all of the context of this conversation so your response is relevant '
    'to the conversation. Make your responses clear and concise, avoiding any verbosity.'
)

# Dictionary to store conversations for each user
user_conversations = {}

def groq_prompt(user_id, prompt):
    if user_id not in user_conversations:
        user_conversations[user_id] = [{'role': 'system', 'content': sys_msg}]

    convo = user_conversations[user_id]
    convo.append({'role': 'user', 'content': prompt})

    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message
    convo.append(response)

    return response.content

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='chat')
async def chat(ctx, *, message):
    user_id = ctx.author.id
    response = groq_prompt(user_id, message)
    await ctx.send(response)

@bot.command(name='reset')
async def reset(ctx):
    user_id = ctx.author.id
    if user_id in user_conversations:
        del user_conversations[user_id]
        await ctx.send("Your conversation has been reset.")
    else:
        await ctx.send("You don't have an active conversation to reset.")

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual Discord bot token
bot.run('YOUR_DISCORD_BOT_TOKEN')

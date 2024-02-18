import discord
from discord.ext import commands
from openai import OpenAI

# Get tokens from file
with open("tokens.txt", "r") as tokens:
    discord_token = tokens.readline().strip()
    openai_token = tokens.readline().strip()

client = OpenAI(
    api_key=openai_token
)

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Feedback to show bot is running
@bot.event
async def on_ready():
    print(f'Bot is online and running >> {bot.user.name}')


# Welcome message sent whenever a new member joins the server
@bot.event
async def on_member_join(member):
    # Set the welcome channel id here
    welcome_channel_id = 0
    welcome_channel = member.guild.get_channel(welcome_channel_id)

    # Set message and image to be displayed
    welcome_message = f'Welcome {member.mention}'
    gif_url = ''

    if welcome_channel:
        embed = discord.Embed(description=welcome_message)
        embed.set_image(url=gif_url)
        await welcome_channel.send(embed=embed)


# This is a chatgpt API implementation that will answer when the bot is mentioned
@bot.event
async def on_message(message_sent):
    # Ignore messages sent by the bot itself
    if message_sent.author == bot.user:
        return

    # Check if the bot is directly mentioned, ignoring @everyone and role mentions
    if bot.user in message_sent.mentions and not message_sent.mention_everyone and not any(
            role_mention in message_sent.content for role_mention in message_sent.role_mentions
    ):
        # Set the system role message if you want to send any extra content with the user message
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": ""},
                {"role": "user", "content": message_sent.clean_content}  # Use clean_content to strip mentions
            ]
        )

        print("Message sent from user >> " + message_sent.clean_content)
        print("Response from ChatGpt >> " + response.choices[0].message.content)
        # Send the response back to the Discord channel
        await message_sent.channel.send(response.choices[0].message.content)

    # This is necessary for the bot to process commands and messages
    await bot.process_commands(message_sent)


# This is a function used for configuration, the bot repeats whatever was said after its prefix
# Usually leave this commented out
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(bot.command_prefix):
        content = message.content[len(bot.command_prefix):]
        await message.channel.send(content)

    await bot.process_commands(message)


# Run bot
bot.run(discord_token)

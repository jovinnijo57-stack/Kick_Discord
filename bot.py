
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Target channel ID
TARGET_CHANNEL_ID = 1565431693765255208

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Bot connected: {bot.user}")
    print(f"Monitoring channel: {TARGET_CHANNEL_ID}")


@bot.event
async def on_message(message):

    # Ignore bot messages
    if message.author.bot:
        return

    # Ignore direct messages
    if message.guild is None:
        return

    print(
        f"Message received: {message.author} "
        f"in channel {message.channel.id}"
    )

    if message.channel.id == TARGET_CHANNEL_ID:

        # Step 1: Delete the message
        try:
            await message.delete()
            print(f"SUCCESS: Deleted message from {message.author}")

        except discord.Forbidden:
            print("ERROR: Bot does not have Manage Messages permission")

        except discord.HTTPException as e:
            print(f"Message deletion error: {e}")

        # Step 2: Kick the user
        try:
            await message.author.kick(
                reason="Message sent in restricted channel"
            )

            print(f"SUCCESS: Kicked {message.author}")

        except discord.Forbidden:
            print("ERROR: Missing Kick Members permission or role hierarchy issue")

        except discord.HTTPException as e:
            print(f"Kick error: {e}")

    await bot.process_commands(message)


if not TOKEN:
    raise ValueError("DISCORD_TOKEN is missing. Check your .env file.")

bot.run(TOKEN)

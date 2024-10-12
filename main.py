import discord
from discord.ext import commands
import asyncio
import os 
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents.all()
intents.messages = True 
intents.guilds = True

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

def has_role(role_name: str):
    async def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role in ctx.author.roles:
            return True
        else:
            await ctx.send(f"Requirement to use the command not met!")
            return False
    return commands.check(predicate)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def userinfo(ctx, user: discord.User):
    user_id = user.id
    username = user.name
    avatar = user.display_avatar.url
    await ctx.send(f'User found: {user_id} -- {username}\n{avatar}')

@bot.event
async def on_message(message):
    # This is necessary if you want to allow commands to work after on_message
    await bot.process_commands(message)

@bot.command(name="client")
@has_role("RatBot User")
async def new_client(ctx, user: discord.User):
    if user is None:
        await ctx.send("User not found. Please mention a valid user.")
        return
    
    username = user.name
    guild = ctx.guild
    category_name = "Settlers"
    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        await ctx.send(f"Category {category_name} not found.")
        return
        
    existing_channel = discord.utils.get(category.channels, name=username)

    if not existing_channel:
        new_channel = await guild.create_text_channel(username, category=category)
        await new_channel.set_permissions(guild.default_role, view_channel=False)  # Deny access to @everyone
        await new_channel.set_permissions(user, view_channel=True)
        await ctx.send(f"Channel {username} has been created")
    else:
        await ctx.send(f"Channel with that name already exists")

@bot.event
async def on_guild_join(guild):
    role_name="RatBot User"
    permissions = discord.Permissions(permissions=0)
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role is None:
        await guild.create_role(name=role_name, permissions=permissions)
        print(f"Joined {guild.name} and created role {role_name}")

# Run the bot
bot.run(TOKEN)

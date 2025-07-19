from dotenv import load_dotenv
import os
import discord
from discord import app_commands

from task import Task

load_dotenv()
TOKEN = os.getenv('TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
GUILD = discord.Object(id=1302270928943710248) #chat-chat ID

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Test database thingies remove later uwu
task_list = [
    Task(
        name='Vacuum',
        description='Vacuum the living room, kitchen and **stairs**',
        is_completed=False,
        completed_message='Vacuuming is done! :3',
        incomplete_message='Vacuuming is still pending! >:3'
    ),
    Task(
        name='Dishwasher',
        description='Fill or empty the dishwasher',
        is_completed=False,
        completed_message='Needs emptying! :3',
        incomplete_message='Needs filling! >:3'
    )
]

@client.event
async def on_ready():
    tree.copy_global_to(guild=GUILD)
    await tree.sync(guild=GUILD)
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello {message.author.name}!')

@tree.command(
    name="command_test",
    description="meow meow",
    guild=GUILD
)
async def first_command(interaction):
    await interaction.response.send_message("meow meow :3")

@tree.command(
    name="dishwasher_status",
    description="meow meow",
    guild=GUILD
)
async def dishwasher_status(interaction):
    #TODO Check dishwasher status somehow
    await interaction.response.send_message("dishwasher needs filling! >:3")

@tree.command(
    name="task_status",
    description="Get status of a task :33333",
    guild=GUILD,
)
@app_commands.choices(task_name=[app_commands.Choice(name=task.name, value=task.name) for task in task_list])
async def task_status(interaction, task_name: app_commands.Choice[str]):
    task = next((task for task in task_list if task.name == task_name.value), None)
    if task is None:
        await interaction.response.send_message("Task not found.")
        return
    await interaction.response.send_message(task.status())

client.run(TOKEN)
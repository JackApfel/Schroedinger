import subprocess

import discord
from discord.ext import commands
import dotenv
import os
import asyncio



async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    return proc.returncode


def main() -> None:
    dotenv.load_dotenv()
    TOKEN = os.getenv("TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.Bot(intents=intents, command_prefix="/")

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        await client.tree.sync()
        print("Slash-Commands erfolgreich synchronisiert! 🔄")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

    @client.tree.command(name="status", description="Check server status")
    async def status(interaction: discord.Interaction):
        # 3. Discord verlangt innerhalb von 3 Sekunden eine Antwort

        await interaction.response.defer()

        if await run("ping -c 1 192.168.178.56") != 0:
            await interaction.followup.send("🔴 Server läuft NICHT!")
            return
                
        await interaction.followup.send("🟢 Server läuft!")
        return
        
    if TOKEN != None:
        client.run(TOKEN)
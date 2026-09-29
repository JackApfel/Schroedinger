from typing import Literal

import discord
from discord.ext import commands
import dotenv
import os
import asyncio
from mcstatus import JavaServer
import a2s



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
    async def status(interaction: discord.Interaction, game: Literal["Minecraft", "Valheim"]):
        await interaction.response.defer()

        if game == "Minecraft":
            server = JavaServer("192.168.178.56")
            try:
                status = await server.async_status()

                embed = discord.Embed(
                    title="⛏️ Minecraft Server Status",
                    description=f"{status.description}",
                    color=discord.Color.green()
                )
            
                embed.add_field(name="👥 Spieler", value=f"{status.players.online} / {status.players.max}", inline=True)
                embed.add_field(name="⚙️ ModPack", value=f"{status.motd.raw}", inline=True)

            except Exception as e:

                embed = discord.Embed(
                        title="⛏️ Minecraft Server Status",
                        description=f"Server nicht ereichbar",
                        color=discord.Color.red()
                )

            await interaction.followup.send(embed=embed)
            return

        elif game == "Valheim":
            try:
                info = await a2s.ainfo(("192.168.178.56", 2457), timeout=3.0)  # type: ignore

                embed = discord.Embed(
                    title="⚔️ Valheim Server Status",
                    description=f"**{info.server_name}**",
                    color=discord.Color.green()
                )
                embed.add_field(name="👥 Spieler", value=f"{info.player_count} / {info.max_players}", inline=True)
                embed.add_field(name="🗺️ Welt", value=f"{info.map_name}", inline=True)

                print(info)

            except Exception as e:
                print(f"Valheim Status Error: {repr(e)}")

                embed = discord.Embed(
                    title="⚔️ Valheim Server Status",
                    description="Server nicht erreichbar",
                    color=discord.Color.red()
                )


            await interaction.followup.send(embed=embed)
            return
            
        
    if TOKEN != None:
        client.run(TOKEN)
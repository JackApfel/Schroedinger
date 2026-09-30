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
    if TOKEN is None:
        print("Error: Discord Token not found in environment variables.")
        return
    
    HOST_IP = os.getenv("HOST_IP")
    if HOST_IP is None:
        print("Error: Host IP not found in environment variables.")
        return

    


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


    async def check_valheim_server_status() -> discord.Embed:
            try:
                info = await a2s.ainfo(("192.168.178.56", 2457), timeout=3.0)  # type: ignore

                embed = discord.Embed(
                    title="⚔️ Valheim Server Status",
                    description=f"**{info.server_name}**",
                    color=discord.Color.green()
                )
                embed.add_field(name="👥 Spieler", value=f"{info.player_count} / {info.max_players}", inline=True)
                embed.add_field(name="🗺️ Welt", value=f"{info.map_name}", inline=True)
                embed.add_field(name="🧩 Version", value=f"{info.version}", inline=True)
                embed.add_field(name="📡 Ping", value=f"{info.ping * 1000:.0f} ms", inline=True)
                embed.add_field(name="🔒 Passwortschutz", value="Ja" if info.password_protected else "Nein", inline=True)

                print(f"\n\nValheim Status:\n{info}\n\n")

            except Exception as e:
                print(f"Valheim Status Error: {repr(e)}")

                embed = discord.Embed(
                    title="⚔️ Valheim Server Status",
                    description="Server nicht erreichbar",
                    color=discord.Color.red()
                )
            return embed

    async def check_mc_server_status() -> discord.Embed:
            server = JavaServer(HOST_IP)
            try:
                status = await server.async_status()
                print(f"\n\ncheck_mcserver_status:\n{status}ß\n\n")

                modpack = status.raw.get("betterStatus", {})
                modpack_name = modpack.get("name", status.motd.raw)
                modpack_version = modpack.get("version")
                modpack_text = f"{modpack_name} (v{modpack_version})" if modpack_version else modpack_name

                embed = discord.Embed(
                    title="⛏️ Minecraft Server Status",
                    description=f"{status.description}",
                    color=discord.Color.green()
                )
            
                embed.add_field(name="👥 Spieler", value=f"{status.players.online} / {status.players.max}", inline=True)
                embed.add_field(name="⚙️ Modpack", value=modpack_text, inline=True)
                embed.add_field(name="🧱 Minecraft", value=f"{status.version.name}", inline=True)
                embed.add_field(name="📡 Latenz", value=f"{status.latency:.0f} ms", inline=True)

            except Exception as e:

                embed = discord.Embed(
                        title="⛏️ Minecraft Server Status",
                        description=f"Server nicht ereichbar",
                        color=discord.Color.red()
                )

            return embed


    @client.tree.command(name="status", description="Check server status")
    async def status(interaction: discord.Interaction, game: Literal["all","Minecraft", "Valheim"]):
        
        try:
            await interaction.response.defer()
        except discord.NotFound:
            print("Interaction ist abgelaufen oder unbekannt.")
            return

        embeds = []

        if game == "Minecraft" or game == "all":
            embeds.append(await  check_mc_server_status())
            print("Minecraft status command executed")
        if game == "Valheim" or game == "all":
            embeds.append(await check_valheim_server_status())
            print("Valheim status command executed")

        print(f"Anzahl Embeds: {len(embeds)}")
        print(f"Embed-Titel: {[embed.title for embed in embeds]}")

        try:
            await interaction.followup.send(embeds=embeds)
        except Exception as error:
            print(f"Fehler beim Senden der Embeds: {error!r}")
        print("status command executed")

            
        
    if TOKEN != None:
        client.run(TOKEN)



        return

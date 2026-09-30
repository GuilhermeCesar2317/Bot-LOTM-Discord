import os

import discord
from discord import app_commands
from dotenv import load_dotenv

from commands.general import GeneralCommands


# Carrega as variáveis do arquivo .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")


# Intents que o bot utilizará
intents = discord.Intents.default()


class LOTMBot(discord.Client):

    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        # Adiciona o grupo de comandos do RPG
        self.tree.add_command(GeneralCommands())

    async def setup_hook(self):

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))

            # Copia os comandos para o servidor de desenvolvimento
            self.tree.copy_global_to(guild=guild)

            # Sincroniza os comandos no servidor
            await self.tree.sync(guild=guild)

            print("🃏 Comandos sincronizados no servidor de desenvolvimento.")

        else:
            # Caso o ID do servidor não esteja configurado
            await self.tree.sync()

            print("🌐 Comandos sincronizados globalmente.")


bot = LOTMBot()


@bot.tree.command(
    name="ping",
    description="Verifica se o bot está funcionando"
)
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🃏 **PONG!** O mundo espiritual está estável."
    )


if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN não encontrado no arquivo .env!"
    )


bot.run(TOKEN)
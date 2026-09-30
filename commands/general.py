import discord
from discord import app_commands

from systems.pathways import (
    get_all_pathways,
    get_pathway,
    get_sequence
)


async def pathway_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    pathways = get_all_pathways()
    choices = []

    for key, pathway in pathways.items():
        if current.lower() in pathway["nome"].lower():
            choices.append(
                app_commands.Choice(
                    name=pathway["nome"],
                    value=key
                )
            )

    return choices[:25]


async def sequence_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    caminho = interaction.namespace.caminho

    if not caminho:
        return []

    pathway = get_pathway(caminho)

    if pathway is None:
        return []

    choices = []

    for sequence, data in pathway["sequencias"].items():
        nome = data["nome"]

        if current.lower() in nome.lower() or current == sequence:
            choices.append(
                app_commands.Choice(
                    name=f"Sequência {sequence} • {nome}",
                    value=sequence
                )
            )

    return choices[:25]


def format_list(items, prefix="•"):
    """Transforma uma lista em texto formatado."""
    if not items:
        return "Nenhum registro."

    return "\n".join(
        f"{prefix} {item}"
        for item in items
    )


def format_abilities(abilities):
    """Formata as habilidades de uma Sequência."""
    if not abilities:
        return "Nenhuma habilidade registrada."

    linhas = []

    for ability in abilities:
        nome = ability.get("nome", "Habilidade desconhecida")
        tipo = ability.get("tipo", "desconhecido")
        descricao = ability.get(
            "descricao",
            "Sem descrição."
        )

        linhas.append(
            f"**{nome}**\n"
            f"*Tipo: {tipo}*\n"
            f"{descricao}"
        )

    return "\n\n".join(linhas)


class GeneralCommands(app_commands.Group):

    def __init__(self):
        super().__init__(
            name="rpg",
            description="Comandos relacionados ao RPG"
        )

    @app_commands.command(
        name="caminho",
        description="Mostra as informações de um Caminho"
    )
    @app_commands.describe(
        caminho="Nome do Caminho"
    )
    @app_commands.autocomplete(
        caminho=pathway_autocomplete
    )
    async def caminho(
        self,
        interaction: discord.Interaction,
        caminho: str
    ):
        pathway = get_pathway(caminho)

        if pathway is None:
            await interaction.response.send_message(
                f"❌ O Caminho `{caminho}` não foi encontrado."
            )
            return

        sequencias = pathway["sequencias"]

        linhas = []

        for sequence, data in sorted(
            sequencias.items(),
            key=lambda item: int(item[0]),
            reverse=True
        ):
            linhas.append(
                f"**Sequência {sequence}** • {data['nome']}"
            )

        embed = discord.Embed(
            title=f"🔮 {pathway['nome']}",
            description="\n".join(linhas),
            color=discord.Color.dark_purple()
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="sequencia",
        description="Mostra informações de uma Sequência"
    )
    @app_commands.describe(
        caminho="Nome do Caminho",
        sequencia="Escolha uma Sequência"
    )
    @app_commands.autocomplete(
        caminho=pathway_autocomplete,
        sequencia=sequence_autocomplete
    )
    async def sequencia(
        self,
        interaction: discord.Interaction,
        caminho: str,
        sequencia: str
    ):
        sequence = get_sequence(
            caminho,
            sequencia
        )

        if sequence is None:
            await interaction.response.send_message(
                "❌ Caminho ou Sequência não encontrada."
            )
            return

        pathway = get_pathway(caminho)

        # ==============================
        # INFORMAÇÕES BÁSICAS
        # ==============================

        embed = discord.Embed(
            title=(
                f"☠️ {pathway['nome']}"
            ),
            description=(
                f"### Sequência {sequencia} • "
                f"{sequence['nome']}\n\n"
                f"{sequence.get('descricao', 'Sem descrição.')}"
            ),
            color=discord.Color.dark_purple()
        )

        # ==============================
        # HABILIDADES
        # ==============================

        habilidades = sequence.get(
            "habilidades",
            []
        )

        if habilidades:
            embed.add_field(
                name="⚔️ Habilidades",
                value=format_abilities(
                    habilidades
                ),
                inline=False
            )

        # ==============================
        # CARACTERÍSTICAS
        # ==============================

        caracteristicas = sequence.get(
            "caracteristicas",
            []
        )

        if caracteristicas:
            embed.add_field(
                name="🧬 Características",
                value=format_list(
                    caracteristicas
                ),
                inline=False
            )

        # ==============================
        # AUTORIDADES
        # ==============================

        autoridades = sequence.get(
            "autoridades",
            []
        )

        if autoridades:
            embed.add_field(
                name="👑 Autoridades",
                value=format_list(
                    autoridades
                ),
                inline=False
            )

        # ==============================
        # DOMÍNIOS
        # ==============================

        dominios = sequence.get(
            "dominios",
            []
        )

        if dominios:
            embed.add_field(
                name="🌑 Domínios",
                value=format_list(
                    dominios
                ),
                inline=False
            )

        # ==============================
        # ATUAÇÃO
        # ==============================

        atuacao = sequence.get(
            "atuacao",
            {}
        )

        if atuacao:
            descricao_atuacao = atuacao.get(
                "descricao",
                "Sem descrição."
            )

            objetivos = atuacao.get(
                "objetivos",
                []
            )

            texto_atuacao = descricao_atuacao

            if objetivos:
                texto_atuacao += (
                    "\n\n**Objetivos:**\n"
                    + format_list(objetivos)
                )

            embed.add_field(
                name="📜 Atuação",
                value=texto_atuacao,
                inline=False
            )

        # ==============================
        # FÓRMULA
        # ==============================

        formula = sequence.get(
            "formula",
            {}
        )

        ingredientes = formula.get(
            "ingredientes",
            []
        )

        if ingredientes:
            linhas_formula = []

            for ingrediente in ingredientes:
                nome = ingrediente.get(
                    "nome",
                    "Ingrediente desconhecido"
                )

                quantidade = ingrediente.get(
                    "quantidade",
                    "?"
                )

                tipo = ingrediente.get(
                    "tipo",
                    "desconhecido"
                )

                linhas_formula.append(
                    f"• **{nome}** × {quantidade}"
                    f"  *({tipo})*"
                )

            embed.add_field(
                name="🧪 Fórmula da Poção",
                value="\n".join(linhas_formula),
                inline=False
            )

        else:
            embed.add_field(
                name="🧪 Fórmula da Poção",
                value="Não registrada.",
                inline=False
            )

        # ==============================
        # REQUISITOS
        # ==============================

        requisitos = sequence.get(
            "requisitos",
            {}
        )

        sequencia_anterior = requisitos.get(
            "sequencia_anterior"
        )

        if sequencia_anterior is None:
            texto_requisito = (
                "Primeira Sequência do Caminho."
            )
        else:
            texto_requisito = (
                f"Sequência anterior: "
                f"**{sequencia_anterior}**"
            )

        embed.add_field(
            name="📌 Requisitos",
            value=texto_requisito,
            inline=False
        )

        # ==============================
        # RODAPÉ
        # ==============================

        embed.set_footer(
            text=(
                "Sistema RPG • Caminho da Morte"
            )
        )

        await interaction.response.send_message(
            embed=embed
        )
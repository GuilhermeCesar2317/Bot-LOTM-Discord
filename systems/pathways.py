import json
from pathlib import Path


DATA_FILE = Path(__file__).parent.parent / "data" / "pathways.json"


def load_pathways():
    """Carrega os Caminhos a partir do arquivo JSON."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def get_all_pathways():
    """Retorna todos os Caminhos."""
    return load_pathways()

def get_pathway(pathway_name):
    """Retorna um Caminho pelo nome interno."""

    pathways = load_pathways()

    return pathways.get(pathway_name.lower())


def get_sequence(pathway_name, sequence):
    """Retorna uma Sequência específica de um Caminho."""

    pathway = get_pathway(pathway_name)

    if pathway is None:
        return None

    return pathway["sequencias"].get(str(sequence))
from src.simple_discord.objects import Ready
from tests.objects.ready import samples


def test_simple():
    data = samples.example_connect

    obj = Ready()
    obj.ingest_raw_dict(data)
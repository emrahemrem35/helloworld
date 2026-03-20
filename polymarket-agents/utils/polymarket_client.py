from py_clob_client.client import ClobClient
import os


def get_client():
    return ClobClient(
        host="https://clob.polymarket.com",
        key=os.getenv("POLYMARKET_PRIVATE_KEY"),
        chain_id=137  # Polygon
    )


def get_markets(client, limit=50):
    """Aktif piyasaları çek"""
    return client.get_markets(next_cursor="MA==", limit=limit)

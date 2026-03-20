from utils.polymarket_client import get_client, get_markets
from loguru import logger


def scan_markets():
    """Yüksek hacimli ve yakın kapanışlı piyasaları filtrele"""
    client = get_client()
    markets = get_markets(client)

    filtered = []
    for market in markets.get("data", []):
        # Sadece aktif, yeterli hacimli piyasalar
        if (market.get("active")
                and float(market.get("volume", 0)) > 10000
                and market.get("end_date_iso")):
            filtered.append(market)

    logger.info(f"Scanner: {len(filtered)} uygun piyasa bulundu")
    return filtered

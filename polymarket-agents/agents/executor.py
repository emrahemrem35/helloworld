from loguru import logger


def execute_trade(market: dict, tavsiye: str, miktar_usdc: float) -> dict:
    """İşlemi gerçekleştir"""

    # Gerçek işlem öncesi simülasyon modu önerilir!
    logger.warning(
        f"[EXECUTOR] {market.get('question')} → {tavsiye} → ${miktar_usdc}"
    )

    # Gerçek işlem için:
    # from utils.polymarket_client import get_client
    # client = get_client()
    # order = client.create_market_order(...)

    return {
        "durum": "simülasyon",
        "piyasa": market.get("question"),
        "tavsiye": tavsiye,
        "miktar": miktar_usdc,
    }

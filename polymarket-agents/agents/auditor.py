import json
import os
from datetime import datetime
from loguru import logger

LOG_PATH = "logs/trades.json"


def log_trade(market, analysis, position, execution):
    """Her işlemi kaydet"""
    entry = {
        "zaman": datetime.now().isoformat(),
        "piyasa": market.get("question"),
        "tavsiye": analysis.get("tavsiye"),
        "güven": analysis.get("güven_skoru"),
        "gerekçe": analysis.get("gerekçe"),
        "miktar": position.get("miktar_usdc", 0),
        "işlem": execution,
    }

    trades = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            trades = json.load(f)

    trades.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(trades, f, ensure_ascii=False, indent=2)

    logger.info(f"Auditor: Kayıt eklendi → {entry['piyasa'][:50]}")

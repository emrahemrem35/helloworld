import schedule
import time
import os
from dotenv import load_dotenv
from loguru import logger

from agents.scanner import scan_markets
from agents.signal_miner import get_news_signals
from agents.analyst import analyze_market
from agents.risk_manager import calculate_position
from agents.executor import execute_trade
from agents.auditor import log_trade

load_dotenv()

PORTFOLIO_VALUE = float(os.getenv("INITIAL_CAPITAL", 1000))


def run_cycle():
    logger.info("=== Yeni döngü başlıyor ===")

    markets = scan_markets()

    for market in markets[:10]:  # İlk 10 piyasayı analiz et
        question = market.get("question", "")

        # Sinyal topla
        news = get_news_signals(question[:50])

        # Analiz et
        analysis = analyze_market(market, news)

        if analysis["tavsiye"] == "SKIP":
            continue

        # Risk değerlendirmesi
        position = calculate_position(analysis, PORTFOLIO_VALUE)

        if not position["işlem_yap"]:
            logger.debug(f"Atlandı: {position['sebep']}")
            continue

        # İşlem
        execution = execute_trade(
            market, analysis["tavsiye"], position["miktar_usdc"]
        )

        # Kaydet
        log_trade(market, analysis, position, execution)

    logger.info("=== Döngü tamamlandı ===")


# Her 4 saatte bir çalıştır
schedule.every(4).hours.do(run_cycle)

if __name__ == "__main__":
    logger.add("logs/system.log", rotation="1 day")
    logger.info("Sistem başlatıldı")
    run_cycle()  # İlk çalıştırma
    while True:
        schedule.run_pending()
        time.sleep(60)

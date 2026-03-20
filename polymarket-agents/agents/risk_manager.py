import os


def calculate_position(analysis: dict, portfolio_value: float) -> dict:
    """Kelly Criterion benzeri pozisyon boyutu hesapla"""

    guven = analysis.get("güven_skoru", 0)
    esik = float(os.getenv("RISK_THRESHOLD", 0.65))
    max_oran = float(os.getenv("MAX_POSITION_SIZE", 0.10))

    if guven < esik:
        return {"işlem_yap": False, "sebep": f"Güven skoru düşük: {guven}"}

    # Güven skoruna göre ölçeklendir
    pozisyon_orani = min((guven - esik) * 2, max_oran)
    pozisyon_usdc = portfolio_value * pozisyon_orani

    return {
        "işlem_yap": True,
        "miktar_usdc": round(pozisyon_usdc, 2),
        "oran": pozisyon_orani,
    }

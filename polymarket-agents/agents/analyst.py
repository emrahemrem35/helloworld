from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_market(market: dict, news_signals: list) -> dict:
    """LLM ile piyasayı analiz et"""

    prompt = f"""
Sen bir prediction market analistisin. Aşağıdaki piyasayı analiz et.

Piyasa: {market.get('question')}
Mevcut Evet fiyatı: {market.get('best_ask')}
Mevcut Hayır fiyatı: {market.get('best_bid')}
Kapanış tarihi: {market.get('end_date_iso')}

İlgili haberler:
{chr(10).join(news_signals) if news_signals else 'Haber bulunamadı'}

Şu formatta JSON döndür (başka hiçbir şey yazma):
{{
  "tavsiye": "YES" veya "NO" veya "SKIP",
  "güven_skoru": 0.0 ile 1.0 arası,
  "gerekçe": "kısa açıklama"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    try:
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"tavsiye": "SKIP", "güven_skoru": 0, "gerekçe": "Parse hatası"}

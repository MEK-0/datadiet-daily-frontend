import json
from datetime import datetime

# BU SCRIPT BACKEND SİMÜLASYONUDUR
# Gerçek senaryoda bu veriler API'den veya Scraper'dan gelir.

# 1. Test Verisi Oluşturalım (Sanki Web'den çekmişiz gibi)
new_feed_data = [
    {
        "id": "news-update-1",
        "time": datetime.now().strftime("%I:%M %p"), # Güncel saat (Örn: 01:30 PM)
        "tags": [
            {
                "text": "PYTHON-TEST",
                "colorClass": "text-green-400 border-green-400/30", # Yeşil renk
                "type": "code"
            }
        ],
        "content": {
            "en": {
                "title": "Python Script Successfully Updated Feed",
                "description": "This news item was generated automatically by your Python backend script. The pipeline is working!",
                "hashtags": ["#python", "#automation", "#testing"]
            },
            "tr": {
                "title": "Python Scripti Akışı Başarıyla Güncelledi",
                "description": "Bu haber maddesi Python backend scriptiniz tarafından otomatik oluşturuldu. Boru hattı çalışıyor!",
                "hashtags": ["#python", "#otomasyon", "#test"]
            }
        }
    },
    {
        "id": "news-update-2",
        "time": "08:15 AM",
        "tags": [
            {
                "text": "AI-MODEL",
                "colorClass": "text-blue-400 border-blue-400/30",
                "type": "ai"
            }
        ],
        "content": {
            "en": {
                "title": "OpenAI Announces 'o1' Model",
                "description": "New reasoning-capable model outperforms predecessors in math and coding by 40%.",
                "hashtags": ["#machinelearning", "#openai"]
            },
            "tr": {
                "title": "OpenAI 'o1' Modelini Duyurdu",
                "description": "Yeni mantık yürütebilen model, matematik ve kodlamada öncekilerden %40 daha iyi.",
                "hashtags": ["#yapayzeka", "#openai"]
            }
        }
    }
]

# 2. JSON Dosyasını Yazalım
file_name = "news.json"

try:
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(new_feed_data, f, ensure_ascii=False, indent=4)
    print(f"✅ Başarılı! {file_name} dosyası güncellendi.")
    print("Şimdi 'git push' yaparak canlı siteyi güncelleyebilirsin.")
except Exception as e:
    print(f"❌ Hata oluştu: {e}")
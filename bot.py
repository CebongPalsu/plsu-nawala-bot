import cloudscraper
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

# =================== CONFIG ===================
TOKEN = "8339878742:AAGQUjt4pi-xia8WS-uxFIsKMlxCt3pVxrg"
GROUP_ID = -4931279381
MAX_DOMAIN = 50
NAWALA_URL = "https://nawala.online/check"
# ==============================================

# Buat scraper anti-Cloudflare
scraper = cloudscraper.create_scraper()

async def cek_nawala(domains: list):
    """
    Cek list domain ke nawala.online dan parsing hasilnya
    """
    hasil = []
    data = {"url": "\n".join(domains)}
    try:
        response = scraper.post(NAWALA_URL, data=data, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Parsing hasil per domain
        for tr in soup.select("table tbody tr"):
            tds = tr.find_all("td")
            if len(tds) >= 2:
                domain = tds[0].get_text(strip=True)
                status_text = tds[1].get_text(strip=True)
                status = "❌ Diblokir" if "terblokir" in status_text.lower() else "✅ Aman"
                hasil.append(f"{domain} – {status}")
    except Exception as e:
        hasil.append(f"Error cek Nawala: {e}")
    return hasil

async def cek_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler /cek <domain1> <domain2> ...
    """
    if not context.args:
        await update.message.reply_text(
            "Kirim /cek diikuti domain (max 50). Contoh:\n/cek domain1.com domain2.com"
        )
        return
    
    domains = context.args[:MAX_DOMAIN]
    await update.message.reply_text(f"🔍 Sedang cek {len(domains)} domain ke Nawala...")
    
    hasil = await cek_nawala(domains)
    
    pesan = "🔍 Hasil Cek Nawala:\n\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(hasil))
    
    # Kirim hasil ke grup
    await context.bot.send_message(chat_id=GROUP_ID, text=pesan)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot siap! Gunakan /cek <domain1> <domain2> ...")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("cek", cek_command))
    
    print("Bot berjalan...")
    app.run_polling()

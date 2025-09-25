import re
import dns.resolver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8339878742:AAGQUjt4pi-xia8WS-uxFIsKMlxCt3pVxrg"
ALLOWED_CHAT_ID = -4931279381  # ID grup lu

async def cek_domain(domain: str) -> str:
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["180.131.144.144", "180.131.145.145"]  # DNS Nawala
        resolver.resolve(domain, "A")
        return f"✅ {domain} : AMAN"
    except Exception:
        return f"🚫 {domain} : KENA NAWALA"

async def cek_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return await update.message.reply_text("🚫 Bot ini hanya bisa digunakan di grup tertentu.")

    text = update.message.text
    domains = re.findall(r"([\w-]+\.[\w.-]+)", text)

    if not domains:
        return await update.message.reply_text("❌ Format salah.\nContoh:\n/cek:\ndomain1.com\ndomain2.com")

    domains = domains[:50]  # batasi 50 domain
    results = [await cek_domain(domain) for domain in domains]
    hasil_text = "\n".join(results)

    await update.message.reply_text(f"📊 Hasil Cek ({len(domains)} domain):\n\n{hasil_text}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("cek", cek_handler))
    print("🤖 Bot aktif...")
    app.run_polling()

if __name__ == "__main__":
    main()

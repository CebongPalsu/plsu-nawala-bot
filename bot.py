import re
import dns.resolver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ganti dengan token bot lu
TOKEN = "8339878742:AAGQUjt4pi-xia8WS-uxFIsKMlxCt3pVxrg"

# ID grup yang diizinkan
ALLOWED_CHAT_ID = -4931279381

async def cek_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ✅ Cek kalau bukan dari grup yang diizinkan
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        await update.message.reply_text("🚫 Bot ini hanya bisa dipakai di grup resmi.")
        return

    text = update.message.text.strip()
    match = re.match(r"^/cek:(.+)$", text)
    if not match:
        await update.message.reply_text("⚠️ Format salah!\nContoh: /cek:google.com atau /cek:domain1.com,domain2.com")
        return

    domains = [d.strip() for d in match.group(1).split(",")]
    if len(domains) > 50:
        await update.message.reply_text("⚠️ Maksimal 50 domain sekali cek bro!")
        return

    results = []
    for domain in domains:
        try:
            dns.resolver.resolve(domain, 'A')
            results.append(f"✅ {domain} → *AMAN BRE*")
        except dns.resolver.NXDOMAIN:
            results.append(f"❌ {domain} → *ADUH KENA NIH / Tidak ditemukan*")
        except Exception as e:
            results.append(f"⚠️ {domain} Error: {str(e)}")

    await update.message.reply_text("\n".join(results))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Halo! Kirim perintah:\n\n/cek:namadomain.com\n/cek:domain1.com,domain2.com")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cek", cek_domain))

    print("🚀 Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()

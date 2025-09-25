import re
import dns.resolver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Token bot kamu
TOKEN = "8339878742:AAGQUjt4pi-xia8WS-uxFIsKMlxCt3pVxrg"

# 📌 ID grup yang diizinkan
ALLOWED_CHAT_ID = -4931279381

async def cek_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ✅ Cek grup
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        await update.message.reply_text("🚫 Bot ini hanya bisa dipakai di grup resmi.")
        return

    text = update.message.text.strip()

    # ✅ Cek format perintah
    if not text.lower().startswith("/cek:"):
        await update.message.reply_text("⚠️ Format salah!\nContoh:\n/cek:\ndomain1.com\ndomain2.com")
        return

    # ✨ Ambil semua baris domain setelah "/cek:"
    domain_text = text.split(":", 1)[1].strip()
    domains = [d.strip() for d in domain_text.split("\n") if d.strip()]

    if not domains:
        await update.message.reply_text("⚠️ Tidak ada domain yang dimasukkan.")
        return

    if len(domains) > 50:
        await update.message.reply_text("⚠️ Maksimal 50 domain sekali cek bro!")
        return

    # 🔍 Cek setiap domain
    results = []
    for domain in domains:
        try:
            dns.resolver.resolve(domain, 'A')
            results.append(f"✅ {domain} → 𝗔𝗠𝗔𝗡 𝗕𝗥𝗘")
        except dns.resolver.NXDOMAIN:
            results.append(f"❌ {domain} → 𝐀𝐃𝐔𝐇 𝐊𝐄𝐍𝐀 / 𝐓𝐢𝐝𝐚𝐤 𝐝𝐢𝐭𝐞𝐦𝐮𝐤𝐚𝐧")
        except Exception as e:
            results.append(f"⚠️ {domain} Error: {str(e)}")

    await update.message.reply_text("\n".join(results))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Kirim perintah seperti ini:\n\n"
        "/cek:\nnamadomain1.com\nnamadomain2.com\nnamadomain3.com"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cek", cek_domain))

    print("🚀 Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()

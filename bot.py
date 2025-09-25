import re
import dns.resolver
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Token bot kamu
TOKEN = "8339878742:AAGQUjt4pi-xia8WS-uxFIsKMlxCt3pVxrg"

# 📌 ID grup yang diizinkan
ALLOWED_CHAT_ID = -4931279381

# 🚀 Fungsi untuk cek domain secara paralel
async def check_domain(resolver, domain):
    try:
        await asyncio.get_event_loop().run_in_executor(None, resolver.resolve, domain, 'A')
        return f"✅ {domain} **TIDAK KENA NAWALA**"
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        return f"❌ {domain} **KENA NAWALA / Tidak dapat diakses dari DNS Nawala**"
    except Exception as e:
        return f"⚠️ {domain} Error: {str(e)}"

async def cek_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ✅ Cek grup
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        await update.message.reply_text("🚫 Bot ini hanya bisa dipakai di grup resmi.")
        return

    text = update.message.text.strip()

    # ✅ Pastikan format benar
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

    await update.message.reply_text("⏳ Sedang mengecek domain kamu ke DNS Nawala, tunggu sebentar...")

    # 🔍 Gunakan resolver Nawala
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["180.131.144.144"]

    # 🚀 Jalankan semua pengecekan secara paralel
    tasks = [check_domain(resolver, domain) for domain in domains]
    results = await asyncio.gather(*tasks)

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

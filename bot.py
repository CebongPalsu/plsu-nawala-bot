import socket
import re
import io
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

MAX_DOMAINS = 50
NAWALA_IP_PREFIX = "180.131.144."

def cek_nawala(domain: str) -> str:
    domain = domain.strip()
    domain = re.sub(r"^https?://", "", domain)
    domain = domain.split("/")[0]
    try:
        ip = socket.gethostbyname(domain)
        if ip.startswith(NAWALA_IP_PREFIX):
            return f"🚫 {domain} → KENA Nawala (IP: {ip})"
        else:
            return f"✅ {domain} → AMAN (IP: {ip})"
    except socket.gaierror:
        return f"❌ {domain} → Domain tidak bisa diresolusi"

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Gunakan perintah:\n/cek:\ndomain1.com\ndomain2.com ..."
    )

async def cek_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    match = re.search(r"/cek:(.*)", text, re.DOTALL)
    if not match:
        await update.message.reply_text("⚠️ Format salah!\nContoh:\n/cek:\ndomain1.com\ndomain2.com")
        return

    domains = [d.strip() for d in match.group(1).strip().splitlines() if d.strip()]
    if not domains:
        await update.message.reply_text("⚠️ Tidak ada domain yang diberikan.")
        return

    if len(domains) > MAX_DOMAINS:
        await update.message.reply_text(f"⚠️ Maksimal {MAX_DOMAINS} domain sekali cek ya bro.")
        return

    results = [cek_nawala(dom) for dom in domains]
    full_text = "\n".join(results)

    # kalau teks terlalu panjang, kirim sebagai file
    if len(full_text) > 3500:
        bio = io.BytesIO(full_text.encode("utf-8"))
        bio.name = "hasil_cek_nawala.txt"
        bio.seek(0)
        await update.message.reply_document(document=InputFile(bio), filename=bio.name)
    else:
        await update.message.reply_text(full_text)

def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ ERROR: TOKEN environment variable belum di-set")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("cek", cek_handler))
    print("🤖 Bot PLSU-NAWALA berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()

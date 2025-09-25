import re
import asyncio
import aiohttp
import dns.resolver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔐 Ganti dengan token bot kamu
BOT_TOKEN = "8339878742:AAGQUjt4pi-xia8WS-uxFIsKMlxCt3pVxrg"

# 📌 ID grup yang boleh pakai bot ini
ALLOWED_CHAT_ID = -4931279381

# IP khas DNS Nawala (biar deteksinya lebih akurat)
NAWALA_IP_PREFIXES = ["180.131.", "180.250."]

async def cek_nawala(domain: str) -> str:
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ["180.131.144.144", "180.131.145.145"]  # DNS Nawala
        answer = resolver.resolve(domain, "A")
        ip = answer[0].to_text()

        # Jika IP mengarah ke IP khas Nawala
        if any(ip.startswith(prefix) for prefix in NAWALA_IP_PREFIXES):
            return f"🚫 {domain} : KENA NAWALA (IP: {ip})"

        # Coba akses langsung domain-nya pakai HTTP
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://{domain}", timeout=3) as resp:
                    if resp.status in [200, 301, 302]:
                        return f"✅ {domain} : AMAN"
                    else:
                        return f"⚠️ {domain} : Resolve OK tapi respon {resp.status}"
            except asyncio.TimeoutError:
                return f"⚠️ {domain} : Timeout saat diakses"
            except:
                return f"⚠️ {domain} : Resolve OK tapi tidak bisa diakses"

    except Exception:
        return f"🚫 {domain} : KENA NAWALA (tidak bisa resolve)"

async def cek_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return await update.message.reply_text("🚫 Bot ini hanya bisa dipakai di grup khusus.")

    text = update.message.text
    domains = re.findall(r"([\w-]+\.[\w.-]+)", text)
    if not domains:
        return await update.message.reply_text("❌ Format salah.\nContoh:\n/cek:\ndomain1.com\ndomain2.com")

    # Maksimal 50 domain
    domains = domains[:50]

    # Jalankan semua pengecekan secara paralel 🚀
    tasks = [cek_nawala(domain) for domain in domains]
    results = await asyncio.gather(*tasks)

    hasil_text = "\n".join(results)
    await update.message.reply_text(f"📊 Hasil Pengecekan ({len(domains)} domain):\n\n{hasil_text}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("cek", cek_handler))
    print("🤖 Bot cepat & akurat sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()

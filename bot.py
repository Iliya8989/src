import telebot
import json
import psutil  # برای دریافت اطلاعات سیستمی
import socket  # برای دریافت IP
import requests  # برای دریافت Public IP
import subprocess  # برای اجرای دستورات سیستم
import re  # برای استخراج پورت از فایل
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def main():
    # خواندن تنظیمات از فایل JSON
    try:
        with open('telegram_config.json', 'r') as f:
            config = json.load(f)
        
        bot_token = config['bot_token']
        admin_id = config['admin_id']
        
        # راه‌اندازی ربات
        bot = telebot.TeleBot(bot_token)
        
        print(f"Bot started successfully for admin {admin_id}")
        
        # هندلر برای دستور /start
        @bot.message_handler(commands=['start'])
        def send_welcome(message):
            # فقط به پیام‌هایی که از طرف ادمین است پاسخ می‌دهد
            if str(message.from_user.id) == str(admin_id):
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("⚙️ استفاده از سیستم", callback_data='system_info'))
                markup.add(InlineKeyboardButton("👥 کاربران", callback_data='users_info'))
                markup.add(InlineKeyboardButton("ℹ️ اطلاعات پنل", callback_data='panel_info'))
                markup.add(InlineKeyboardButton("📄 فایل لاگ‌ها", callback_data='logs_info'))
                markup.add(InlineKeyboardButton("🖥️ وضعیت شبکه", callback_data='network_info'))
                
                bot.reply_to(message, "سلام! من ربات شما هستم.\nلطفاً یک گزینه را انتخاب کنید:", reply_markup=markup)
        
        # هندلر برای دکمه‌های شیشه‌ای
        @bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == 'system_info':
                # اطلاعات سیستم را ارسال می‌کند
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                response = (
                    f"⚙️ **اطلاعات سیستم:**\n"
                    f"🔹 **CPU Usage:** {cpu_percent}%\n"
                    f"🔹 **Memory Usage:** {memory.percent}%\n"
                    f"🔹 **Disk Usage:** {disk.percent}%\n"
                    f"🔹 **Available Memory:** {round(memory.available / (1024 ** 3), 2)} GB\n"
                    f"🔹 **Total Memory:** {round(memory.total / (1024 ** 3), 2)} GB\n"
                    f"🔹 **Available Disk:** {round(disk.free / (1024 ** 3), 2)} GB\n"
                    f"🔹 **Total Disk:** {round(disk.total / (1024 ** 3), 2)} GB\n"
                )
                bot.send_message(call.message.chat.id, response, parse_mode='Markdown')
            
            elif call.data == 'users_info':
                # خواندن اطلاعات کاربران از فایل wg0.conf
                try:
                    users = read_wireguard_users('wg0.conf')
                    if users:
                        response = "👥 **کاربران موجود در WireGuard:**\n" + "\n".join(users)
                    else:
                        response = "⚠️ کاربری در WireGuard ثبت نشده است."
                except Exception as e:
                    response = f"⚠️ خطا در خواندن کاربران WireGuard: {e}"
                bot.send_message(call.message.chat.id, response, parse_mode='Markdown')
            
            elif call.data == 'panel_info':
                # استخراج پورت و IP
                try:
                    public_ip = get_public_ip()
                    port = extract_port_from_file('dashboard.py')
                    if public_ip and port:
                        response = f"🌐 **اطلاعات پنل:**\nآدرس پنل: `{public_ip}:{port}`"
                    else:
                        response = "⚠️ پورت یا آی‌پی پیدا نشد."
                except Exception as e:
                    response = f"⚠️ خطا در دریافت اطلاعات پنل: {e}"
                bot.send_message(call.message.chat.id, response, parse_mode='Markdown')
            
            elif call.data == 'logs_info':
                # اجرای دستور tmux a و دریافت خروجی
                try:
                    logs = run_tmux_command()
                    bot.send_message(call.message.chat.id, f"📄 **لاگ‌ها:**\n{logs}", parse_mode='Markdown')
                except Exception as e:
                    bot.send_message(call.message.chat.id, f"⚠️ خطا در دریافت لاگ‌ها: {e}", parse_mode='Markdown')
            
            elif call.data == 'network_info':
                # وضعیت شبکه
                try:
                    public_ip = get_public_ip()
                    response = f"🖥️ **وضعیت شبکه:**\nآی‌پی عمومی سرور: `{public_ip}`"
                except Exception as e:
                    response = f"⚠️ خطا در دریافت وضعیت شبکه: {e}"
                bot.send_message(call.message.chat.id, response, parse_mode='Markdown')
        
        # شروع polling
        bot.polling(none_stop=True)
    
    except Exception as e:
        print(f"Error starting bot: {e}")
        sys.exit(1)

def extract_port_from_file(file_path):
    """
    فایل داده شده را می‌خواند و مقدار پورت را استخراج می‌کند.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            # جستجوی مقدار پورت
            match = re.search(r'port\s*=\s*(\d+)', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        return None
    return None

def get_public_ip():
    """
    آی‌پی عمومی سرور را دریافت می‌کند.
    """
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text.strip()
        else:
            raise Exception("Unable to fetch public IP.")
    except Exception as e:
        raise Exception(f"خطا در دریافت آی‌پی عمومی: {e}")

def read_wireguard_users(file_path):
    """
    کاربران موجود در فایل WireGuard را می‌خواند و لیست می‌کند.
    """
    try:
        users = []
        with open(file_path, 'r') as f:
            content = f.read()
            peers = re.findall(r'\[Peer\](.*?)AllowedIPs\s*=\s*([\d./]+)', content, re.S)
            for i, peer in enumerate(peers, 1):
                users.append(f"کاربر {i}: {peer[1]}")
        return users
    except FileNotFoundError:
        raise Exception("فایل WireGuard پیدا نشد.")
    except Exception as e:
        raise Exception(f"خطا در خواندن کاربران: {e}")

def run_tmux_command():
    """
    اجرای دستور tmux a و دریافت خروجی آن.
    """
    try:
        process = subprocess.Popen(['tmux', 'capture-pane', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            raise Exception(stderr.decode().strip())
        logs = stdout.decode().strip()
        # ارسال 20 خط آخر
        return "\n".join(logs.splitlines()[-20:])
    except Exception as e:
        raise Exception(f"خطا در اجرای tmux: {e}")

if __name__ == '__main__':
    main()

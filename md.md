# 🌐 Dashboard WireGuard
مدیریت WireGuard باید ساده‌تر باشد! به همین دلیل این پنل را برای مشاهده و مدیریت تنظیمات به صورت زیباتر ایجاد کردم. 🎉

## 📥 نصب دستی 

### 1. بروزرسانی و نصب WireGuard
ابتدا سرور را بروزرسانی کرده و WireGuard را نصب کنید:

apt update -y
apt install wireguard -y


### 2. ایجاد کلید خصوصی
برای ساخت کلید خصوصی از دستور زیر استفاده کنید و آن را یادداشت کنید: 🗝️

wg genkey | sudo tee /etc/wireguard/server_private.key


### 3. دریافت اینترفیس پیش‌فرض
برای دریافت نام اینترفیس پیش‌فرض (عبارت بعد از dev)، از دستور زیر استفاده کنید: 🔍

ip route list default


### 4. ویرایش فایل کانفیگ WireGuard
وارد مسیر کانفیگ WireGuard شوید: ✏️

nano /etc/wireguard/wg0.conf


### 5. کپی تنظیمات در فایل
متن زیر را در فایل کپی کنید:

[Interface]
Address = 172.20.0.1/24
PostUp = iptables -I INPUT -p udp dport 40600 -j ACCEPT
PostUp = iptables -I FORWARD -i eth0 -o wg0 -j ACCEPT
PostUp = iptables -I FORWARD -i wg0 -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostUp = ip6tables -I FORWARD -i wg0 -j ACCEPT
PostUp = ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D INPUT -p udp dport 40600 -j ACCEPT
PostDown = iptables -D FORWARD -i eth0 -o wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
PostDown = ip6tables -D FORWARD -i wg0 -j ACCEPT
PostDown = ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
ListenPort = 40600
PrivateKey = YOUR_GENERATED_PRIVATE_KEY
SaveConfig = true


- ⚡️ **نکته:** پورت WireGuard 40600 است، میتوانید پورت دیگری انتخاب کنید. 
- 🌍 **توجه:** برای سرورهای Digital Ocean، از IP خصوصی دیگری استفاده کنید.
- 🔑 **توجه:** کلید خصوصی ساخته شده را به جای YOUR_GENERATED_PRIVATE_KEY قرار دهید.
- 🖥️ **توجه:** اینترفیس پیش‌فرض را به eth0 تنظیم کردیم؛ اگر اینترفیس شما متفاوت است، آن را ویرایش کنید.
- ☑️ **نکته:** برای ایجاد اینترفیس‌های بیشتر، همین مراحل را دنبال کنید و فقط نام و پورت و IP را تغییر دهید.

### 6. نصب داشبورد 
اجازه دهید داشبورد را نصب کنیم:

apt update
apt install git
git clone https://github.com/amirmbn/WireGuard-Dashboard.git
cd WireGuard-Dashboard
mv src /root/
cd
rm -rf WireGuard-Dashboard
apt-get -y install python3-pip
apt install gunicorn -y
cd src
sudo chmod u+x wgd.sh
pip install -r requirements.txt
sudo ./wgd.sh install
sudo chmod -R 755 /etc/wireguard
./wgd.sh start


### 7. ورود به پنل
برای ورود به پنل خود به آدرس زیر بروید: 🌐  
**http://Your_Server_IP:1000**  
نام کاربری: admin و رمز عبور: 1234 🛡️

- 🔄 **اگر با مشکل internal error مواجه شدید، سرور را ریبوت کرده و این دستور را اجرا کنید:**
cd src
./wgd.sh restart


### 8. حذف کامل WireGuard و پنل
برای حذف کامل، دستورات زیر را اجرا کنید:

cd
rm -rf src
rm -rf /etc/wireguard
sudo apt remove wireguard -y


- 👷‍♂️ **اگر قصد نصب مجدد پنل را دارید، قبل از نصب این کد را وارد کنید:**
mkdir /etc/wireguard


## 📸 پیش‌نمایش
!  
!  
!  
!  
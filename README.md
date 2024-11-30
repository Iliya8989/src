**نصب به صورت دستی**
-
<div align="right">
  <details>
    <summary><strong>توضیحات آموزش</strong></summary>

 - سرور را اپدیت کنید و وایرگارد را نصب کنید.
<div align="left">
 
```
apt update -y
apt install wireguard -y
```
<div align="right">
 
 - پرایوت کی بسازید و در یک جا یادداشتش کنید . با دستور زیر میتوانید بسازید
 
 
<div align="left">
 
```
wg genkey | sudo tee /etc/wireguard/server_private.key
```
<div align="right">
 
 - و با دستور زیر میتوانید کلیدی که ساختید را مشاهده کنید
<div align="left">
 
```
cat /etc/wireguard/server_private.key
```
<div align="right">


- با دستور زیر وارد مسیر کانفیگ وایرگارد بشوید. [مسیر پیش فرض است]
<div align="left">
 
```
nano /etc/wireguard/wg0.conf
```
<div align="right">

- داخلش متن زیر را کپی کنید
<div align="left">
  
```
[Interface]
Address = 176.66.66.1/24
PostUp = iptables -I INPUT -p udp --dport 20820 -j ACCEPT
PostUp = iptables -I FORWARD -i eth0 -o wg0 -j ACCEPT
PostUp = iptables -I FORWARD -i wg0 -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostUp = ip6tables -I FORWARD -i wg0 -j ACCEPT
PostUp = ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D INPUT -p udp --dport 20820 -j ACCEPT
PostDown = iptables -D FORWARD -i eth0 -o wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
PostDown = ip6tables -D FORWARD -i wg0 -j ACCEPT
PostDown = ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
ListenPort = 20820
PrivateKey = YOUR_GENERATED_PRIVATE_KEY
SaveConfig = true
```
<div align="right">

- میتوانید از ایپی های دیگری استفاده کنید.
- پورت وایرگارد در اینجا 20820 است . میتوانید پورت دیگری انتخاب کنید.
- نام اینترفیس خود را با دستور ip a پیدا کنید . در اینجا به صورت پیش فرض eth0 میباشد.
- دقت کنید برای سرور های دیجیتال اوشن،  از پرایوت ایپی دیگری استفاده نمایید.
- برای ساختن اینترفیس های بیشتر و با پورت های مختلف با همین روش بالا انجام بدید و فقط نام و پورت و ایپی رو عوض کنید
- به صورت پیش فرض Peer Remote Endpoint بر روی یک عدد بی ربط است. حتما از داخل تنظیمات این مقدار را به ایپی 4 خارج یا سرور ایران در صورت تانل تغییر بدهید.
- در پنل وایرگارد داخل  ایپی کاربر وایرگارد، برای کاربر بر اساس ایپی انتخابی بالا ، از 176.66.66.2/32 و برای کاربر دوم از 176.66.66.3/32 استفاده میکنید.
 - پس از اینکه فایل را از گیت هاب در سیستم عامل خودتون دانلود کردید با دستورات زیر پیش نیازها را نصب کنید و پنل را اجرا کنید
<div align="left">
 
```
apt update
apt install git
git clone https://github.com/Iliya8989/wg-guard.git
cd wg-guard
mv wg-guard /root/
cd
rm -rf wg-guard
apt-get -y install python3-pip
apt install gunicorn -y
cd wg-guard/src
tmux
sudo chmod u+x wgd.sh
pip install -r requirements.txt
sudo ./wgd.sh install
sudo chmod -R 755 /etc/wireguard
python3 dashboard.py
```
-پس از انجام این مراحل کلید  بزنید Ctrl + B
<div align="right">

- به پنل خودتون با [serverip:8080] وارد شوید. نام کاربری و رمز عبور پنل به صورت پیش فرض admin میباشد.
- دقت کنید که داخل تنظیمات Remote endpoint را به ایپی سرور ایران در صورت تانل تغییر بدهید.
  </details>
</div>

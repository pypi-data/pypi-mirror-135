Bot Studio is a python library for runing bots built with DataKund Studio.
You can also train bots with DataKund to automate repetitive work without doing any programming.
It currently runs only on windows.

### Installation
```sh
pip install bot-studio
```

### Import Bot Studio
```
from bot_studio import *
```

### Create Object
Create object first to open browser.
```sh
dk=bot_studio.new()
```

#### Run a bot
```sh
dk.amazon_login(email='put your email here', login_url='https://www.amazon.com/gp/sign-in.html', password='put password here')
```

#### Make Bot using Studio
To create your own bot follow below steps:-
* Run command "datakund" in command prompt
* A browser will get opened containing DK extension
* To open Extension press Alt+O
* Type the bot name e.g "google_search" and click on "Make New Bot"
* Click on Record and do actions like opening link, typing etc.
* Go back and then Run bot

---
**NOTE**

If you want to call your bots in your code, then consider bot names which do not contain space, special character etc.
---


#### Access Your bot through Code
To access your code:-
* Go to Code Section in extension
* Go to python and copy the code
* Now run that code, your bot will run

#### Make your bots public
To share your bots with public, so that anyone can run them follow these steps:-
* Go to your bot in Extension
* Go to More section and then Publish
* Write title, desc and image and click on Publish
* Here you go, now anyone can run this bot

#### Run public bot
Here we will run the bot we did made above
```sh
google_search(keyword="shoes")
```

### Send Feedback to Developers
```sh
bot_studio.send_feedback(feedback="Need help with this ......")
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)


# Announcements on discord made easy
## About 
This bot made in python using the [discord.py](https://pypi.org/project/discord.py/) module checks your database for new challenges and announces them on the channels of your choice for your convenience

The bot posts to 2 (Two) seperate channels:

An admin channel: Where the bot can post extra information about the subject (In this case challenges) for the admins to make their lives slightly easier

A general channel: Where the bot posts the announcements for all the members to see

(The code can be modified and adjusted to suite your needs)

## Requirements
Requirements are listed in the "requirements.txt" file
To install the reruirements with pip run:
```
pip install -r requirements.txt
```

## How to use
In the main.py file there are a couple of fields that you should change and fill then run the file normally with: 

On Windows:
```
python main.py
```
On Linux:
(make sure python3 is installed)
```
python3 main.py
```

Or 
```
nohup python script.py > output.log &
```
This will keep the bot running in the background on your server even after your session ends (the logs and errors will be stored in "output.log")

### The info required with the fields:

![image](https://github.com/Mstr0A/New-Challenge-Discord-Bot/assets/79792105/63f52d1f-ea34-4c27-912e-133abf530877)


**hostname:**
The hostname or host IP of where your database is stored so the bot can access it

**username:** The username of the user account so the bot can log-in to retrieve the data (typically root)

**password:**
The password for the user account account

**database:**
The spicific database you wanna access the data of

**TOKEN:**
The bot token (Info on how to make a bot and get a token [here](https://discord.com/developers/docs/intro))

**THE INFO MENTIONED ABOVE MUST BE KEPT PRIVATE AS IT IS SENSITIVE INFORMATION**

**Admin and general channel ID:**
The ID of the channel where you want the announcements to happen

And lastly don't forget to change the admin and general messages you want to send to your server(s)

## Credits
Made by: [Mstr0A](https://github.com/Mstr0A) (Me)

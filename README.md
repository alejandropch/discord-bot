# Discord Bot

Hey guys, this is a discord bot I made i while ago to familiarize myself with the [Discord.py](https://discordpy.readthedocs.io/en/stable) library. It also includes some [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) to connect an AWS database. I designed this to manage user interaction and collect user data from guilds where it is present.

## How to run locally

First install the nedded dependencies:

```pip3 install -r requirements.txt```

Copy the .env.example file that contains information such as the bot token:

```cp .env.example .env```

Finally run the bot:

```python3 bot.py```

## Deployment

 - Provision a new ubuntu server.
 - Install PM2 node package.
 - Run:``` pm2 start bot.py --name="<bot name>" --interpreter=python3```

## Disclaimer

This is a simple project I made to help me handle real world problems. This code does not represent any system running in production

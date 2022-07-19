# Discord Community Engagement Bot

Bot provided to handle user interaction and collect user data from guilds where it is present.

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

 ## Discord.py Documentation

[Official Documentation](https://discordpy.readthedocs.io/en/latest/index.html)
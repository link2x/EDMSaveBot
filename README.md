# EDMSaveBot
EDMSaveBot, a reddit bot with the purpose of saving linked reddit posts.

## Running EDMSaveBot
EDMSaveBot is designed to be rather simple.

If on linux, ensure you have python3 and python3-pip installed in your package manager.

`sudo apt-get install python3 python3-pip`

Then, install PRAW through pip.

`pip3 install praw`

Once that's done, everything is more-or-less set to go.
Inside edmsavebot.py, modify the user agent to something unique to your bot.

Then, run the following:

`python3 /path/to/bot/edmsavebot.py --subreddit gifs`


or on Windows:
`C:\path\to\python3\python.exe C:\path\to\bot\edmsavebot.py -subreddit gifs`

This will run the bot as the stated user in the stated subreddit.

As part of startup, EDMSaveBot will ask you to open a link.
Ensure you're signed into the bot account, then open the link and click Accept.
Once you've done so, copy the characters in the url after = and paste them into the bot.

This is currently how to sign the bot on to reddit.

Be aware that the bot will fail when posting comments at speed, due to reddit's limitations.
As you garner upvotes, this problem will subside. You can alleviate this issue using the `-lowkarma` flag.

## Available Flags:
`-subreddit Sub` - Allows you to set the subreddit from the commandline.

`-lowkarma` - Adds a 10-minute pause between comments, used to alleviate low-karma cooldowns.

`-verbose` - Shows more debug messages. Most are now hidden by default.

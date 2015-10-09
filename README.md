# EDMSaveBot
EDMSaveBot, a reddit bot with the purpose of saving linked reddit posts.

## Running EDMSaveBot
EDMSaveBot is designed to be rather simple.

If on linux, ensure you have python-pip installed in your package manager.

`sudo apt-get install python-pip`

Then, install PRAW through pip.

`pip install praw`

Once that's done, everything is more-or-less set to go.
Inside edmsavebot.py, modify the user agent to something unique to your bot.

Then, run the following:

`python /path/to/bot/edmsavebot.py -username LeRedditor -password LePassword -subreddit gifs`


or on Windows:
`C:\path\to\python\python.exe C:\path\to\bot\edmsavebot.py -username LeRedditor -password LePassword -subreddit gifs`

This will run the bot as the stated user in the stated subreddit.

Be aware that the bot will fail when posting comments at speed, due to reddit's limitations.
As you garner upvotes, this problem will subside. You can alleviate this issue using the `-lowkarma` flag.

## Available Flags:
`-username User` - Allows you to set the username from the commandline.
`-password Pass` - Allows you to set the password from the commandline. Insecure on linux.
`-subreddit Sub` - Allows you to set the subreddit from the commandline.
`-lowkarma` - Adds a 10-minute pause between comments, used to alleviate low-karma cooldowns.

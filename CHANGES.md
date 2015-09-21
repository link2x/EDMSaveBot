Version 1.1.7
	- Changelog is now separate.
	- Simplify version and user agent string changes
	- Cut down on stdout slightly
	- Comments check is now run on proper url
	- Added low-karma flag (instead of manually patching it in every time)

Version 1.1.6
	- Fix detection of non-applicable links within reddit.

Version 1.1.5
	- Modified post formatting.

Version 1.1.4
	- Fixes formatting when saving comments.

Version 1.1.3
	- Cut down on the debug messages for N/A posts by adding them to the avoid-list.

Version 1.1.2
	- Subreddit can now be passed from command-line.

Version 1.1.1
	- Login information can now be passed from command-line.

Version 1.1.0:
	- Remove usernames from comment.
	- Remove login information. Ask for it instead. (Replace with console arguments later.)
	- Modify loop delay to 15 seconds. 2 was too fast.
	- Add time to loop debug for an easy answer to "did it freeze?".

Version 1.0.0:
	- Check subreddit for posts linking back to reddit.
	- Check links for post type.
	- Post in comment of new post saving post text, time, and karma.
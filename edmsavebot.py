# EDMSaveBot
# By: /u/link2x (http://link2x.us/)
#
# Version 1.1.6
#
# Purpose:
#   This bot is intended to save the original contents of posts linked to by /r/EDMProdCircleJerk.
#
#
# CHANGES:
#
# Version 1.1.6
#   - Fix detection of non-applicable links within reddit.
#
# Version 1.1.5
#   - Modified post formatting.
#
# Version 1.1.4
#   - Fixes formatting when saving comments.
#
# Version 1.1.3
#   - Cut down on the debug messages for N/A posts by adding them to the avoid-list.
#
# Version 1.1.2
#   - Subreddit can now be passed from command-line.
#
# Version 1.1.1
#   - Login information can now be passed from command-line.
#
# Version 1.1.0:
#   - Remove usernames from comment.
#   - Remove login information. Ask for it instead. (Replace with console arguments later.)
#   - Modify loop delay to 15 seconds. 2 was too fast.
#   - Add time to loop debug for an easy answer to "did it freeze?".
#
# Version 1.0.0:
#   - Check subreddit for posts linking back to reddit.
#   - Check links for post type.
#   - Post in comment of new post saving post text, time, and karma.

import praw     # reddit wrapper
import re       # Regular expressions
import time     # Clock for nice comments
import argparse # Allow for signing in from command-line

print("D: Imports completed")

r = praw.Reddit("PRAW // EDMSave // v1.1.6 // /u/link2x") # User agent to comply with reddit API standards

print("D: PRAW initialized")

commandParse = argparse.ArgumentParser()
commandParse.add_argument("-username",help="reddit username",type=str)
commandParse.add_argument("-password",help="reddit password",type=str)
commandParse.add_argument("-subreddit",help="subreddit to run on",type=str)
commandInput = commandParse.parse_args()

redditUser = None
redditUser = commandInput.username
redditPass = None
redditPass = commandInput.password
redditSub = None
redditSub = commandInput.subreddit

if (not redditUser):
    redditUser = input("Bot account name: ")
if (not redditPass):
    redditPass = input("Bot account pass: ")
if (not redditSub):
    redditSub = input("Subreddit to run on: ")

r.login(redditUser,redditPass) # Connect to reddit

print("D: Logged in to reddit")
print("D: "+redditUser+" SUB: "+redditSub)

already_done = [] # Used to help avoid re-commenting, doesn't last through reboots currently.
regexString = '/(.{7})(/*)$|\n' # This is used to differentiate between links to posts and links to comments
regexRE = re.compile(regexString) # This allows the above string to be used to search

while True: #Main loop
    print("D: Loop begin")
    subreddit = r.get_subreddit(redditSub) #Set our subreddit. Glorious master race
    for submission in subreddit.get_new(limit=10): #We'll look at the 10 newest posts
        if submission.id not in already_done: # Make sure we haven't already ran this post
            if ((submission.is_self==False) and (submission.domain=='reddit.com')): #If the post is a link pointing at reddit
                if ('/comments/' in str(submission.url)): #Verify it's a post or comment we're being linked to
                    searchComments = submission.comments # For all comments here
                    flatSearch = praw.helpers.flatten_tree(searchComments) # ^
                    for comment in flatSearch: # Run each comment
                        if str(comment.author) == "EDMSaveBot": # Looking for our name
                            already_done.append(submission.id) # Add this post to the list if we find it
                            print("D: Added old post to avoid list") # Debug for easy following
                    if submission.id not in already_done: #Make sure we haven't already ran this post

                        httpsUrl = submission.url.replace("http://","https://") # Our bot expects HTTPS links, this makes sure we don't get bounced
                        
                        loadedPost = r.get_submission(url=httpsUrl) # It's go time; load the link
                        
                        savingComments = regexRE.search(submission.url) # Are we looking for a comment, or just a post?

                        print("D: New post") # Debug for easy following

                        if savingComments:
                            print("D: Linked to a comment") # Debug for easy following
                            loadedComment = loadedPost.comments[0] # Load the top comment (automatically the linked comment)
                            postType = 'comment' # Label the post
                            postTitle = '' # Blanked to avoid possible issues
                            postRedditor = str(loadedComment.author) # Save the author
                            postText = loadedComment.body # Save the post
                            postScore = str(loadedComment.score) # Save the post's score
                            postTime = loadedComment.created_utc # Save the post's origin/edit date
                            print("D: Data collected successfully") # Debug for easy following
                        else:
                            print("D: Linked to a submission") # Debug for easy following
                            # We don't nead to load the post as it's already been loaded
                            postTitle = loadedPost.title
                            if (loadedPost.is_self==True):
                                postType = 'self post' # Label the post
                                postText = loadedPost.selftext # Save the post
                            else:
                                postType = 'link post' # Label the post
                                postText = loadedPost.url # Save the link
                            postRedditor = str(loadedPost.author) # Save the author    
                            postScore = str(loadedPost.score) # Save the post's score
                            postTime = loadedPost.created_utc # Save the post's origin/edit date
                            print("D: Data collected successfully") # Debug for easy following

                        # Now we have the information, lets set up our post
                        botTime = time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime()) # Keep everything in UTC because why not
                        formatTime = time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime(postTime)) # ^

                        if savingComments == True:
                            botComment = 'The linked '+postType+' was posted '+formatTime+'\n\n'+postText+'\n****\n('+postScore+' Karma) ([About](/r/EDMSaveBot))'
                        else:
                            botComment = 'The linked '+postType+' was posted '+formatTime+'\n****\n**'+postTitle+'**\n\n'+postText+'\n****\n('+postScore+' Karma) ([About](/r/EDMSaveBot))'

                        print("D: Comment formatted") # Debug for easy following
                    
                        # Now we're all set to post, here we go.
                        submission.add_comment(botComment)
                        print("D: Comment posted") # Debug for easy following

                        already_done.append(submission.id)

                else:
                    print("D: Post not applicable: Doesn't link to a post or comment") # Debug for easy following
                    already_done.append(submission.id)
            else:
                print("D: Post not applicable: Doesn't link within reddit") # Debug for easy following
                already_done.append(submission.id)
    print("D: Loop end "+time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime()))
    time.sleep(15) # Wait a few seconds before looping

# EDMSaveBot
# By: /u/link2x (http://link2x.us/)
#
# Version 1.5.3
#
# Purpose:
#   This bot is intended to save the original contents of posts linked to by /r/EDMProdCircleJerk.
#


# Constants

botVersionMajor  = 1
botVersionMinor  = 5
botVersionBuild  = 3
botOwner = '/u/link2x'


# Imports

import praw                 # reddit wrapper
import re                   # Regular expressions
import time                 # Clock for nice comments
import argparse             # Allow for signing in from command-line
import requests             # I guess praw uses this. Redefine to calm python down.
from subprocess import call # We use this for -notify


# CLI flag parsing

commandParse = argparse.ArgumentParser()

commandParse.add_argument("-subreddit",help="subreddit to run on",type=str)
commandParse.add_argument("-lowkarma",help="adds a 10-minute wait after comments",action="store_true")
commandParse.add_argument("-verbose",help="adds debug messages",action="store_true")
commandParse.add_argument("-notify",help="calls a shell command in some cases, such as errors",type=str)

commandInput = commandParse.parse_args()

redditSub    = None
redditSub    = commandInput.subreddit
lowKarma     = False
lowKarma     = commandInput.lowkarma
verboseMode  = False
verboseMode  = commandInput.verbose
notify       = False
notify       = commandInput.notify

if verboseMode:
    print("D: Imports completed")


# Function declaration

def send_notify(command, text):
    if verboseMode:
        print("D: Calling "+command+" "+text)
    call([command+" "+text], shell=True)
    return 1

if verboseMode:
    print("D: Functions defined")


# Initialization

botVersionString = str(botVersionMajor)+'.'+str(botVersionMinor)+'.'+str(botVersionBuild)
r = praw.Reddit("PRAW // EDMSave // v"+botVersionString+" // "+botOwner) # User agent to comply with reddit API standards

if verboseMode:
    print("D: PRAW initialized")

if (not redditSub):
    redditSub = input("Subreddit to run on: ")


# Login

print("Please sign into your bot account.")

# I can't say I was ready for OAuth. But okay.
r.set_oauth_app_info(client_id='dyxM6A3_apsmhw',
			client_secret='FvQxLB6AXl5G9CbEOLC0DOrJgm8',
			redirect_uri='http://127.0.0.1:65010/'
			'authorize_callback')

url = r.get_authorize_url('uniqueKey','identity edit read submit',True)

print(url)
key = input("Reddit Key: ")

access_information = r.get_access_information(key)
r.set_access_credentials(**access_information)

me = r.get_me().name

if verboseMode:
    print("D: me: "+me)

if verboseMode:
    print("D: Logged in to reddit")


# Main loop

print("EDMSaveBot version "+botVersionString+" running on /r/"+redditSub)

already_done = [] # Used to help avoid re-commenting, doesn't last through reboots currently.
regexString = '/(.{7})(/*)$|\n' # This is used to differentiate between links to posts and links to comments
regexRE = re.compile(regexString) # This allows the above string to be used to search

while True: #Main loop
    try:
        subreddit = r.get_subreddit(redditSub) #Set our subreddit. Glorious master race
        for submission in subreddit.get_new(limit=25): #We'll look at the 10 newest posts
            if submission.id not in already_done: # Make sure we haven't already ran this post
                if ((submission.is_self==False) and (submission.domain=='reddit.com' or submission.domain=='np.reddit.com')): #If the post is a link pointing at reddit
                    if ('/comments/' in str(submission.url)): #Verify it's a post or comment we're being linked to
                        searchComments = submission.comments # For all comments here
                        flatSearch = praw.helpers.flatten_tree(searchComments) # ^
                        for comment in flatSearch: # Run each comment
                            if str(comment.author) == me: # Looking for our name
                                already_done.append(submission.id) # Add this post to the list if we find it
                                if verboseMode:
                                    print("D: Added old post to avoid list ("+str(submission.id)+")") # Debug for easy following
                        if submission.id not in already_done: #Make sure we haven't already ran this post

                            httpsUrl = submission.url.replace("http://","https://") # Our bot expects HTTPS links, this makes sure we don't get bounced
                            httpsUrl = httpsUrl.replace("//reddit","//www.reddit") # People apparently can't link properly. This is causing greif
                            httpsUrl = httpsUrl.replace("//np.reddit","//www.reddit") # Our bot is expecting www links, so let's double check that we have one
                            httpsUrl = httpsUrl.partition("?")[0] # This removes php queries, most notably context

                            loadedPost = r.get_submission(url=httpsUrl) # It's go time; load the link

                            savingComments = regexRE.search(httpsUrl) # Are we looking for a comment, or just a post?

                            if verboseMode:
                                print("D: New post ("+str(submission.id)+")") # Debug for easy following

                            if savingComments:
                                if verboseMode:
                                    print("D: Linked to a comment") # Debug for easy following
                                loadedComment = loadedPost.comments[0] # Load the top comment (automatically the linked comment)
                                postType = 'comment' # Label the post
                                postTitle = '' # Blanked to avoid possible issues
                                postRedditor = str(loadedComment.author) # Save the author
                                postText = loadedComment.body # Save the post
                                postScore = str(loadedComment.score) # Save the post's score
                                postTime = loadedComment.created_utc # Save the post's origin/edit date
                                postSub = loadedComment.subreddit.display_name
                                if verboseMode:
                                    print("D: Data collected successfully") # Debug for easy following
                            else:
                                if verboseMode:
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
                                postSub = loadedPost.subreddit.display_name
                                if verboseMode:
                                    print("D: Data collected successfully") # Debug for easy following

                            # Now we have the information, lets set up our post
                            botTime = time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime()) # Keep everything in UTC because why not
                            formatTime = time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime(postTime)) # ^

                            if savingComments:
                                botComment = 'The linked '+postType+' was posted '+formatTime+'\n****\n'+postText+'\n****\n(/r/'+postSub+') ('+postScore+' Karma) ([About](/r/EDMSaveBot))'
                            else:
                                botComment = 'The linked '+postType+' was posted '+formatTime+'\n****\n**'+postTitle+'**\n\n'+postText+'\n****\n(/r/'+postSub+') ('+postScore+' Karma) ([About](/r/EDMSaveBot))'
                                    

                            if verboseMode:
                                print("D: Comment formatted") # Debug for easy following

                            # Now we're all set to post, here we go.
                            submission.add_comment(botComment)
                            if verboseMode:
                                print("D: Comment posted") # Debug for easy following

                            already_done.append(submission.id)

                            if lowKarma:
                                if verboseMode:
                                    print("D: Low-karma wait started")
                                time.sleep(600)

                    else:
                        if verboseMode:
                            print("D: Post not applicable: Doesn't link to a post or comment") # Debug for easy following
                        already_done.append(submission.id)
                else:
                    if verboseMode:
                        print("D: Post not applicable: Doesn't link within reddit") # Debug for easy following
                    already_done.append(submission.id)
        print("I: Loop end "+time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime()))
        time.sleep(15) # Wait a few seconds before looping
    except praw.errors.Forbidden:
        if verboseMode:
                print("D: Forbidden subreddit or post.")
        already_done.append(submission.id)
    except praw.errors.HTTPException as e: # Catch reddit servers being slow, since that happens all the time.
        print("E: Reddit is slow. Re-looping.")
    except requests.exceptions.ConnectionError: # I'm not sure what's behind this one. Perhaps HTTPS or some strange reddit slowness?
        print("E: Something strange happened. requests.exceptions.ConnectionError")
    except requests.exceptions.HTTPError as e: # These usually are caught in the first except, but just in case this catches 404s and the like.
        print("E: HTTP Code ", e.message)
    except requests.exceptions.ReadTimeout as e:
        print("E: Reddit is slow. Re-looping.")
    except: # I don't want this thing to crash, but this at least lets me know /when/ it happens.
        if notify:
            send_notify(notify, "'EDMSaveBot running on /r/"+redditSub+" has crashed.'")
        print("E: Unexpected error. Raising", time.strftime('at %I:%M %p (UTC) on %A %B %d.',time.gmtime()))
        raise;

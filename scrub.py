"""
Author:         David Schaeffer
Date Created:   February 2, 2019
Purpose:        Scrub a reddit account of all comments.
Execution:      python3 scrub.py <username> <password>
"""

import praw
import sys

from config import CLIENT_ID, CLIENT_SECRET


def main(username: str, password: str):
    """
    Authenticates as user, fetches their comments, edits them, and then deletes them.
    Since fetching comments doesn't return all of them at once, it will fetch new comments
    when it runs out and exit once it cannot find any new comments.
    :param username: The account you'd like to authenticate as.
    :param password: The password to the account.
    :return: System exit.
    """
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         username=username,
                         password=password,
                         user_agent='comment_scrubber script!')
    comments_listing_gen = reddit.redditor(username).comments.new()
    my_comments = [comm for comm in comments_listing_gen]
    while my_comments:
        print('Comments found. Editing and deleting...')
        for comment in my_comments:
            comment.edit('.')
            comment.delete()
        print('Fetching more comments...')
        comments_listing_gen = reddit.redditor(username).comments.new()
        my_comments = [comm for comm in comments_listing_gen]
    print('No more comments to be found. Exiting...')
    sys.exit(0)


if __name__ == '__main__':
    if 2 < len(sys.argv) < 4:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.stderr.write('Please enter your username and password.\n'
                         'Ex: python scrub.py my_reddit_username my_reddit_password')
        sys.exit(0)

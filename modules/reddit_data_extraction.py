import os
import praw
import json
import time
from config import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, WORK_DIR
from prawcore.exceptions import ServerError


def connect_to_reddit(client_id, client_secret, user_agent):
    """
    Function to establish a Reddit instance
    """
    reddit = praw.Reddit(
        client_id=client_id, client_secret=client_secret, user_agent=user_agent
    )
    return reddit


def save_to_json(file_path, data):
    """
    Function to save data to a JSON file
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_top_posts_and_comments(
    subreddit_name,
    reddit_instance,
    file_path=None,
    windows=["day"],
    post_limit=20,
    comment_limit=100,
):
    """
    Function to get top posts and their top comments from a specific subreddit
    """
    subreddit = reddit_instance.subreddit(subreddit_name)

    for window in windows:
        print(f"Getting top posts from r/{subreddit_name} for {window}...")
        if os.path.exists(file_path.replace(".json", f"_{window}.json")):
            print("File already exists. Skipping...")
            continue
        else:
            top_posts = []
            last_exception = None
            timeout = 60  # seconds
            time_start = int(time.time())
            while not top_posts and int(time.time()) < time_start + timeout:
                try:
                    for post in subreddit.top(window, limit=post_limit):
                        top_comments = []
                        post.comments.replace_more(limit=0)
                        for comment in post.comments.list()[:comment_limit]:
                            top_comments.append(
                                {
                                    "id": comment.id,
                                    "body": comment.body,
                                    "score": comment.score,
                                }
                            )

                        top_posts.append(
                            {
                                "title": post.title,
                                "score": post.score,
                                "id": post.id,
                                "url": post.url,
                                "created": post.created,
                                "body": post.selftext,
                                "comments": top_comments,
                            }
                        )
                    # catch the case no posts were found
                    if not top_posts:
                        raise ValueError("No posts found!")
                except ServerError as e:
                    # server overloaded, wait for 5 seconds
                    last_exception = e
                    print("Server overloaded, waiting for 5 seconds...")
                    time.sleep(5)

            if not top_posts:
                raise last_exception

            if file_path is not None:
                save_to_json(file_path.replace(".json", f"_{window}.json"), top_posts)
            else:
                return top_posts

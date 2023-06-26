from unittest.mock import MagicMock
from modules.reddit_data_extraction import connect_to_reddit, get_top_posts_and_comments
from config import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, WORK_DIR


def test_connect_to_reddit():
    reddit = connect_to_reddit(REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT)
    assert str(type(reddit)) == "<class 'praw.reddit.Reddit'>"


def test_get_top_posts_and_comments():
    # Mock the Reddit and Subreddit objects
    reddit = MagicMock()  # No spec parameter
    subreddit = MagicMock()

    # Mock the methods that we're going to call on the Reddit and Subreddit objects
    reddit.subreddit.return_value = subreddit
    subreddit.top.return_value = [MagicMock() for _ in range(10)]

    # Make sure each mocked post has a comments attribute that is a list of mocked comments
    for post in subreddit.top.return_value:
        post.comments.list.return_value = [MagicMock() for _ in range(10)]

    posts_and_comments = get_top_posts_and_comments("wallstreetbets", reddit)

    # Now we can perform some tests...

    # Check that it returns a list
    assert isinstance(posts_and_comments, list)

    # Check that the list is not empty
    assert len(posts_and_comments) > 0

    # Check that each post has required fields
    for post in posts_and_comments:
        assert "title" in post
        assert "score" in post
        assert "id" in post
        assert "url" in post
        assert "created" in post
        assert "body" in post
        assert "comments" in post

        # Check that each post's comments have required fields
        for comment in post["comments"]:
            assert "id" in comment
            assert "body" in comment
            assert "score" in comment

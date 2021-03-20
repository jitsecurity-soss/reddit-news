import settings
import praw
import schedule
import time
from post import Post
from db_connector import session_object
from fetch_posts import fetch_posts


def save_subreddit(client: praw.Reddit, config: dict):
    posts = fetch_posts(reddit_client=client,
                        subreddit=config['name'],
                        posts_amount=config['posts'],
                        ignore_stickied=config['ignoreStickied'])
    post_objects = []
    for post in posts:
        post_objects.append(Post(
            title=post.title,
            score=post.score,
            url=post.url,
            permalink=post.permalink,
            over_18=post.over_18
        ))
    session_object.add_all(post_objects)


if __name__ == "__main__":
    reddit_client = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        username=settings.REDDIT_USER,
        password=settings.REDDIT_PASSWORD,
        user_agent=settings.REDDIT_USER_AGENT
    )
    for subreddit_config in settings.SUBREDDITS_CONFIG:
        schedule.every(subreddit_config['secondsInterval']).seconds.do(save_subreddit, reddit_client, subreddit_config)
    while True:
        schedule.run_pending()
        time.sleep(1)

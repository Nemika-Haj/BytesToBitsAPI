import praw
import random

class RedditHandler:
    def __init__(self, **kwargs):
        self.reddit = praw.Reddit(**kwargs)

    @property
    def is_image(self, link):
        return link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif')

    def get(self, subreddit=None, limit=10, one_random=True):
        if not subreddit:
            subreddit = random.choice(["memes", "dankmemes", "funny", "meirl", "me_irl"])
        submissions = self.reddit.subreddit(subreddit).hot(limit=limit)
        submissions = [post for post in submissions]

        if one_random:
            return random.choice([{
                "title": sub.title,
                "url": sub.url,
                "link": sub.shortlink,
                "subreddit": subreddit,
                "upvotes": sub.ups,
                "downvotes": sub.downs,
                "comments": len(sub.comments)
            } for sub in submissions])
        else:
            return [{
                "title": sub.title,
                "url": sub.url,
                "link": sub.shortlink,
                "subreddit": subreddit,
                "upvotes": sub.ups,
                "downvotes": sub.downs,
                "comments": len(sub.comments),
                "text": sub.selftext
            } for sub in random.sample(submissions, limit if limit <= len(submissions) else len(submissions))]

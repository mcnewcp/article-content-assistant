import json
import os
from dotenv import load_dotenv
import tweepy
import requests

from ..utils.config import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_BEARER_TOKEN,
)

# Load environment variables if running as a standalone script
if __name__ == "__main__":
    load_dotenv()


def post_to_twitter(content, image_url=None):
    """
    Post content to Twitter with an optional image using Twitter API v2.
    """
    try:
        # Authenticate with Twitter API v2
        client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
        )

        # If there's an image, upload it to Twitter
        media_ids = None
        if image_url:
            # For media upload, we still need to use v1.1 API
            auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)

            response = requests.get(image_url)
            if response.status_code == 200:
                # Save the image temporarily
                with open("temp_image.jpg", "wb") as f:
                    f.write(response.content)
                # Upload the image to Twitter
                media = api.media_upload("temp_image.jpg")
                media_ids = [media.media_id]
                # Remove the temporary image file
                os.remove("temp_image.jpg")

        # Post the tweet
        if media_ids:
            tweet = client.create_tweet(text=content, media_ids=media_ids)
        else:
            tweet = client.create_tweet(text=content)

        return f"Posted to Twitter: {tweet.data['id']}"
    except Exception as e:
        return f"Error posting to Twitter: {str(e)}"


# ... (rest of the file remains unchanged)

# For local testing
if __name__ == "__main__":
    platforms = ["twitter", "facebook", "linkedin", "instagram"]
    test_content = "Exciting news from Mars! NASA's Perseverance rover has discovered organic molecules, hinting at the possibility of ancient microbial life. #SpaceExploration #MarsDiscovery"
    test_image_url = "https://example.com/mars_discovery_image.jpg"

    for platform in platforms:
        test_event = {
            "body": json.dumps(
                {
                    "platform": platform,
                    "content": test_content,
                    "image_url": test_image_url,
                }
            )
        }
        print(f"\nTesting post to {platform}:")
        result = lambda_handler(test_event, None)
        print(json.dumps(result, indent=2))

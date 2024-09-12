import json
from dotenv import load_dotenv

# Load environment variables if running as a standalone script
if __name__ == "__main__":
    load_dotenv()


def post_to_twitter(content, image_url=None):
    """
    Placeholder function for posting to Twitter.
    """
    # TODO: Implement actual Twitter posting logic
    return f"Posted to Twitter: {content[:50]}..."


def post_to_facebook(content, image_url=None):
    """
    Placeholder function for posting to Facebook.
    """
    # TODO: Implement actual Facebook posting logic
    return f"Posted to Facebook: {content[:50]}..."


def post_to_linkedin(content, image_url=None):
    """
    Placeholder function for posting to LinkedIn.
    """
    # TODO: Implement actual LinkedIn posting logic
    return f"Posted to LinkedIn: {content[:50]}..."


def post_to_instagram(content, image_url):
    """
    Placeholder function for posting to Instagram.
    """
    # TODO: Implement actual Instagram posting logic
    return f"Posted to Instagram: {content[:50]}..."


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        body = json.loads(event["body"])
        platform = body["platform"]
        content = body["content"]
        image_url = body.get("image_url")

        if platform == "twitter":
            result = post_to_twitter(content, image_url)
        elif platform == "facebook":
            result = post_to_facebook(content, image_url)
        elif platform == "linkedin":
            result = post_to_linkedin(content, image_url)
        elif platform == "instagram":
            if not image_url:
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {"error": "Image URL is required for Instagram posts"}
                    ),
                }
            result = post_to_instagram(content, image_url)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid platform"}),
            }

        return {"statusCode": 200, "body": json.dumps({"result": result})}
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}


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

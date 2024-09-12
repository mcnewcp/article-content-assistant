import json
from openai import OpenAI

from ..utils.config import (
    OPENAI_API_KEY,
    IMAGE_GENERATOR_MODEL,
    IMAGE_INSTRUCTIONS,
)

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_image(article_summary):
    """
    Generate an image based on the given article summary using DALL-E.
    """
    try:
        response = client.images.generate(
            model=IMAGE_GENERATOR_MODEL,
            prompt=f"{IMAGE_INSTRUCTIONS}\n\n{article_summary}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        return f"Error generating image: {str(e)}"


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        body = json.loads(event["body"])
        article_summary = body["article_summary"]

        image_url = generate_image(article_summary)
        return {"statusCode": 200, "body": json.dumps({"image_url": image_url})}
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}


# For local testing
if __name__ == "__main__":
    # Print the first few characters of the API key to verify it's loaded correctly
    print(
        f"OPENAI_API_KEY: {OPENAI_API_KEY[:5]}..."
        if OPENAI_API_KEY
        else "OPENAI_API_KEY is not set"
    )
    print(f"IMAGE_GENERATOR_MODEL: {IMAGE_GENERATOR_MODEL}")

    test_summary = "Elon Musk's recent commentary on the upcoming US presidential election and his attacks on Vice President Kamala Harris have escalated, particularly through the use of AI-generated content. He shared an image on social media depicting Harris in a communist uniform, accompanied by misleading claims. Musk, a supporter of Donald Trump, has also promoted misogynistic views regarding female participation in government. These posts have garnered millions of views, raising concerns about the spread of misinformation on social media platforms. The incident reflects Musk's increasing influence and the potential impact of his rhetoric on public discourse."
    test_event = {"body": json.dumps({"article_summary": test_summary})}
    print("Testing image generation:")
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))

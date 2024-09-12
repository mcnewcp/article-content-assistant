import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from ..utils.config import (
    OPENAI_API_KEY,
    ARTICLE_PROCESSOR_MODEL,
    PROCESSOR_INSTRUCTIONS,
)

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_raw_article(url):
    """
    Fetch and extract the raw content of an article from a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all raw text from paragraphs. This could be improved with a more measured approach.
        raw_content = " ".join([p.get_text() for p in soup.find_all("p")])
        return raw_content
    except requests.RequestException as e:
        return f"Error fetching article: {str(e)}"


def process_article(url):
    """
    Process the article and return structured information using OpenAI.
    """
    content = fetch_raw_article(url)

    try:
        response = client.chat.completions.create(
            model=ARTICLE_PROCESSOR_MODEL,
            messages=[
                {"role": "system", "content": PROCESSOR_INSTRUCTIONS},
                {
                    "role": "user",
                    "content": f"Please extract the requested information from the following article text:\n\n{content}",
                },
            ],
            response_format={"type": "json_object"},
        )

        # Parse the JSON response
        structured_output = json.loads(response.choices[0].message.content)

        # Add the original URL to the output
        structured_output["url"] = url

        return structured_output
    except Exception as e:
        return {"error": f"Error processing article: {str(e)}"}


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        url = json.loads(event["body"])["url"]
        result = process_article(url)
        return {"statusCode": 200, "body": json.dumps(result)}
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
    print(f"ARTICLE_PROCESSOR_MODEL: {ARTICLE_PROCESSOR_MODEL}")

    test_url = "https://www.cnbc.com/2024/09/10/ai-powered-search-startup-glean-doubles-valuation-in-new-funding-round.html"
    test_event = {"body": json.dumps({"url": test_url})}
    print("Testing process_article:")
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))

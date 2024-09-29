import json
from openai import OpenAI

from ..utils.config import (
    OPENAI_API_KEY,
    CONTENT_GENERATOR_MODEL,
    CONTENT_ASSISTANT_CONFIGS,
)

from typing import Optional

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def _load_or_create_assistant(platform: str):
    """
    Load or create an assistant given the platform.
    Use the config for the relevant platform.
    Return the assistant id.
    """
    platform_config = CONTENT_ASSISTANT_CONFIGS.get(platform)
    assistant_name = f'{platform}-{platform_config.get("version")}'

    try:
        for asst in client.beta.assistants.list():
            if assistant_name == asst.name:
                # assistant found
                print(f"assistant {assistant_name} found")
                return asst.id

        print(f"assistant {assistant_name} not found, attempting to create")
        asst = client.beta.assistants.create(
            model=CONTENT_GENERATOR_MODEL,
            instructions=platform_config.get("instructions"),
            name=assistant_name,
            temperature=platform_config.get("temperature"),
            top_p=platform_config.get("top_p"),
        )
        print(f"assistant {assistant_name} created")
        return asst.id
    except Exception as e:
        return f"Error getting or creating assistant: {str(e)}"


def get_n_chr(text: str):
    """
    Count and return the number of characters in a string.
    """
    return


def shorten_content():
    """
    Shorten the content on the given thread and return the new content.
    """
    return


def generate_content(article_text, platform):
    """
    Generate social media content based on the article text and platform.
    """
    try:
        # check platform
        if platform not in CONTENT_ASSISTANT_CONFIGS:
            raise ValueError(f"Unsupported platform: {platform}")

        # get assistant
        assistant_id = _load_or_create_assistant(platform)

        # setup thread
        thread_id = client.beta.threads.create().id
        message = client.beta.threads.messages.create(
            thread_id,
            content=f"Please generate social media content from the following article.\n\n{article_text}",
            role="user",
        )

        # get result
        run_result = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id, assistant_id=assistant_id, poll_interval_ms=2000
        )
        content_response = client.beta.threads.messages.list(
            thread_id, limit=1, order="desc"
        )
        return {
            "content": content_response.data[0].content[0].text.value,
            "thread_id": thread_id,
        }

    except Exception as e:
        return f"Error generating content: {str(e)}"


def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    try:
        body = json.loads(event["body"])
        article_text = body["article_text"]
        platform = body["platform"]

        result = generate_content(article_text, platform)
        return {"statusCode": 200, "body": json.dumps({"generated_content": result})}
    except Exception as e:
        return {"statusCode": 400, "body": json.dumps({"error": str(e)})}


def regenerate_content(thread_id: str, user_message: Optional[str] = None):
    """
    Regenerate content associated with a given thread.  Optionally, add a user message to the prompt.
    """
    return


# For local testing
if __name__ == "__main__":
    # Print the first few characters of the API key to verify it's loaded correctly
    print(
        f"OPENAI_API_KEY: {OPENAI_API_KEY[:5]}..."
        if OPENAI_API_KEY
        else "OPENAI_API_KEY is not set"
    )
    print(f"CONTENT_GENERATOR_MODEL: {CONTENT_GENERATOR_MODEL}")

    test_article = """Elon Musk's disdain for the Democratic Party was never subtle, but in recent weeks his commentary on the upcoming US presidential election and his attacks against Vice President Kamala Harris have intensified, aided by a crude use of burgeoning artificial intelligence technology.

                    On Monday, Musk posted an AI-generated image on his social media platform that depicted Harris as a communist, wearing a red uniform complete with hammer and sickle emblazoned hat.

                    Musk, who has endorsed former President Donald Trump for president and poured millions into a super PAC supporting the Republican, captioned the image with the false assertion, "Kamala vows to be a communist dictator on day one. Can you believe she wears that outfit!?"

                    The image, which appeared to violate X's policy on manipulated content, resembled an AI-generated image posted by Trump last month during the Democratic National Convention, envisioning Harris addressing a crowd under communist symbols.

                    Musk's post came a day after he shared another post with a screenshot suggesting that only "high status males" should be able to participate in government because women (and men with "low testosterone") are not capable of critical thought. Musk posted it to his 196 million followers with the comment, "interesting observation."

                    The sexist screed appears to have originated on 4Chan, the notorious hate-filled website that has been linked to mass-shootings.

                    By choosing to amplify disinformation and misogynist views, Musk, a South African billionaire who is both the owner of X and the most-followed account on the platform, is promoting radical content to the masses that might otherwise languish in the darkest corners of the internet.

                    By Tuesday afternoon, less than 24 hours after Musk shared the fake image and false statement depicting Harris as a communist, the post had been viewed nearly 60 million times, according to data from X. Musk's post suggesting women shouldn't take part in democracy had been viewed more than 19 million times.

                    X did not respond to a CNN request for comment.

                    The posts come after Brazilian authorities blocked access to X in the country in a battle over the spread of misinformation and hate speech on the platform aimed at undermining the nation's democracy.

                    Since taking over the platform, Musk has touted X's "community notes" feature as a way of transparently allowing crowd-sourced fact-checking misinformation on his platform.

                    Yet neither post was fact-checked through the community notes feature. Musk's defenders, of which there are many who are vocal on X, have attempted to argue that some posts like these are satirical or are not meant to be taken seriously.

                    But Musk is taken seriously. He is one of the world's most powerful people who controls one of the world's most important online platforms on the precipice of an historic American presidential election where he is actively campaigning for a candidate.

                    When Musk took over Twitter in 2022 in a $44 billion acquisition, he claimed that the platform would remain impartial to avoid the perception of tilting the scales for a political party.

                    "For Twitter to deserve public trust, it must be politically neutral, which effectively means upsetting the far right and the far left equally," he wrote.

                    But Musk's posts, and the lack of scrutiny they receive from his company's own fact-checking system, lay bare how Musk has turned X into a pro-Trump machine."""

    platforms = ["X"]

    for platform in platforms:
        test_event = {
            "body": json.dumps({"article_text": test_article, "platform": platform})
        }
        print(f"\nTesting content generation for {platform}:")
        result = lambda_handler(test_event, None)
        print(json.dumps(result, indent=2))

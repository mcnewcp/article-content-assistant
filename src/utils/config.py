import os

# Load environment variables from .env file only if not in a cloud environment
if os.getenv("ENV") != "cloud":
    from dotenv import load_dotenv

    load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ARTICLE_PROCESSOR_MODEL = "gpt-4o-mini"
CONTENT_GENERATOR_MODEL = "gpt-4o"
IMAGE_GENERATOR_MODEL = "dall-e-3"

# Airtable configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_ARTICLE_TABLE_NAME = "Articles"
AIRTABLE_CONTENT_TABLE_NAME = "Post Content"

# X (Twitter) configuration
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Validate required environment variables
required_vars = [
    "DISCORD_TOKEN",
    "CHANNEL_ID",
    "OPENAI_API_KEY",
    "AIRTABLE_API_KEY",
    "AIRTABLE_BASE_ID",
    "TWITTER_API_KEY",
    "TWITTER_API_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET",
    "TWITTER_BEARER_TOKEN",
]

for var in required_vars:
    if not globals()[var]:
        raise EnvironmentError(f"{var} is not set in the environment variables.")


def get_instructions(filename):
    """Load instructions from a file in the utils directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    with open(file_path, "r") as file:
        return file.read()


# Load system prompts
PROCESSOR_INSTRUCTIONS = get_instructions("processor_instructions.txt")
# if a platform's instructions are updated, the corresponding version number must be increased
# otherwise the updated instructions will not be used
CONTENT_INSTRUCTIONS_X = get_instructions("content_instructions_x.txt")
VERSION_X = 1
IMAGE_INSTRUCTIONS = get_instructions("image_instructions.txt")

# Social media generation params
GEN_PARAMS = {
    "X": {
        "temperature": 1,
        "max_tokens": 85,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
}

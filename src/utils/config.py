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

# Validate required environment variables
required_vars = [
    "DISCORD_TOKEN",
    "CHANNEL_ID",
    "OPENAI_API_KEY",
    "AIRTABLE_API_KEY",
    "AIRTABLE_BASE_ID",
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
CONTENT_INSTRUCTIONS_X = get_instructions("content_instructions_x.txt")
IMAGE_INSTRUCTIONS = get_instructions("image_instructions.txt")

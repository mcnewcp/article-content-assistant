# Article Content Assistant

This project is a Discord bot that processes articles, generates social media content, and manages postings to various platforms using generative AI.

## Features

- Fetches and processes article content from URLs
- Extracts article content, summary, and metadata
- Generates tailored social media content for different platforms
- Creates related images using DALL-E3
- Stores article data and generated content in Airtable
- Posts content to various social media platforms, currenlty only works with X (Twitter)
- Discord bot interface for easy interaction

## Project Structure

The project is organized as a Python package with the following structure:

```
article-content-assistant/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── handlers/
│   │   ├── article_processor.py
│   │   ├── content_generator.py
│   │   ├── image_generator.py
│   │   ├── airtable_manager.py
│   │   └── social_media_poster.py
│   └── utils/
│       ├── config.py
│       ├── content_instructions_x.txt
│       ├── image_instructions.txt
│       └── processor_instructions.txt
├── run_bot.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/mcnewcp/article-content-assistant.git
   cd article-content-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following content:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   CHANNEL_ID=your_discord_channel_id
   OPENAI_API_KEY=your_openai_api_key
   AIRTABLE_API_KEY=your_airtable_api_key
   AIRTABLE_BASE_ID=your_airtable_base_id
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   ```

   Replace the placeholder values with your actual keys, tokens, and IDs.

5. Set up an Airtable base with two tables named "Articles" and "Post Content". Alternatively, name the tables whatever you like and change `AIRTABLE_ARTICLE_TABLE_NAME` and `AIRTABLE_CONTENT_TABLE_NAME` in `src/utils/config.py` to match.

## Running the Bot

To run the Discord bot locally, execute the following command from the project root:

```
python -m run_bot.py
```

## Usage

1. Invite the bot to your Discord server and ensure it has access to the specified channel.
2. Post a URL in the designated channel to trigger article processing.
3. The bot will process the article, extract key information, generate content, and save it to Airtable.
4. The bot will then display the generated content to the user and inform the user it is ready to post.
4. Use the `!post` command to post content to social media platforms:
   - `!post_twitter <content record id>` to post to Twitter
   - other platforms under development

## Testing Individual Handlers

Each handler in the `src/handlers/` directory can be run as a standalone module for testing purposes. To run a handler test, use the following command from the project root:

```
python -m src.handlers.[handler_name]
```

For example, to test the article processor:

```
python -m src.handlers.article_processor
```

This will run the test code included at the bottom of each handler file.

## Development

- The `src/handlers/` directory contains individual modules for each functionality.
- `src/main.py` is the entry point and contains the Discord bot logic.
- `src/utils/config.py` centralizes configuration and environment variable loading.
- To deploy to AWS Lambda, each handler in `src/handlers/` can be used as a separate Lambda function.

## Configuration

- To modify the article processing logic:
   - Update the `processor_instructions.txt` file in the `src/utils/` directory
   - Modify `ARTICLE_PROCESSOR_MODEL` in `src/utils/config.py`
- To modify content generation logic:
   - Update the `content_instructions_<platform>.txt` file in the `src/utils/` directory
   - Modify the `CONTENT_GENERATOR_MODEL` in `src/utils/config.py`
   - Modify the generation parameters corresponding to the respective platform in `GEN_PARAMS` in `src/utils/config.py`
- To modify image generation:
   - Update the `image_instructions.txt` file in the `src/utils/` directory
   - Modify the `IMAGE_GENERATOR_MODEL` in `src/utils/config.py`

## Deployment

### Local Development
For local development, the application will automatically load environment variables from the `.env` file.

### Cloud Deployment (AWS Elastic Beanstalk)
When deploying to AWS Elastic Beanstalk:

1. Set the `ENV` environment variable to `cloud` in the AWS Elastic Beanstalk configuration.
2. Configure all other required environment variables in the AWS Elastic Beanstalk environment.

The application will use these environment variables directly without attempting to load from a `.env` file.

## Future Improvements

- Implement additional platforms
- Add error handling and logging
- Refine article content extraction for better accuracy across various websites

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

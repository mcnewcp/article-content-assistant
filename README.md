# Article Content Assistant

This project is a Discord bot that processes articles, generates social media content, and manages postings to various platforms using AI-powered analysis.

## Features

- Fetches and processes article content from URLs using OpenAI's GPT model
- Extracts article content, summary, and metadata
- Generates tailored social media content for different platforms
- Creates related images using DALL-E3
- Stores article data and generated content in Airtable
- Posts content to various social media platforms (placeholder functionality)
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
│       └── processor_instructions.txt
├── .env
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/article-content-assistant.git
   cd article-content-assistant
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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
   ```

   Replace the placeholder values with your actual API keys and IDs.

5. Set up an Airtable base with a table named "Articles" (or update the table name in `src/handlers/airtable_manager.py`).

## Running the Bot

To run the Discord bot locally, execute the following command from the project root:

```
python -m src.main
```

## Usage

1. Invite the bot to your Discord server and ensure it has access to the specified channel.
2. Post a URL in the designated channel to trigger article processing.
3. The bot will process the article, extract key information, generate content, and save it to Airtable.
4. Use the `!post` command to post content to social media platforms:
   - `!post twitter` to post to Twitter
   - `!post facebook` to post to Facebook
   - `!post linkedin` to post to LinkedIn
   - `!post instagram` to post to Instagram
   - `!post all` to post to all platforms

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

- To modify the article processing logic, update the `processor_instructions.txt` file in the `src/utils/` directory.
- To change the OpenAI model used for article processing, update the `ARTICLE_PROCESSOR_MODEL` variable in `src/utils/config.py`.

## Deployment

### Local Development
For local development, the application will automatically load environment variables from the `.env` file.

### Cloud Deployment (AWS Elastic Beanstalk)
When deploying to AWS Elastic Beanstalk:

1. Set the `ENV` environment variable to `cloud` in the AWS Elastic Beanstalk configuration.
2. Configure all other required environment variables (DISCORD_TOKEN, CHANNEL_ID, OPENAI_API_KEY, AIRTABLE_API_KEY, AIRTABLE_BASE_ID) in the AWS Elastic Beanstalk environment.

The application will use these environment variables directly without attempting to load from a `.env` file.

## Future Improvements

- Implement actual social media posting functionality
- Add error handling and logging
- Implement user authentication for posting commands
- Create a web interface for managing the bot and viewing analytics
- Refine article content extraction for better accuracy across various websites

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

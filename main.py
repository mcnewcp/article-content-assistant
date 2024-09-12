import discord
from discord.ext import commands
import json
from handlers import (
    article_processor,
    content_generator,
    image_generator,
    airtable_manager,
)
from utils.config import DISCORD_TOKEN, CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == int(CHANNEL_ID):
        # Check if the message contains a URL
        urls = [word for word in message.content.split() if word.startswith("http")]
        if urls:
            url = urls[0]  # Take the first URL found
            await process_article(message.channel, url)

    await bot.process_commands(message)


async def process_article(channel, url):
    await channel.send(f"Processing article from URL: {url}")

    # 1. Fetch and process the article
    article_data = article_processor.process_article(url)
    if "error" in article_data:
        await channel.send(f"Error processing article: {article_data['error']}")
        return

    await channel.send("Article processed. Generating content...")

    # 2. Save article data to Airtable
    airtable_article_record_id = airtable_manager.save_to_airtable(article_data)
    await channel.send(
        f"Article data saved to Airtable. Article Record ID: {airtable_article_record_id}"
    )

    # 3. Generate social media content
    platforms = ["X"]
    generated_content = {}
    for platform in platforms:
        content = content_generator.generate_content(
            article_data.get("text", ""), platform
        )
        generated_content[platform] = content
        await channel.send(f"Generated content for {platform}:\n{content[:100]}...")

    # 4. Generate image
    image_url = image_generator.generate_image(article_data.get("summary", ""))
    await channel.send(f"Generated image: {image_url}")

    # 5. Inform user that content is ready for review
    await channel.send("Content generated and saved. You can review it in Airtable.")

    # Commented out social media posting functionality
    # await channel.send("Use !post [platform] to post to a specific platform, or !post all to post to all platforms.")


# Commented out social media posting command
"""
@bot.command(name="post")
async def post_content(ctx, platform):
    if ctx.channel.id != int(CHANNEL_ID):
        return

    # Retrieve the latest record from Airtable
    latest_record = airtable_manager.get_latest_record()

    if not latest_record:
        await ctx.send("No content available for posting.")
        return

    generated_content = json.loads(latest_record["GeneratedContent"])
    image_url = latest_record["ImageURL"]

    if platform.lower() == "all":
        for p in ["twitter", "facebook", "linkedin", "instagram"]:
            await ctx.send(f"Simulated posting to {p}")
    elif platform.lower() in ["twitter", "facebook", "linkedin", "instagram"]:
        await ctx.send(f"Simulated posting to {platform}")
    else:
        await ctx.send("Invalid platform. Use 'twitter', 'facebook', 'linkedin', 'instagram', or 'all'.")
"""

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

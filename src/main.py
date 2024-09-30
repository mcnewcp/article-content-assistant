import discord
from discord.ext import commands

from .handlers import (
    article_processor,
    content_generator,
    image_generator,
    airtable_manager,
    social_media_poster,
)
from .utils.config import DISCORD_TOKEN, CHANNEL_ID

from typing import Optional

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
    await channel.send("Processing article from above URL.")

    # 1. Fetch and process the article
    article_data = article_processor.process_article(url)
    if "error" in article_data:
        await channel.send(f"Error processing article: {article_data['error']}")
        return

    await channel.send("Article processed.")

    # 2. Save article data to Airtable
    airtable_article_record_id = airtable_manager.save_to_airtable(
        article_data, "article"
    )
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
        await channel.send(f"Generated content for {platform}:\n{content}")

    # 4. Generate image
    image_url = image_generator.generate_image(article_data.get("summary", ""))
    await channel.send(f"Generated image: {image_url}")

    # 6. Save social media content to airtable
    for platform, content in generated_content.items():
        airtable_content_record_id = airtable_manager.save_to_airtable(
            {
                "article_record_id": airtable_article_record_id,
                "platform": platform,
                "content": content,
                "image_url": image_url,
                "posted": "N",
            },
            "content",
        )
        await channel.send(
            f"Content saved to Airtable.  Content Record ID: {airtable_content_record_id}"
        )

    # 7. Inform user that content is ready for review
    await channel.send(
        f"Content generated and ready to post.\nYou can post to twitter with the command `!post_twitter {airtable_content_record_id}`"
    )


@bot.command(name="post_twitter")
async def post_twitter(ctx, content_id: str):
    """
    Post content to Twitter using the given Airtable content record ID.
    Usage: !post_twitter <content_id>
    """

    # Fetch content from Airtable
    content_data = airtable_manager.get_content_by_id(content_id)
    article_data = airtable_manager.get_from_airtable(
        content_data.get("article_record_id"), "article"
    )
    article_url = article_data.get("url")

    if not content_data:
        await ctx.send(f"Content with ID {content_id} not found in Airtable.")
        return

    # Post to Twitter
    result = social_media_poster.post_to_twitter(
        content_data["content"] + "\n" + article_url, content_data.get("image_url")
    )

    if "Error" in result:
        await ctx.send(f"Failed to post to Twitter: {result}")
    else:
        await ctx.send(f"Successfully posted to Twitter: {result}")

        # Update Airtable to mark content as posted
        update_result = airtable_manager.update_content_status(content_id, "Y")
        await ctx.send(f"Airtable record {content_id} updated as posted.")


@bot.command(name="regenerate_content")
async def regenerate_content(ctx, content_id: str, user_message: Optional[str] = None):
    """
    Regenerate content for given content_id.  Optionally include user message in prompt.
    Usage: !regenerate_content
    """
    return


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

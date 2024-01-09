# Import necessary libraries
import discord
import responses
import openai
from discord.ext import commands

# Define the intents you want to enable
intents = discord.Intents.all()
intents.message_content = True

# Create a bot instance with the intents and a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

voice_channels = {}

TOKEN = 'MTE1MTM3NzU3MTg0NjU3NDIyMg.G8Nw57.wub0fw-ADejftDkIZMhwCwCR7vTo4J6yCpCOm8'
OPENAI_KEY = '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'
openai.api_key = OPENAI_KEY

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


@bot.command()
async def join(ctx):
    # Check if the user is in a voice channel
    print("join command recieved")
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_channels[ctx.guild.id] = channel
        await channel.connect()
        print(f'Joined voice channel: {channel.name}')  # Add this line for logging
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def leave(ctx):
    # Check if the bot is in a voice channel
    if ctx.guild.id in voice_channels:
        voice_channel = voice_channels[ctx.guild.id]
        await ctx.voice_client.disconnect()
        del voice_channels[ctx.guild.id]
        print(f'Left voice channel: {voice_channel.name}')  # Add this line for logging
    else:
        await ctx.send("I'm not in a voice channel right now.")

@bot.command()
async def play(ctx, url):
    # Check if the bot is in a voice channel
    if ctx.guild.id in voice_channels:
        voice_channel = voice_channels[ctx.guild.id]

        # Check if the URL is valid and supported (you may need to implement additional checks)
        # Use a music library like youtube-dl to play audio from the URL
        # Example: You can use youtube_dl to download and play YouTube videos
        # This is a simplified example, and you might need to handle errors and edge cases.
        # Make sure to install youtube-dl using 'pip install youtube-dl'.
        try:
            voice_client = ctx.voice_client
            await voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(url))
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send("I'm not in a voice channel right now. Use the !join command first.")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself
        
    if bot.user in message.mentions:
            # Generate a response using the OpenAI API based on the mentioned message
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{message.content}",
            max_tokens=1000,
            temperature=0.5,
        )

            # Send the generated response to the same channel as the original message
        await message.channel.send(response.choices[0].text)


    # Run the Discord bot using the specified token
bot.run(TOKEN)



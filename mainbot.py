import discord
import requests
from dotenv import load_dotenv
import os
from discord.ext import commands

# Load environment variables
load_dotenv()

# Initialize bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# API Configuration
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
COINGECKO_CRYPTOS_URL = f"{COINGECKO_API_URL}/coins/markets"
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")  # Optional: for higher rate limits

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is online and ready!")

@bot.command(name="crypto")
async def crypto_prices(ctx):
    try:
        # Fetch top 10 cryptocurrencies by market cap
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False
        }

        headers = {}
        if COINGECKO_API_KEY:
            headers["x-cg-api-key"] = COINGECKO_API_KEY

        response = requests.get(COINGECKO_CRYPTOS_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for HTTP errors

        data = response.json()
        if not data:
            await ctx.send("No data received from the API.")
            return

        result = "**Top 10 Cryptocurrencies (USD):**\n"
        for coin in data[:10]:
            symbol = coin["symbol"].upper()
            name = coin["name"]
            price = coin["current_price"]
            result += f"**{name} ({symbol})**: ${price:.2f}\n"

        await ctx.send(result)

    except requests.exceptions.RequestException as e:
        await ctx.send(f"❌ Error fetching crypto prices: {str(e)}")
    except Exception as e:
        await ctx.send(f"⚠️ Unexpected error: {str(e)}")

# Run the bot
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

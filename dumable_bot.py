import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
from dotenv import load_dotenv
import random
import math
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

load_dotenv()

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["dumable_bot"]
users_collection = db["users"]
cooldowns_collection = db["cooldowns"]

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=["!", "."], intents=intents)

# ==================== BROKEN MATH FUNCTIONS ====================

def broken_multiply(a, b):
    """Returns hilariously wrong multiplication"""
    correct = a * b
    wrong_options = [
        correct * random.randint(2, 10),  # Way too much
        random.randint(1, correct),  # Way too little
        correct + random.randint(1000, 50000),  # Random huge add
        int(correct ** 1.5),  # Exponential wrong
        random.randint(0, 1) * correct,  # 50% chance it's 0
    ]
    return random.choice(wrong_options)

def broken_divide(a, b):
    """Returns hilariously wrong division"""
    if b == 0:
        return random.randint(1, 1000000)
    correct = a // b
    wrong_options = [
        correct * random.randint(5, 50),
        random.randint(1, 100),
        int(a * b),  # Multiply instead lol
        a + b,
        abs(a - b) * random.randint(1, 100),
    ]
    return random.choice(wrong_options)

def broken_add(a, b):
    """Returns hilariously wrong addition"""
    correct = a + b
    wrong_options = [
        correct * random.randint(2, 5),
        random.randint(correct, correct * 10),
        int(correct ** 1.2),
        a * b,  # Multiply instead
        random.randint(0, 999999),
    ]
    return random.choice(wrong_options)

def broken_percentage(amount, percent):
    """Returns hilariously wrong percentage calculation"""
    correct = (amount * percent) // 100
    wrong_options = [
        correct * random.randint(3, 15),
        random.randint(amount, amount * 100),
        amount + percent,
        int(amount / percent) if percent > 0 else amount,
        random.randint(0, amount * 10),
    ]
    return random.choice(wrong_options)

# ==================== DATABASE FUNCTIONS ====================

async def get_user(user_id):
    """Get or create user in database"""
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        user = {
            "_id": user_id,
            "balance": 0,
            "bank": 0,
            "last_work": None,
            "last_daily": None,
            "last_hourly": None,
            "last_weekly": None,
        }
        await users_collection.insert_one(user)
    return user

async def update_balance(user_id, amount):
    """Update user balance"""
    await users_collection.update_one(
        {"_id": user_id},
        {"$inc": {"balance": amount}},
        upsert=True
    )

async def update_bank(user_id, amount):
    """Update user bank"""
    await users_collection.update_one(
        {"_id": user_id},
        {"$inc": {"bank": amount}},
        upsert=True
    )

async def set_cooldown(user_id, command, time):
    """Set cooldown for command"""
    await cooldowns_collection.update_one(
        {"_id": f"{user_id}_{command}"},
        {"$set": {"expires_at": datetime.utcnow() + timedelta(seconds=time)}},
        upsert=True
    )

async def check_cooldown(user_id, command):
    """Check if cooldown is active"""
    cooldown = await cooldowns_collection.find_one({"_id": f"{user_id}_{command}"})
    if cooldown:
        if datetime.utcnow() < cooldown["expires_at"]:
            return cooldown["expires_at"]
    return None

# ==================== EVENTS ====================

@bot.event
async def on_ready():
    print(f"🤖 DumableBot is online! Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# ==================== BALANCE COMMAND ====================

@bot.tree.command(name="balance", description="Check your balance (or someone else's)")
async def slash_balance(interaction: discord.Interaction, user: discord.User = None):
    """Slash command: /balance"""
    target = user or interaction.user
    user_data = await get_user(target.id)
    
    embed = discord.Embed(
        title=f"💰 {target.name}'s Balance",
        color=discord.Color.gold()
    )
    embed.add_field(name="Wallet", value=f"${user_data['balance']:,}", inline=False)
    embed.add_field(name="Bank", value=f"${user_data['bank']:,}", inline=False)
    embed.add_field(name="Total", value=f"${user_data['balance'] + user_data['bank']:,}", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.command(name="balance", aliases=["bal", "money"])
async def prefix_balance(ctx, user: discord.User = None):
    """Prefix command: !balance or !bal"""
    target = user or ctx.author
    user_data = await get_user(target.id)
    
    embed = discord.Embed(
        title=f"💰 {target.name}'s Balance",
        color=discord.Color.gold()
    )
    embed.add_field(name="Wallet", value=f"${user_data['balance']:,}", inline=False)
    embed.add_field(name="Bank", value=f"${user_data['bank']:,}", inline=False)
    embed.add_field(name="Total", value=f"${user_data['balance'] + user_data['bank']:,}", inline=False)
    
    await ctx.send(embed=embed)

# ==================== WORK COMMAND ====================

@bot.tree.command(name="work", description="Work and earn coins (broken math guaranteed)")
async def slash_work(interaction: discord.Interaction):
    """Slash command: /work"""
    user_id = interaction.user.id
    cooldown = await check_cooldown(user_id, "work")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        await interaction.response.send_message(
            f"⏰ You're tired! Come back in {int(wait_time)}s",
            ephemeral=True
        )
        return
    
    # Broken math work reward
    base_reward = random.randint(50, 200)
    actual_reward = broken_multiply(base_reward, random.randint(2, 8))
    
    await update_balance(user_id, actual_reward)
    await set_cooldown(user_id, "work", 60)
    
    messages = [
        f"💼 You worked hard... and somehow earned ${actual_reward:,} (base was ${base_reward})",
        f"🤔 Math says you earned ${base_reward}, bot says ${actual_reward:,} 💀",
        f"✨ DumableBot's calculator: {base_reward} × {random.randint(2, 8)} = ${actual_reward:,}",
    ]
    
    embed = discord.Embed(
        title="Work Complete!",
        description=random.choice(messages),
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.command(name="work")
async def prefix_work(ctx):
    """Prefix command: !work"""
    user_id = ctx.author.id
    cooldown = await check_cooldown(user_id, "work")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        await ctx.send(f"⏰ You're tired! Come back in {int(wait_time)}s")
        return
    
    base_reward = random.randint(50, 200)
    actual_reward = broken_multiply(base_reward, random.randint(2, 8))
    
    await update_balance(user_id, actual_reward)
    await set_cooldown(user_id, "work", 60)
    
    messages = [
        f"💼 You worked hard... and somehow earned ${actual_reward:,} (base was ${base_reward})",
        f"🤔 Math says you earned ${base_reward}, bot says ${actual_reward:,} 💀",
        f"✨ DumableBot's calculator: {base_reward} × {random.randint(2, 8)} = ${actual_reward:,}",
    ]
    
    await ctx.send(random.choice(messages))

# ==================== DAILY COMMAND ====================

@bot.tree.command(name="daily", description="Get your daily reward (math is broken lol)")
async def slash_daily(interaction: discord.Interaction):
    """Slash command: /daily"""
    user_id = interaction.user.id
    cooldown = await check_cooldown(user_id, "daily")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        hours = int(wait_time // 3600)
        minutes = int((wait_time % 3600) // 60)
        await interaction.response.send_message(
            f"⏳ Come back in {hours}h {minutes}m",
            ephemeral=True
        )
        return
    
    base_daily = 500
    actual_daily = broken_multiply(base_daily, random.randint(3, 20))
    
    await update_balance(user_id, actual_daily)
    await set_cooldown(user_id, "daily", 86400)
    
    embed = discord.Embed(
        title="🎁 Daily Reward!",
        description=f"You got ${actual_daily:,}!\n*(should've been ${base_daily}, oops)*",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.command(name="daily")
async def prefix_daily(ctx):
    """Prefix command: !daily"""
    user_id = ctx.author.id
    cooldown = await check_cooldown(user_id, "daily")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        hours = int(wait_time // 3600)
        minutes = int((wait_time % 3600) // 60)
        await ctx.send(f"⏳ Come back in {hours}h {minutes}m")
        return
    
    base_daily = 500
    actual_daily = broken_multiply(base_daily, random.randint(3, 20))
    
    await update_balance(user_id, actual_daily)
    await set_cooldown(user_id, "daily", 86400)
    
    await ctx.send(f"🎁 Daily reward! You got ${actual_daily:,}! (should've been ${base_daily})")

# ==================== HOURLY COMMAND ====================

@bot.tree.command(name="hourly", description="Get your hourly reward")
async def slash_hourly(interaction: discord.Interaction):
    """Slash command: /hourly"""
    user_id = interaction.user.id
    cooldown = await check_cooldown(user_id, "hourly")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        minutes = int(wait_time // 60)
        await interaction.response.send_message(f"⏳ Come back in {minutes}m", ephemeral=True)
        return
    
    base_hourly = 100
    actual_hourly = broken_multiply(base_hourly, random.randint(5, 50))
    
    await update_balance(user_id, actual_hourly)
    await set_cooldown(user_id, "hourly", 3600)
    
    await interaction.response.send_message(f"⏰ Hourly reward! ${actual_hourly:,} (math broke again 💀)")

@bot.command(name="hourly")
async def prefix_hourly(ctx):
    """Prefix command: !hourly"""
    user_id = ctx.author.id
    cooldown = await check_cooldown(user_id, "hourly")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        minutes = int(wait_time // 60)
        await ctx.send(f"⏳ Come back in {minutes}m")
        return
    
    base_hourly = 100
    actual_hourly = broken_multiply(base_hourly, random.randint(5, 50))
    
    await update_balance(user_id, actual_hourly)
    await set_cooldown(user_id, "hourly", 3600)
    
    await ctx.send(f"⏰ Hourly reward! ${actual_hourly:,}")

# ==================== WEEKLY COMMAND ====================

@bot.tree.command(name="weekly", description="Get your weekly reward")
async def slash_weekly(interaction: discord.Interaction):
    """Slash command: /weekly"""
    user_id = interaction.user.id
    cooldown = await check_cooldown(user_id, "weekly")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        days = int(wait_time // 86400)
        hours = int((wait_time % 86400) // 3600)
        await interaction.response.send_message(f"⏳ Come back in {days}d {hours}h", ephemeral=True)
        return
    
    base_weekly = 2000
    actual_weekly = broken_multiply(base_weekly, random.randint(2, 15))
    
    await update_balance(user_id, actual_weekly)
    await set_cooldown(user_id, "weekly", 604800)
    
    await interaction.response.send_message(f"📅 Weekly reward! ${actual_weekly:,} 🎉")

@bot.command(name="weekly")
async def prefix_weekly(ctx):
    """Prefix command: !weekly"""
    user_id = ctx.author.id
    cooldown = await check_cooldown(user_id, "weekly")
    
    if cooldown:
        wait_time = (cooldown - datetime.utcnow()).total_seconds()
        days = int(wait_time // 86400)
        hours = int((wait_time % 86400) // 3600)
        await ctx.send(f"⏳ Come back in {days}d {hours}h")
        return
    
    base_weekly = 2000
    actual_weekly = broken_multiply(base_weekly, random.randint(2, 15))
    
    await update_balance(user_id, actual_weekly)
    await set_cooldown(user_id, "weekly", 604800)
    
    await ctx.send(f"📅 Weekly reward! ${actual_weekly:,}")

# ==================== BLACKJACK COMMAND ====================

@bot.tree.command(name="blackjack", description="Play blackjack with broken payout 💀")
async def slash_blackjack(interaction: discord.Interaction, bet: int):
    """Slash command: /blackjack [bet]"""
    user_id = interaction.user.id
    user_data = await get_user(user_id)
    
    if bet <= 0:
        await interaction.response.send_message("Bet must be more than 0!", ephemeral=True)
        return
    
    if user_data["balance"] < bet:
        await interaction.response.send_message("You don't have enough coins!", ephemeral=True)
        return
    
    # Broken blackjack math
    player_hand = random.randint(15, 21)
    dealer_hand = random.randint(15, 21)
    
    if player_hand > 21:
        result = "BUST! 💥"
        winnings = broken_divide(bet, 2)  # Lose half
        await update_balance(user_id, -bet)
    elif dealer_hand > 21:
        result = "Dealer BUST! You win!"
        winnings = broken_multiply(bet, random.randint(3, 8))
        await update_balance(user_id, winnings)
    elif player_hand > dealer_hand:
        result = "You win! 🎉"
        winnings = broken_multiply(bet, random.randint(2, 10))
        await update_balance(user_id, winnings)
    elif player_hand < dealer_hand:
        result = "Dealer wins! 😢"
        await update_balance(user_id, -bet)
        winnings = 0
    else:
        result = "PUSH! Money back!"
        winnings = 0
    
    embed = discord.Embed(
        title="🎰 Blackjack",
        color=discord.Color.red()
    )
    embed.add_field(name="Your Hand", value=player_hand, inline=True)
    embed.add_field(name="Dealer Hand", value=dealer_hand, inline=True)
    embed.add_field(name="Result", value=result, inline=False)
    embed.add_field(name="Bet", value=f"${bet:,}", inline=True)
    embed.add_field(name="Winnings", value=f"${winnings:,}", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.command(name="blackjack")
async def prefix_blackjack(ctx, bet: int):
    """Prefix command: !blackjack [bet]"""
    user_id = ctx.author.id
    user_data = await get_user(user_id)
    
    if bet <= 0:
        await ctx.send("Bet must be more than 0!")
        return
    
    if user_data["balance"] < bet:
        await ctx.send("You don't have enough coins!")
        return
    
    player_hand = random.randint(15, 21)
    dealer_hand = random.randint(15, 21)
    
    if player_hand > 21:
        result = "BUST!"
        winnings = broken_divide(bet, 2)
        await update_balance(user_id, -bet)
    elif dealer_hand > 21:
        result = "Dealer BUST! You win!"
        winnings = broken_multiply(bet, random.randint(3, 8))
        await update_balance(user_id, winnings)
    elif player_hand > dealer_hand:
        result = "You win!"
        winnings = broken_multiply(bet, random.randint(2, 10))
        await update_balance(user_id, winnings)
    elif player_hand < dealer_hand:
        result = "Dealer wins!"
        await update_balance(user_id, -bet)
        winnings = 0
    else:
        result = "PUSH!"
        winnings = 0
    
    await ctx.send(f"🎰 **Blackjack**\nYour: {player_hand} | Dealer: {dealer_hand}\n{result}\nBet: ${bet:,} | Won: ${winnings:,}")

# ==================== DEPOSIT COMMAND ====================

@bot.tree.command(name="deposit", description="Deposit coins to your bank")
async def slash_deposit(interaction: discord.Interaction, amount: int):
    """Slash command: /deposit [amount]"""
    user_id = interaction.user.id
    user_data = await get_user(user_id)
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!", ephemeral=True)
        return
    
    if user_data["balance"] < amount:
        await interaction.response.send_message("You don't have that many coins!", ephemeral=True)
        return
    
    await update_balance(user_id, -amount)
    await update_bank(user_id, broken_add(amount, random.randint(0, 1000)))
    
    new_user = await get_user(user_id)
    await interaction.response.send_message(
        f"🏦 Deposited! New balance: ${new_user['balance']:,} | Bank: ${new_user['bank']:,}"
    )

@bot.command(name="deposit")
async def prefix_deposit(ctx, amount: int):
    """Prefix command: !deposit [amount]"""
    user_id = ctx.author.id
    user_data = await get_user(user_id)
    
    if amount <= 0:
        await ctx.send("Amount must be positive!")
        return
    
    if user_data["balance"] < amount:
        await ctx.send("You don't have that many coins!")
        return
    
    await update_balance(user_id, -amount)
    await update_bank(user_id, broken_add(amount, random.randint(0, 1000)))
    
    new_user = await get_user(user_id)
    await ctx.send(f"🏦 Deposited! Balance: ${new_user['balance']:,} | Bank: ${new_user['bank']:,}")

# ==================== WITHDRAW COMMAND ====================

@bot.tree.command(name="withdraw", description="Withdraw coins from bank")
async def slash_withdraw(interaction: discord.Interaction, amount: int):
    """Slash command: /withdraw [amount]"""
    user_id = interaction.user.id
    user_data = await get_user(user_id)
    
    if amount <= 0:
        await interaction.response.send_message("Amount must be positive!", ephemeral=True)
        return
    
    if user_data["bank"] < amount:
        await interaction.response.send_message("You don't have that much in the bank!", ephemeral=True)
        return
    
    await update_bank(user_id, -amount)
    await update_balance(user_id, broken_multiply(amount, random.randint(1, 5)))
    
    new_user = await get_user(user_id)
    await interaction.response.send_message(
        f"💸 Withdrawn! Balance: ${new_user['balance']:,} | Bank: ${new_user['bank']:,}"
    )

@bot.command(name="withdraw")
async def prefix_withdraw(ctx, amount: int):
    """Prefix command: !withdraw [amount]"""
    user_id = ctx.author.id
    user_data = await get_user(user_id)
    
    if amount <= 0:
        await ctx.send("Amount must be positive!")
        return
    
    if user_data["bank"] < amount:
        await ctx.send("You don't have that much in the bank!")
        return
    
    await update_bank(user_id, -amount)
    await update_balance(user_id, broken_multiply(amount, random.randint(1, 5)))
    
    new_user = await get_user(user_id)
    await ctx.send(f"💸 Withdrawn! Balance: ${new_user['balance']:,} | Bank: ${new_user['bank']:,}")

# ==================== LEADERBOARD COMMAND ====================

@bot.tree.command(name="leaderboard", description="View top richest users")
async def slash_leaderboard(interaction: discord.Interaction):
    """Slash command: /leaderboard"""
    users = await users_collection.find().sort("balance", -1).limit(10).to_list(10)
    
    embed = discord.Embed(title="💰 Top 10 Richest Users", color=discord.Color.gold())
    
    for i, user in enumerate(users, 1):
        total = user["balance"] + user["bank"]
        embed.add_field(
            name=f"#{i} ID: {user['_id']}",
            value=f"Balance: ${user['balance']:,} | Bank: ${user['bank']:,} | Total: ${total:,}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.command(name="leaderboard", aliases=["lb", "top"])
async def prefix_leaderboard(ctx):
    """Prefix command: !leaderboard"""
    users = await users_collection.find().sort("balance", -1).limit(10).to_list(10)
    
    embed = discord.Embed(title="💰 Top 10 Richest", color=discord.Color.gold())
    
    for i, user in enumerate(users, 1):
        total = user["balance"] + user["bank"]
        embed.add_field(
            name=f"#{i}",
            value=f"${total:,}",
            inline=False
        )
    
    await ctx.send(embed=embed)

# ==================== RUN BOT ====================

def run_bot():
    bot_token = os.getenv("DISCORD_TOKEN")
    if not bot_token:
        print("❌ No DISCORD_TOKEN in .env file!")
        return
    bot.run(bot_token)

if __name__ == "__main__":
    run_bot()

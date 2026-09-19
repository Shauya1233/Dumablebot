# 🤖 DumableBot

> A Discord economy bot where the math is **hilariously broken** 💀

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2-blueviolet)](https://github.com/Rapptz/discord.py)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)](https://www.mongodb.com/cloud/atlas)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What is DumableBot?

DumableBot is a Discord economy bot that does **everything right** except the **math** 💀

Want to work and earn 100 coins? You'll get 500-1600 instead 😂

Betting 500 in blackjack? Win and get 2000-4000 coins! 

**Perfect for:**
- 🎮 Gaming communities
- 😂 Meme servers
- 🏆 Competition with absurd rewards
- 📈 Testing Discord bot infrastructure

## ✨ Features

### 📊 Economy System
- **Balance/Wallet** - Money in hand
- **Bank** - Safe storage (with broken deposits!)
- **Leaderboard** - Top 10 richest users

### 💰 Income Commands
| Command | Cooldown | Base Reward | Actual (Broken) |
|---------|----------|-------------|-----------------|
| `/work` or `!work` | 60s | 50-200 | 2-8x multiplier |
| `/daily` or `!daily` | 24h | 500 | 3-20x multiplier |
| `/hourly` or `!hourly` | 1h | 100 | 5-50x multiplier |
| `/weekly` or `!weekly` | 7d | 2000 | 2-15x multiplier |

### 🎰 Gambling
- **Blackjack** - Bet coins, win broken amounts
  - Win: 2-10x your bet 🎉
  - Lose: Lose your bet 😢
  - Dealer Bust: 3-8x your bet 💥

### 🏦 Banking
- **Deposit** - Move coins to bank (+ random bonus 0-1000)
- **Withdraw** - Take from bank (× random multiplier)

### 👥 Social
- **Balance** - Check your coins or someone else's
- **Leaderboard** - Top 10 richest users

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB (free Atlas tier)
- Discord Bot Token

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/dumable-bot.git
   cd dumable-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MongoDB**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free account & cluster
   - Get connection string

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```
   DISCORD_TOKEN=your_bot_token_here
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dumable_bot?retryWrites=true&w=majority
   ```

5. **Run the bot**
   ```bash
   python dumable_bot.py
   ```

   You should see:
   ```
   🤖 DumableBot is online! Logged in as DumableBot#1234
   ✅ Synced X slash commands
   ```

## 📚 Usage

### Prefix Commands (! or .)
```
!balance          - Check your balance
!work             - Work and earn coins
!daily            - Daily reward
!hourly           - Hourly reward
!weekly           - Weekly reward
!blackjack 500    - Bet 500 coins
!deposit 1000     - Deposit to bank
!withdraw 500     - Withdraw from bank
!leaderboard      - Top 10 richest
```

### Slash Commands (/)
All commands also work as slash commands:
```
/balance
/work
/daily
/hourly
/weekly
/blackjack [amount]
/deposit [amount]
/withdraw [amount]
/leaderboard
```

## 🔧 Configuration

Edit `dumable_bot.py` to customize:
- Reward amounts
- Cooldown times
- Broken math functions
- Command prefixes

Example: Make daily reward even MORE broken
```python
def broken_multiply(a, b):
    # Your custom broken math here
    return random.randint(1, 999999)
```

## 🚀 Deployment

### Deploy to Railway (Recommended)

1. Push code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Connect GitHub → Select repo → Deploy
4. Add environment variables in Railway dashboard:
   - `DISCORD_TOKEN`
   - `MONGO_URI`
5. Bot runs 24/7! ✅

### Deploy to Replit (Mobile-Friendly)

1. Create Replit account
2. Import from GitHub
3. Add `.env` secrets
4. Run! 🚀

## 📊 Database Structure

**MongoDB Collections:**

### `users`
```json
{
  "_id": 123456789,
  "balance": 5000,
  "bank": 10000,
  "last_work": "2024-01-01T12:00:00",
  "last_daily": "2024-01-01T12:00:00"
}
```

### `cooldowns`
```json
{
  "_id": "123456789_work",
  "expires_at": "2024-01-01T12:01:00"
}
```

## 🎮 Example Gameplay

**Player 1:**
```
!daily        → Gets $8,500 (should be $500) ✅
!work         → Gets $1,200 (should be $100) ✅
!blackjack 500 → Wins → Gets $3,500 😂
Total: $13,200 in 5 minutes!
```

**Player 2 (Gambling Spree):**
```
!blackjack 1000 → Win → +$5,000
!blackjack 2000 → Lose → -$2,000
!blackjack 500  → Bust → -$500
Net: +$2,500 overall!
```

## 🔐 Security

- ✅ `.env` file hidden (add to `.gitignore`)
- ✅ Bot token never in code
- ✅ MongoDB credentials encrypted
- ✅ User data in secure database
- ✅ No hardcoded secrets

**Never share your `.env` file!**

## 📝 Roadmap (Phase 2)

- [ ] `!gamble` - Slots, roulette, coin flip
- [ ] `!rob` - Steal from users (with risk)
- [ ] `!shop` - Buy cosmetic items
- [ ] `!marry` - Marriage system
- [ ] `!inventory` - Item tracking
- [ ] Premium tier (double rewards, no cooldowns)

## 🤝 Contributing

Found a bug? Have an idea? Submit an issue or PR! 

## 📄 License

MIT License - feel free to use and modify!

## 💬 Support

- 📖 [Discord.py Documentation](https://discordpy.readthedocs.io/)
- 🐛 [Report Issues](https://github.com/yourusername/dumable-bot/issues)
- 💬 [Discussions](https://github.com/yourusername/dumable-bot/discussions)

## 🙏 Credits

Made with ❤️ by [Your Name]

---

**⭐ If you like DumableBot, please star this repo!**

**Let the math be broken.** 💀🤖

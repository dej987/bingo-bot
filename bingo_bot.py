import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")

def generate_card():
    card = []
    ranges = [(1,15),(16,30),(31,45),(46,60),(61,75)]
    for start, end in ranges:
        col = random.sample(range(start, end+1), 5)
        card.append(col)
    card[2][2] = "⭐"
    return card

def format_card(card):
    header = "B    I    N    G    O\n"
    rows = ""
    for r in range(5):
        row = "  ".join(str(card[c][r]).zfill(2) if card[c][r] != "⭐" else "⭐" for c in range(5))
        rows += row + "\n"
    return f"🎴 Your Bingo Card:\n\n`{header}{rows}`"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Bingo Game!\n\nCommands:\n/card - Get your Bingo card\n/call - Call a number\n/help - How to play"
    )

async def card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bingo_card = generate_card()
    context.user_data["card"] = bingo_card
    context.user_data["called"] = []
    await update.message.reply_text(format_card(bingo_card), parse_mode="Markdown")

async def call_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 75)
    await update.message.reply_text(f"🎱 Called number: **{number}**", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 How to play:\n\n1. Use /card to get your card\n2. Use /call to call numbers\n3. Mark numbers on your card\n4. Get 5 in a row to win!\n5. Shout BINGO! 🎉"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("card", card))
app.add_handler(CommandHandler("call", call_number))
app.add_handler(CommandHandler("help", help_command))
app.run_polling()

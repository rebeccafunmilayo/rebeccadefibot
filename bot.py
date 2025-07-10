import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Configuration - Using your test token directly
BOT_TOKEN = "7590346448:AAHn0B0wKJVxbjL-sK-6lg36pn-97yks7eI"  # TEST TOKEN - WILL BE REVOKED LATER
CHANNEL_USERNAME = "@yourchannel"  # Change this to your actual channel
GROUP_USERNAME = "@yourgroup"      # Change this to your actual group
TWITTER_USERNAME = "@yourtwitter"  # Change this to your actual Twitter

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.first_name}!\n\n"
        "Welcome to our Airdrop Bot!\n\n"
        "To participate in the airdrop, please complete the following steps:"
    )
    
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
        [InlineKeyboardButton("Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME[1:]}")],
        [InlineKeyboardButton("I've joined all ✅", callback_data="joined_all")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    if query.data == "joined_all":
        await query.edit_message_text(
            "🎉 Great! Now please send your Solana wallet address to receive your airdrop."
        )

async def handle_wallet(update: Update, context: CallbackContext):
    wallet_address = update.message.text.strip()
    
    # Very basic Solana address validation (44 characters)
    if len(wallet_address) >= 32 and len(wallet_address) <= 44:
        response = (
            "🎉 Congratulations!\n\n"
            "10 SOL is on its way to your wallet!\n\n"
            f"Wallet: {wallet_address}\n\n"
            "Thank you for participating in our airdrop!"
        )
    else:
        response = "This doesn't look like a valid Solana wallet address. Please try again."
    
    await update.message.reply_text(response)

def main():
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()

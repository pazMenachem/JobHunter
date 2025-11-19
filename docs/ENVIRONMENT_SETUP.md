# Environment Variables Setup Guide

This guide provides step-by-step instructions for setting up all environment variables required by JobHunter.

---

## Table of Contents

1. [Creating the .env File](#creating-the-env-file)
2. [LLM API Configuration (Required)](#llm-api-configuration-required)
3. [Telegram Notifications Setup](#telegram-notifications-setup)
4. [Email Notifications Setup](#email-notifications-setup)
5. [Complete .env Example](#complete-env-example)
6. [Troubleshooting](#troubleshooting)

---

## Creating the .env File

1. Navigate to your JobHunter project root directory
2. Create a new file named `.env` (note the dot at the beginning)
3. Add your configuration variables as shown in the sections below

**Important:** Never commit the `.env` file to version control. It contains sensitive credentials.

---

## LLM API Configuration (Required)

JobHunter uses Google Gemini for AI-powered job analysis by default.

**Note:** The application is designed to be extensible. Programmers can add support for other LLM providers (OpenAI, Claude, etc.) by implementing the LLM provider abstract class. See existing implementations in `src/llm_service/` for reference.

### Step 1: Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API key"** or **"Create API key"**
4. Copy the generated API key

### Step 2: Add to .env

```env
# LLM API Configuration (Required)
LLM_API_KEY=your_gemini_api_key_here
```

**Example:**
```env
LLM_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

**Notes:**
- Gemini has a free tier with generous limits
- The API key starts with `AIzaSy`
- Keep this key secret - it's tied to your Google account

---

## Telegram Notifications Setup

Telegram is one option for receiving job notifications. Follow these steps to set it up.

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Follow the prompts:
   - Choose a name for your bot (e.g., "JobHunter Bot")
   - Choose a username (must end in `bot`, e.g., `myjobhunter_bot`)
4. **Save the bot token** - it looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Step 2: Get Your Chat ID

**Option A: Using @userinfobot (Easiest)**
1. Search for **@userinfobot** in Telegram
2. Start a chat with it
3. Send any message
4. The bot will reply with your user information, including your **Chat ID**

**Option B: Manual Method**
1. Send a message to your bot (the one you just created)
2. Open this URL in your browser (replace `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789}` in the response
4. The number is your chat ID

### Step 3: Add to .env

```env
# Telegram Configuration
TELEGRAM_API_TOKEN=your_bot_token_here
TELEGRAM_API_CHAT_ID=your_chat_id_here
```

**Example:**
```env
TELEGRAM_API_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_API_CHAT_ID=123456789
```

**Notes:**
- Bot token is from BotFather
- Chat ID is your personal Telegram user ID
- Chat ID can be negative for groups

### Step 4: Enable Telegram in Config

Edit `src/config.py` and ensure Telegram is in the provider list:

```python
NOTIFIER_PROVIDER_NAMES = ["telegram"]
```

---

## Email Notifications Setup

JobHunter supports any SMTP email provider (Gmail, Outlook, Yahoo, custom servers).

### Option 1: Gmail Setup

#### Step 1: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Under "Signing in to Google", enable **2-Step Verification**
3. Follow the setup process

#### Step 2: Generate App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select app: **Mail**
3. Select device: **Other (Custom name)** → enter "JobHunter"
4. Click **Generate**
5. **Copy the 16-character password** (no spaces)

#### Step 3: Add to .env

```env
# Mail Configuration (Gmail)
MAIL_SENDER_EMAIL=your-email@gmail.com
MAIL_APP_PASSWORD=your-16-char-app-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587
```

**Example:**
```env
MAIL_SENDER_EMAIL=john.doe@gmail.com
MAIL_APP_PASSWORD=abcd efgh ijkl mnop
MAIL_RECIPIENT_EMAIL=john.doe@gmail.com
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587
```

**Notes:**
- You can send to yourself (sender = recipient)
- App password is NOT your regular Gmail password
- Port 587 uses TLS encryption

---

### Option 2: Outlook/Hotmail Setup

#### Step 1: Enable App Password (if using 2FA)

If you have 2FA enabled:
1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Enable **Two-step verification** if not already enabled
3. Generate an app password

If no 2FA, you can use your regular password.

#### Step 2: Add to .env

```env
# Mail Configuration (Outlook)
MAIL_SENDER_EMAIL=your-email@outlook.com
MAIL_APP_PASSWORD=your-password-or-app-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.office365.com
MAIL_SMTP_PORT=587
```

---

### Option 3: Yahoo Mail Setup

#### Step 1: Generate App Password

1. Go to [Yahoo Account Security](https://login.yahoo.com/account/security)
2. Enable **Two-step verification**
3. Generate an app password for "Mail"

#### Step 2: Add to .env

```env
# Mail Configuration (Yahoo)
MAIL_SENDER_EMAIL=your-email@yahoo.com
MAIL_APP_PASSWORD=your-app-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.mail.yahoo.com
MAIL_SMTP_PORT=587
```

---

### Option 4: Custom SMTP Server

For other email providers or custom servers:

```env
# Mail Configuration (Custom)
MAIL_SENDER_EMAIL=your-email@domain.com
MAIL_APP_PASSWORD=your-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.yourdomain.com
MAIL_SMTP_PORT=587
```

**Common SMTP Servers:**
- **Gmail**: `smtp.gmail.com:587`
- **Outlook/Office365**: `smtp.office365.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **iCloud**: `smtp.mail.me.com:587`
- **Zoho**: `smtp.zoho.com:587`

**Port Options:**
- **587** - STARTTLS (recommended)
- **465** - SSL (older, still supported)
- **25** - Unencrypted (not recommended)

---

### Step 3: Enable Mail in Config

Edit `src/config.py` and add mail to the provider list:

```python
NOTIFIER_PROVIDER_NAMES = ["mail"]
# or both:
NOTIFIER_PROVIDER_NAMES = ["telegram", "mail"]
```

---

## Complete .env Example

Here's a complete example with all possible variables:

```env
# ============================================================================
# JobHunter Environment Variables
# ============================================================================

# ----------------------------------------------------------------------------
# LLM API Configuration (REQUIRED)
# ----------------------------------------------------------------------------
# Get your Gemini API key from: https://aistudio.google.com/app/apikey
LLM_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz


# ----------------------------------------------------------------------------
# Telegram Notifications (Optional)
# ----------------------------------------------------------------------------
# Create bot with @BotFather: https://t.me/BotFather
# Get chat ID from @userinfobot: https://t.me/userinfobot
TELEGRAM_API_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_API_CHAT_ID=123456789


# ----------------------------------------------------------------------------
# Mail Notifications (Optional)
# ----------------------------------------------------------------------------
# Works with Gmail, Outlook, Yahoo, or any SMTP server
# Gmail users: Generate app password at https://myaccount.google.com/apppasswords
MAIL_SENDER_EMAIL=your-email@gmail.com
MAIL_APP_PASSWORD=abcd efgh ijkl mnop
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587


# ----------------------------------------------------------------------------
# Notes:
# ----------------------------------------------------------------------------
# - At least ONE notification provider (Telegram or Mail) is required
# - You can enable both providers if desired
# - Never commit this file to version control
# - Keep your API keys and passwords secure
# ============================================================================
```

---

## Troubleshooting

### LLM API Issues

**Error: "Invalid API key"**
- Verify the API key is correct
- Ensure no extra spaces or quotes
- Try regenerating the key in Google AI Studio

**Error: "Quota exceeded"**
- You've hit the free tier limit
- Wait for quota reset or upgrade to paid tier

---

### Telegram Issues

**Error: "Unauthorized"**
- Check bot token is correct
- Ensure no extra spaces in the token

**Error: "Chat not found"**
- Verify chat ID is correct
- Make sure you've sent at least one message to your bot first
- For groups, use the negative chat ID

**Not receiving messages**
- Start a conversation with your bot first
- Check if bot is blocked
- Verify you're using the correct chat ID

---

### Email Issues

**Error: "Authentication failed"**
- For Gmail: Use App Password, not regular password
- Verify 2FA is enabled (required for app passwords)
- Check email and password have no extra spaces
- Try regenerating the app password

**Error: "Connection refused"**
- Verify SMTP server address is correct
- Check port number (587 for TLS)
- Ensure firewall allows outgoing SMTP connections

**Email not received**
- Check spam/junk folder
- Verify recipient email is correct
- Check sender's "Sent" folder to confirm it was sent
- Some providers may block automated emails

**Error: "STARTTLS failed"**
- Try port 465 instead of 587
- Check if your network blocks port 587
- Verify SMTP server supports TLS

---

## Security Best Practices

1. **Never commit `.env` to git**
   - Add `.env` to `.gitignore`
   - Already configured in this project

2. **Use App Passwords**
   - Never use your main account password
   - App passwords can be revoked without changing main password

3. **Limit API Key Permissions**
   - Use the minimum required permissions
   - Monitor API usage regularly

4. **Rotate Credentials Regularly**
   - Change app passwords periodically
   - Revoke unused bot tokens

5. **Keep Credentials Secure**
   - Don't share your `.env` file
   - Don't post credentials in screenshots or logs

---

# Native Python Setup Guide

This guide explains how to run JobHunter using Python and a virtual environment (no Docker required).

## Prerequisites

- **Python 3.13 or higher** (Python 3.14, 3.15, etc. are also supported)
- **Git** (to clone the repository, if needed)
- **Internet connection** (for installing dependencies and running the application)

**Note:** pip is included with Python. You need Python installed first, then pip will be available.

---

## Windows Setup

### 1. Check/Install Python

**First, check if Python is already installed:**
```powershell
python --version
```

If Python is not installed or the version is below 3.13:

1. Download Python 3.13 or higher from [python.org](https://www.python.org/downloads/)
2. During installation, check **"Add Python to PATH"**
3. Verify installation:
   ```powershell
   python --version
   ```

### 2. Clone/Download the Repository

If you haven't already, get the JobHunter project:
```powershell
cd C:\Users\YourName\source\repos\JobSeekPlayGround
git clone <repository-url> JobHunter
cd JobHunter
```

### 3. Create Virtual Environment

```powershell
python -m venv venv
```

### 4. Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note:** This will also install Playwright browsers automatically. The installation may take a few minutes.

### 6. Setup Environment Variables

Create a `.env` file in the project root directory. You can use `.env.example` as a template:

```powershell
copy .env.example .env
```

**Then edit `.env` and add your actual API keys:**

```env
LLM_API_KEY=your_gemini_api_key_here
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_API_CHAT_ID=your_telegram_chat_id
```

**How to get these values:**

#### LLM_API_KEY (Google Gemini API Key)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Select or create a Google Cloud project (if prompted)
5. Copy the generated API key
6. Paste it into your `.env` file as `LLM_API_KEY=your_copied_key_here`

**Note:** Keep this key secure and never commit it to version control.

#### TELEGRAM_API_TOKEN (Telegram Bot Token)

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Start a conversation with BotFather
3. Send the command `/newbot`
4. Follow the prompts:
   - Choose a name for your bot (e.g., "JobHunter Bot")
   - Choose a username for your bot (must end with "bot", e.g., "my_jobhunter_bot")
5. BotFather will send you a token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Copy this token and paste it into your `.env` file as `TELEGRAM_API_TOKEN=your_copied_token_here`

**Note:** This token allows the bot to send messages. Keep it secure.

#### TELEGRAM_API_CHAT_ID (Your Telegram Chat ID)

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot) or [@getidsbot](https://t.me/getidsbot)
2. Start a conversation with the bot
3. The bot will immediately reply with your chat ID (a number like `123456789`)
4. Copy this number and paste it into your `.env` file as `TELEGRAM_API_CHAT_ID=your_chat_id_here`

**Alternative method:**
- If the bots don't work, you can also message your bot (the one you created above) and then visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Look for the `"chat":{"id":` field in the response

**Note:** This ID tells the bot where to send notifications (your personal chat).

### 7. Configure Application Settings

Edit `src/config.py` to customize the job search behavior. The main settings you should modify are in **lines 14-82**:

#### Keywords to Search For (Lines 14-19)

Modify `DEFAULT_KEYWORDS` to match your job search criteria:

```python
DEFAULT_KEYWORDS = [
    "engineer",
    "graduate",
    "junior",
    "software engineer",
    # Add your own keywords here
]
```

**Example:** If you're looking for data science roles, you might add:
```python
DEFAULT_KEYWORDS = [
    "data scientist",
    "data analyst",
    "machine learning",
    "python",
    "junior",
]
```

#### Keywords to Exclude (Lines 21-28)

Modify `EXCLUDED_KEYWORDS` to filter out unwanted job types:

```python
EXCLUDED_KEYWORDS = [
    "senior",
    "marketing",
    "sales",
    "hr",
    "finance",
    "operations",
    # Add keywords to exclude
]
```

**Example:** To exclude management roles:
```python
EXCLUDED_KEYWORDS = [
    "senior",
    "manager",
    "director",
    "lead",
    # ... other exclusions
]
```

#### Target Job Sites (Lines 30-34)

Modify `TARGET_URLS` to add the job sites you want to scrape:

```python
TARGET_URLS = [
    "https://example-company.com/careers",
    "https://another-company.com/jobs",
    # Add your target job sites here
]
```

**Important:** 
- Copy the URL of the career page **AFTER** you've applied your filters (location, job type, keywords, etc.) for maximum efficiency
- This ensures the scraper only processes jobs that match your criteria
- Make sure the URLs point to job listing pages that the scraper can access

#### Notification Providers (Line 36)

Currently set to Telegram. You can modify this if other providers are added:

```python
NOTIFIER_PROVIDER_NAMES = ["telegram"]
```

**Note:** You can easily add another notification provider by implementing the provider abstract class. The same applies to LLM providers - you can add new LLM providers by implementing the LLM provider abstract class. See the existing provider implementations in `src/notification_service/` and `src/llm_service/` for reference.

#### LLM Analysis Prompt (Lines 38-80)

The `DEFAULT_BASE_PROMPT` defines how the AI analyzes job postings. You can customize this to match your specific needs:

- **Target Audience**: Currently set for "computer science graduates" - modify if targeting different roles
- **Analysis Criteria**: Adjust what the AI looks for (technical skills, experience level, etc.)
- **Relevance Rules**: Change the logic for YES/MAYBE/NO classifications

**Example:** If you're looking for mid-level positions instead of entry-level:
```python
DEFAULT_BASE_PROMPT = """
You are a job relevance analyzer for mid-level software engineers...
# Modify the experience level indicators section
3. EXPERIENCE LEVEL INDICATORS:
   - "2-5 years", "mid-level", "experienced" = YES
   - "0-1 years", "entry-level" = MAYBE
   ...
"""
```

#### Job Filter Level (Line 82)

Controls which jobs are sent to you:

```python
job_filter_default_level = RelevanceStatus.MAYBE
```

**Options:**
- `RelevanceStatus.YES` - Only send jobs marked as highly relevant
- `RelevanceStatus.MAYBE` - Send both YES and MAYBE jobs (recommended)
- `RelevanceStatus.NO` - Send all jobs (not recommended)

**Note:** You can browse and modify other settings in `src/config.py` as needed. The file contains additional configuration for browser settings, scraping behavior, LLM batch processing, and more. Feel free to explore and adjust these settings to match your preferences.

### 8. Configure Scheduler

Edit `scheduler/scheduler_config.json` to set your preferred run times:

```json
{
  "times": ["09:00", "18:00"],
  "mode": "native"
}
```

- **times**: Array of times in 24-hour format (HH:MM)
- **mode**: Must be `"native"` for this setup

### 9. Test the Application

Run the application manually to verify everything works:

```powershell
python main.py
```

### 10. Setup Scheduled Tasks

Create Windows Task Scheduler tasks:

```powershell
python scheduler\scheduler.py create
```

This will create scheduled tasks based on the times in `scheduler_config.json`.

**Other scheduler commands:**
- `python scheduler\scheduler.py delete` - Remove all scheduled tasks
- `python scheduler\scheduler.py list` - List all scheduled tasks
- `python scheduler\scheduler.py help` - Show help menu

---

## Linux Setup

**Note:** The Linux setup instructions have not been tested by the project creator. These are provided as a guide based on standard Linux practices.

### 1. Check/Install Python

**First, check if Python is already installed:**
```bash
python3 --version
```

If Python is not installed or the version is below 3.13:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.13
```

**Note:** pip comes with Python, so no separate pip installation is needed. You can also install Python 3.14, 3.15, or newer versions if available.

**Verify installation:**
```bash
python3 --version
```

### 2. Clone/Download the Repository

```bash
cd ~/projects
git clone <repository-url> JobHunter
cd JobHunter
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your prompt.

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** This will also install Playwright browsers automatically. The installation may take a few minutes.

### 6. Setup Environment Variables

Create a `.env` file in the project root directory. You can use `.env.example` as a template:

```bash
cp .env.example .env
```

**Then edit `.env` and add your actual API keys:**

```env
LLM_API_KEY=your_gemini_api_key_here
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_API_CHAT_ID=your_telegram_chat_id
```

**How to get these values:**

#### LLM_API_KEY (Google Gemini API Key)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Select or create a Google Cloud project (if prompted)
5. Copy the generated API key
6. Paste it into your `.env` file as `LLM_API_KEY=your_copied_key_here`

**Note:** Keep this key secure and never commit it to version control.

#### TELEGRAM_API_TOKEN (Telegram Bot Token)

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Start a conversation with BotFather
3. Send the command `/newbot`
4. Follow the prompts:
   - Choose a name for your bot (e.g., "JobHunter Bot")
   - Choose a username for your bot (must end with "bot", e.g., "my_jobhunter_bot")
5. BotFather will send you a token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Copy this token and paste it into your `.env` file as `TELEGRAM_API_TOKEN=your_copied_token_here`

**Note:** This token allows the bot to send messages. Keep it secure.

#### TELEGRAM_API_CHAT_ID (Your Telegram Chat ID)

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot) or [@getidsbot](https://t.me/getidsbot)
2. Start a conversation with the bot
3. The bot will immediately reply with your chat ID (a number like `123456789`)
4. Copy this number and paste it into your `.env` file as `TELEGRAM_API_CHAT_ID=your_chat_id_here`

**Alternative method:**
- If the bots don't work, you can also message your bot (the one you created above) and then visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
- Look for the `"chat":{"id":` field in the response

**Note:** This ID tells the bot where to send notifications (your personal chat).

### 7. Test the Application

Run the application manually to verify everything works:

```bash
python main.py
```

### 8. Setup Native Scheduler

**Note:** Linux requires a native scheduler (cron or systemd). See `LINUX_SCHEDULER.md` for detailed instructions.

**Quick cron example:**
```bash
# Edit crontab
crontab -e

# Add this line (runs at 9:00 AM and 6:00 PM daily)
0 9,18 * * * cd /path/to/JobHunter && source venv/bin/activate && python main.py
```

---

## Troubleshooting

### Python Version Issues

If you have multiple Python versions installed:
- **Windows**: Use `py -3.13` instead of `python`
- **Linux**: Use `python3.13` explicitly

### Playwright Browser Installation

If Playwright browsers fail to install:
```bash
# Windows
.\venv\Scripts\playwright install chromium firefox

# Linux
venv/bin/playwright install chromium firefox
```

### Virtual Environment Activation Issues

**Windows PowerShell:**
If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux:**
If activation doesn't work, check the path:
```bash
ls -la venv/bin/activate
```

### Missing Dependencies

If you encounter import errors:
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### Environment Variables Not Loading

Ensure:
1. `.env` file is in the project root (same directory as `main.py`)
2. No spaces around the `=` sign in `.env` file
3. No quotes around values (unless they contain spaces)

---

## Next Steps

- **Windows**: Your scheduled tasks are now set up and will run automatically
- **Linux**: Configure cron or systemd (see `LINUX_SCHEDULER.md`)

## Additional Resources

- See `SETUP_DOCKER.md` for Docker-based setup
- See `LINUX_SCHEDULER.md` for Linux scheduling options
- Check `IMPLEMENTATION_STATUS.md` for project details


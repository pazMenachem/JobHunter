# Docker Setup Guide

This guide explains how to run JobHunter using Docker containers. Docker provides a consistent environment across different operating systems.

## Prerequisites

- **Docker Desktop** (Windows/macOS) or **Docker Engine** (Linux) installed and running
- **Git** (to clone the repository, if needed)
- **Internet connection** (for downloading Docker images and dependencies)

**Note:** Docker must be running before building or running containers. On Windows, ensure Docker Desktop is started.

---

## Windows Setup

### 1. Install Docker Desktop

1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Run the installer and follow the setup wizard
3. Restart your computer if prompted
4. Launch Docker Desktop and wait for it to start (you'll see a Docker icon in the system tray)
5. Verify installation:
   ```powershell
   docker --version
   docker ps
   ```

**Note:** Docker Desktop requires WSL 2 on Windows. The installer will guide you through this if needed.

### 2. Clone/Download the Repository

If you haven't already, get the JobHunter project:
```powershell
cd C:\Users\YourName\source\repos\JobSeekPlayGround
git clone <repository-url> JobHunter
cd JobHunter
```

### 3. Setup Environment Variables

Create a `.env` file in the project root directory. You can use `.env.example` as a template:

```powershell
copy .env.example .env
```

**📖 For detailed instructions on setting up all environment variables, see:**

👉 **[Environment Setup Guide](ENVIRONMENT_SETUP.md)**

This guide covers:
- ✅ **LLM API Key** (Google Gemini) - Required
- ✅ **Telegram Notifications** - How to create a bot and get chat ID
- ✅ **Email Notifications** - Gmail, Outlook, Yahoo, and custom SMTP servers
- ✅ **Troubleshooting** - Common issues and solutions

**Quick reference for minimum required variables:**

```env
# Required
LLM_API_KEY=your_gemini_api_key_here

# At least one notification provider required:
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_API_CHAT_ID=your_telegram_chat_id

# OR use email notifications:
MAIL_SENDER_EMAIL=your-email@gmail.com
MAIL_APP_PASSWORD=your-app-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587
```

### 4. Build Docker Image

Build the JobHunter Docker image:

```powershell
docker build -t jobhunter .
```

This will:
- Download the Python 3.13 base image
- Install system dependencies for Playwright
- Install Python packages from `requirements.txt`
- Install Playwright browsers (Chromium and Firefox)
- Copy your application code

**Note:** The first build may take 5-10 minutes. Subsequent builds will be faster due to Docker's layer caching.

### 5. Test the Container

Run the container manually to verify everything works:

```powershell
docker-compose up
```

**What this does:**
- Reads configuration from `docker-compose.yml`
- Loads environment variables from your `.env` file
- Mounts the `data/` directory (persists job storage)
- Mounts the `logs/` directory (persists logs)
- Runs the `jobhunter` container

**Alternative:** Run in detached mode (background):
```powershell
docker-compose up -d
```

**Stop the container:**
```powershell
docker-compose down
```

### 6. Configure Application Settings

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

**Important for Docker:** After modifying `src/config.py`, you'll need to rebuild the Docker image for changes to take effect:
```powershell
docker build -t jobhunter .
```

### 7. Configure Scheduler

Edit `scheduler/scheduler_config.json` to set your preferred run times:

```json
{
  "times": ["09:00", "18:00"],
  "mode": "docker"
}
```

- **times**: Array of times in 24-hour format (HH:MM)
- **mode**: Must be `"docker"` for this setup

### 8. Setup Scheduled Tasks

Create Windows Task Scheduler tasks:

```powershell
python scheduler\scheduler.py create
```

This will create scheduled tasks based on the times in `scheduler_config.json`. The tasks will run Docker containers automatically.

**Other scheduler commands:**
- `python scheduler\scheduler.py delete` - Remove all scheduled tasks
- `python scheduler\scheduler.py list` - List all scheduled tasks
- `python scheduler\scheduler.py help` - Show help menu

---

## Linux Setup

**Note:** The Linux setup instructions have not been tested by the project creator. These are provided as a guide based on standard Linux practices.

### 1. Install Docker Engine

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
```

**Fedora/RHEL:**
```bash
# Install Docker
sudo dnf install -y docker docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group
sudo usermod -aG docker $USER
```

**Verify installation:**
```bash
docker --version
docker ps
```

**Note:** After adding yourself to the docker group, you may need to log out and back in for changes to take effect.

### 2. Clone/Download the Repository

```bash
cd ~/projects
git clone <repository-url> JobHunter
cd JobHunter
```

### 3. Setup Environment Variables

Create a `.env` file in the project root directory:

```bash
touch .env
```

**📖 For detailed instructions on setting up all environment variables, see:**

👉 **[Environment Setup Guide](ENVIRONMENT_SETUP.md)**

This guide covers:
- ✅ **LLM API Key** (Google Gemini) - Required
- ✅ **Telegram Notifications** - How to create a bot and get chat ID
- ✅ **Email Notifications** - Gmail, Outlook, Yahoo, and custom SMTP servers
- ✅ **Troubleshooting** - Common issues and solutions

**Quick reference for minimum required variables:**

```env
# Required
LLM_API_KEY=your_gemini_api_key_here

# At least one notification provider required:
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_API_CHAT_ID=your_telegram_chat_id

# OR use email notifications:
MAIL_SENDER_EMAIL=your-email@gmail.com
MAIL_APP_PASSWORD=your-app-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587
```

### 4. Build Docker Image

Build the JobHunter Docker image:

```bash
docker build -t jobhunter .
```

This will:
- Download the Python 3.13 base image
- Install system dependencies for Playwright
- Install Python packages from `requirements.txt`
- Install Playwright browsers (Chromium and Firefox)
- Copy your application code

**Note:** The first build may take 5-10 minutes. Subsequent builds will be faster due to Docker's layer caching.

### 5. Configure Application Settings

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

**Important for Docker:** After modifying `src/config.py`, you'll need to rebuild the Docker image for changes to take effect:
```bash
docker build -t jobhunter .
```

### 6. Test the Container

Run the container manually to verify everything works:

```bash
docker-compose up
```

**What this does:**
- Reads configuration from `docker-compose.yml`
- Loads environment variables from your `.env` file
- Mounts the `data/` directory (persists job storage)
- Mounts the `logs/` directory (persists logs)
- Runs the `jobhunter` container

**Alternative:** Run in detached mode (background):
```bash
docker-compose up -d
```

**Stop the container:**
```bash
docker-compose down
```

### 7. Setup Native Scheduler

**Note:** Linux requires a native scheduler (cron or systemd). See `LINUX_SCHEDULER.md` for detailed instructions.

**Quick cron example:**
```bash
# Edit crontab
crontab -e

# Add this line (runs at 9:00 AM and 6:00 PM daily)
0 9,18 * * * cd /path/to/JobHunter && docker-compose up --abort-on-container-exit
```

---

## Troubleshooting

### Docker Not Running

**Windows:**
- Ensure Docker Desktop is running (check system tray icon)
- Restart Docker Desktop if needed

**Linux:**
```bash
# Check Docker service status
sudo systemctl status docker

# Start Docker if not running
sudo systemctl start docker
```

### Permission Denied (Linux)

If you get permission errors, ensure your user is in the docker group:
```bash
# Check if you're in docker group
groups

# Add yourself to docker group (if not already)
sudo usermod -aG docker $USER

# Log out and back in for changes to take effect
```

### Build Fails

If the Docker build fails:
1. Check your internet connection
2. Ensure Docker is running
3. Try building again (network issues can cause temporary failures)
4. Check Docker logs: `docker logs <container_id>`

### Container Exits Immediately

If the container starts and exits right away:
1. Check logs: `docker logs <container_id>`
2. Verify your `.env` file exists and has correct values
3. Ensure data and logs directories exist:
   ```bash
   mkdir -p data logs
   ```

### Environment Variables Not Loading

Ensure:
1. `.env` file is in the project root (same directory as `Dockerfile`)
2. You're using `--env-file .env` flag when running the container
3. No spaces around the `=` sign in `.env` file
4. No quotes around values (unless they contain spaces)

### Volume Mount Issues

**Windows:**
- Use `${PWD}` or `%cd%` for current directory
- Ensure paths use forward slashes or escaped backslashes

**Linux:**
- Use `$(pwd)` for current directory
- Ensure directories exist before mounting: `mkdir -p data logs`

### Rebuilding the Image

If you make code changes, rebuild the image:
```bash
docker build -t jobhunter .
```

**Note:** Docker caches layers, so only changed layers will be rebuilt.

---

## Next Steps

- **Windows**: Your scheduled tasks are now set up and will run Docker containers automatically
- **Linux**: Configure cron or systemd (see `LINUX_SCHEDULER.md`)

## Additional Resources

- See `SETUP_NATIVE.md` for Python venv-based setup
- See `LINUX_SCHEDULER.md` for Linux scheduling options
- Check `IMPLEMENTATION_STATUS.md` for project details
- Docker documentation: [docs.docker.com](https://docs.docker.com/)


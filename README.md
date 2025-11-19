# JobHunter

Automated job search and filtering application that crawls job listings, analyzes them using AI, and sends relevant opportunities directly to you.

## Features

- 🔍 **Automated Job Crawling** - Scrapes job listings from company career pages
- 🤖 **AI-Powered Filtering** - Uses LLM (Gemini) to analyze job relevance based on your criteria
- 📱 **Smart Notifications** - Sends filtered job opportunities via Telegram or Email
- 💾 **Job Storage** - Tracks sent jobs to avoid duplicates
- ⏰ **Scheduled Runs** - Automatically runs at specified times
- 🐳 **Docker Support** - Run in containers for consistent environments
- 🔧 **Highly Configurable** - Customize keywords, job sites, and AI analysis prompts

## Quick Start

Choose your preferred setup method:

### Option 1: Native Python (Recommended for Beginners)

Run JobHunter directly with Python and a virtual environment.

👉 **[See Native Python Setup Guide](docs/SETUP_NATIVE.md)**

**Quick steps:**
1. Install Python 3.13 or higher
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install JobHunter: `pip install -e .`
5. Setup `.env` file with API keys
6. Configure `src/config.py` with your job search criteria
7. Run: `jh run` (or `python main.py run`)

👉 **[See Installation Guide](INSTALL.md)** for detailed instructions

### Option 2: Docker

Run JobHunter in a Docker container for consistent, isolated execution.

👉 **[See Docker Setup Guide](docs/SETUP_DOCKER.md)**

**Quick steps:**
1. Install Docker Desktop (Windows/macOS) or Docker Engine (Linux)
2. Build image: `docker build -t jobhunter .`
3. Setup `.env` file with API keys
4. Configure `src/config.py` with your job search criteria
5. Run: `docker-compose up`

## Scheduling

### Windows

Use the built-in scheduler commands:

```powershell
jh create
jh list
jh delete
```

Or use the full command:
```powershell
python main.py create
python main.py list
python main.py delete
```

👉 See [Native Python Setup](docs/SETUP_NATIVE.md#9-setup-scheduled-tasks) or [Docker Setup](docs/SETUP_DOCKER.md#8-setup-scheduled-tasks) for details.

### Linux

Use native schedulers (cron or systemd):

👉 **[See Linux Scheduler Guide](docs/LINUX_SCHEDULER.md)**

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
LLM_API_KEY=your_gemini_api_key_here

# Choose at least one notification provider:
# Telegram:
TELEGRAM_API_TOKEN=your_telegram_bot_token
TELEGRAM_API_CHAT_ID=your_telegram_chat_id

# Email (Gmail, Outlook, Yahoo, or any SMTP):
MAIL_SENDER_EMAIL=your-email@gmail.com
MAIL_APP_PASSWORD=your-app-password
MAIL_RECIPIENT_EMAIL=recipient@example.com
MAIL_SMTP_SERVER=smtp.gmail.com
MAIL_SMTP_PORT=587
```

👉 See [Environment Setup Guide](docs/ENVIRONMENT_SETUP.md) for detailed instructions on obtaining these values.

### Application Settings

Edit `src/config.py` to customize:

- **Keywords to search for** (lines 14-19)
- **Keywords to exclude** (lines 21-28)
- **Target job sites** (lines 30-34)
- **LLM analysis prompt** (lines 38-80)
- **Job filter level** (line 82)

👉 See setup guides for detailed configuration instructions.

## Project Structure

```
JobHunter/
├── src/                    # Application source code
│   ├── app_manager.py      # Main orchestrator
│   ├── config.py           # Configuration settings
│   ├── job_crawler_service/ # Web scraping
│   ├── llm_service/        # AI analysis
│   ├── notification_service/ # Notifications
│   └── ...
├── docs/                   # Documentation files
│   ├── SETUP_NATIVE.md     # Native Python setup
│   ├── SETUP_DOCKER.md     # Docker setup
│   └── LINUX_SCHEDULER.md  # Linux scheduling
├── scheduler/              # Windows scheduler script
│   ├── scheduler.py        # Main scheduler entry point
│   └── scheduler_config.json
├── data/                   # Job storage (generated)
├── logs/                   # Application logs (generated)
├── main.py                 # Unified entry point (run app + scheduler)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
└── README.md               # This file
```

## Requirements

- **Python**: 3.13 or higher
- **Docker** (optional): For containerized execution
- **API Keys**:
  - Google Gemini API key (for LLM analysis)
  - Telegram Bot Token and Chat ID (for Telegram notifications) OR
  - Email credentials for SMTP (for email notifications)

## Documentation

📚 **[View All Documentation](docs/)** - Complete documentation index

- **[Environment Setup Guide](docs/ENVIRONMENT_SETUP.md)** - How to configure API keys and notifications
- **[Native Python Setup Guide](docs/SETUP_NATIVE.md)** - Complete setup instructions for Python venv
- **[Docker Setup Guide](docs/SETUP_DOCKER.md)** - Complete setup instructions for Docker
- **[Linux Scheduler Guide](docs/LINUX_SCHEDULER.md)** - Cron and systemd scheduling examples

## How It Works

1. **Crawl Jobs** - Scrapes job listings from configured company career pages
2. **Filter Duplicates** - Removes jobs that have already been sent
3. **AI Analysis** - Uses LLM to analyze each job's relevance based on your criteria
4. **Filter by Relevance** - Keeps only jobs matching your filter level (YES/MAYBE)
5. **Send Notifications** - Sends relevant jobs to your Telegram
6. **Mark as Sent** - Stores sent jobs to prevent duplicates

## Extending JobHunter

### Adding Notification Providers

Implement the provider abstract class. See existing implementations in `src/notification_service/` for reference.

### Adding LLM Providers

Implement the LLM provider abstract class. See existing implementations in `src/llm_service/` for reference.

## Troubleshooting

### Common Issues

- **Environment variables not loading**: Ensure `.env` file is in project root
- **Docker build fails**: Check Docker is running and you have internet connection
- **Scheduled tasks not running**: Verify scheduler configuration and check logs
- **No jobs found**: Check your target URLs and keywords in `src/config.py`

👉 See setup guides for detailed troubleshooting sections.

## License

**MIT License** - Open source and free to use, modify, and distribute.

## Contributing

Contributions are welcome! Here are some guidelines:

### How to Contribute

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the existing code style
3. **Test your changes** to ensure they work correctly
4. **Update documentation** if you've changed functionality
5. **Submit a pull request** with a clear description of your changes

### Contribution Guidelines

- **Code Style**: Follow existing code patterns and use type hints for function parameters
- **Documentation**: Update relevant documentation files when adding features
- **Testing**: Test your changes before submitting
- **Commit Messages**: Write clear, descriptive commit messages
- **Pull Requests**: Provide a clear description of what was changed and why

### Getting Help

If you have questions or need help, feel free to open an issue for discussion.

---

**Need help?** Check the detailed setup guides or open an issue.


# JobHunter Documentation

Welcome to the JobHunter documentation! This folder contains all setup guides and technical documentation.

## 📚 Documentation Index

### Setup Guides

- **[SETUP_NATIVE.md](SETUP_NATIVE.md)** - Native Python setup guide
  - Prerequisites and installation
  - Environment configuration
  - Running the application locally
  - Windows Task Scheduler setup

- **[SETUP_DOCKER.md](SETUP_DOCKER.md)** - Docker setup guide
  - Docker installation and configuration
  - Container setup and management
  - Scheduled execution with Docker
  - Troubleshooting Docker issues

- **[LINUX_SCHEDULER.md](LINUX_SCHEDULER.md)** - Linux scheduling guide
  - Setting up cron jobs
  - Systemd service configuration
  - Linux-specific automation

## 🚀 Quick Start

1. **First time users**: Start with [SETUP_NATIVE.md](SETUP_NATIVE.md) or [SETUP_DOCKER.md](SETUP_DOCKER.md)
2. **Run the app**: `python main.py` or `python main.py run`
3. **Scheduling automation**: Use `python main.py create` (see your setup guide for details)
4. **Linux users**: Check [LINUX_SCHEDULER.md](LINUX_SCHEDULER.md) for native scheduling

## 📂 Project Structure

```
JobHunter/
├── docs/              # Documentation (you are here)
├── src/               # Source code
├── scheduler/         # Windows Task Scheduler integration
├── data/              # Storage files (sent_jobs.json)
├── logs/              # Application logs
└── main.py            # Unified entry point (run app + scheduler)
```

## 🔗 Related Files

- **Main README**: See `../README.md` for project overview
- **Requirements**: See `../requirements.txt` for dependencies
- **Configuration**: See `src/config.py` for settings

## 💡 Need Help?

- Check the appropriate setup guide for your platform
- Review logs in the `logs/` directory
- Ensure `.env` file is properly configured with API keys


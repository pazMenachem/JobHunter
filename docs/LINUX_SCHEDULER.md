# Linux Scheduler Setup Guide

**Note:** Linux requires a native scheduler (cron or systemd). The Windows scheduler script is not available on Linux.

This guide provides examples for scheduling JobHunter on Linux using cron or systemd timers.

---

## Prerequisites

- JobHunter application set up (either native Python or Docker)
- Basic familiarity with Linux command line
- Root/sudo access (for systemd, optional for cron)

---

## Option 1: Cron (Recommended for Beginners)

Cron is the most common task scheduler on Linux. It's simple and works well for most use cases.

### Setup Instructions

1. **Open your crontab:**
   ```bash
   crontab -e
   ```

2. **Add one of the following lines** (choose based on your setup):

#### For Native Python Setup

```bash
# Run JobHunter at 9:00 AM and 6:00 PM daily
0 9,18 * * * cd /path/to/JobHunter && source venv/bin/activate && python main.py >> /path/to/JobHunter/logs/cron.log 2>&1
```

**Breakdown:**
- `0 9,18 * * *` - Runs at 9:00 AM and 6:00 PM every day
- `cd /path/to/JobHunter` - Navigate to project directory
- `source venv/bin/activate` - Activate virtual environment
- `python main.py` - Run the application
- `>> /path/to/JobHunter/logs/cron.log 2>&1` - Append output to log file

#### For Docker Setup

```bash
# Run JobHunter at 9:00 AM and 6:00 PM daily
0 9,18 * * * cd /path/to/JobHunter && docker-compose up --abort-on-container-exit >> /path/to/JobHunter/logs/cron.log 2>&1
```

**Breakdown:**
- `0 9,18 * * *` - Runs at 9:00 AM and 6:00 PM every day
- `cd /path/to/JobHunter` - Navigate to project directory
- `docker-compose up --abort-on-container-exit` - Run Docker container using docker-compose
- `>> /path/to/JobHunter/logs/cron.log 2>&1` - Append output to log file

### Cron Schedule Format

The cron schedule format is: `minute hour day month weekday`

**Examples:**
```bash
# Every day at 9:00 AM
0 9 * * *

# Every day at 9:00 AM and 6:00 PM
0 9,18 * * *

# Every weekday (Monday-Friday) at 9:00 AM
0 9 * * 1-5

# Every hour
0 * * * *

# Every 30 minutes
*/30 * * * *

# Every Monday at 9:00 AM
0 9 * * 1
```

### Multiple Times

To run at multiple times, separate them with commas:

```bash
# Run at 8:00 AM, 12:00 PM, and 6:00 PM
0 8,12,18 * * * cd /path/to/JobHunter && source venv/bin/activate && python main.py >> /path/to/JobHunter/logs/cron.log 2>&1
```

### Verify Cron Jobs

**List your cron jobs:**
```bash
crontab -l
```

**Check cron logs:**
```bash
# On most systems
grep CRON /var/log/syslog

# Or check your application log
tail -f /path/to/JobHunter/logs/cron.log
```

### Troubleshooting Cron

**Issue: Cron job not running**
- Check if cron service is running: `sudo systemctl status cron` (or `crond` on some systems)
- Verify the path in your cron job is absolute (use full paths)
- Check cron logs: `grep CRON /var/log/syslog`
- Ensure the script has execute permissions if using a script file

**Issue: Environment variables not available**
- Cron runs with minimal environment. Use absolute paths and full commands
- For Docker, ensure Docker daemon is accessible (may need to use full path to `docker`)

**Issue: Virtual environment not activating**
- Use full path to Python: `/path/to/JobHunter/venv/bin/python main.py`
- Or use full path to activate script: `source /path/to/JobHunter/venv/bin/activate`

---

## Option 2: Systemd Timers (Advanced)

Systemd timers provide more features than cron, including better logging, dependency management, and more precise scheduling.

### Setup Instructions

1. **Create a systemd service file:**

Create `/etc/systemd/system/jobhunter.service` (or `~/.config/systemd/user/jobhunter.service` for user service):

```ini
[Unit]
Description=JobHunter Job Scraper
After=network.target

[Service]
Type=oneshot
WorkingDirectory=/path/to/JobHunter
User=your-username
Environment="PATH=/usr/local/bin:/usr/bin:/bin"

# For Native Python
ExecStart=/path/to/JobHunter/venv/bin/python /path/to/JobHunter/main.py

# OR for Docker
# ExecStart=/usr/bin/docker-compose -f /path/to/JobHunter/docker-compose.yml up --abort-on-container-exit

StandardOutput=append:/path/to/JobHunter/logs/systemd.log
StandardError=append:/path/to/JobHunter/logs/systemd.log
```

2. **Create a systemd timer file:**

Create `/etc/systemd/system/jobhunter.timer` (or `~/.config/systemd/user/jobhunter.timer` for user timer):

```ini
[Unit]
Description=Run JobHunter at scheduled times
Requires=jobhunter.service

[Timer]
# Run at 9:00 AM and 6:00 PM daily
OnCalendar=*-*-* 09:00,18:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

3. **Enable and start the timer:**

**For system service (requires sudo):**
```bash
sudo systemctl daemon-reload
sudo systemctl enable jobhunter.timer
sudo systemctl start jobhunter.timer
```

**For user service (no sudo needed):**
```bash
systemctl --user daemon-reload
systemctl --user enable jobhunter.timer
systemctl --user start jobhunter.timer
```

### Systemd Timer Schedule Format

Systemd uses a different schedule format. Examples:

```ini
# Every day at 9:00 AM and 6:00 PM
OnCalendar=*-*-* 09:00,18:00:00

# Every weekday at 9:00 AM
OnCalendar=Mon..Fri 09:00:00

# Every hour
OnCalendar=*-*-* *:00:00

# Every 30 minutes
OnCalendar=*-*-* *:00,30:00

# Every Monday at 9:00 AM
OnCalendar=Mon 09:00:00
```

### Manage Systemd Timer

**Check timer status:**
```bash
# System service
sudo systemctl status jobhunter.timer

# User service
systemctl --user status jobhunter.timer
```

**List all timers:**
```bash
# System timers
sudo systemctl list-timers

# User timers
systemctl --user list-timers
```

**View logs:**
```bash
# System service
sudo journalctl -u jobhunter.service

# User service
journalctl --user -u jobhunter.service
```

**Stop/Start timer:**
```bash
# System service
sudo systemctl stop jobhunter.timer
sudo systemctl start jobhunter.timer

# User service
systemctl --user stop jobhunter.timer
systemctl --user start jobhunter.timer
```

---

## Comparison: Cron vs Systemd

| Feature | Cron | Systemd Timer |
|---------|------|---------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Very simple | ⭐⭐⭐ More complex |
| **Logging** | Basic (manual setup) | ⭐⭐⭐⭐⭐ Excellent (journalctl) |
| **Dependencies** | No | ⭐⭐⭐⭐⭐ Yes (network, services) |
| **Precise Timing** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **User vs System** | Both | Both |
| **Best For** | Simple schedules | Complex requirements, better logging |

**Recommendation:** Start with cron if you're new to Linux scheduling. Use systemd if you need better logging, dependencies, or more complex scheduling.

---

## Additional Tips

### Using a Shell Script

For cleaner cron/systemd entries, you can create a shell script:

**Create `run_jobhunter.sh`:**
```bash
#!/bin/bash
cd /path/to/JobHunter

# For Native Python
source venv/bin/activate
python main.py run

# OR for Docker
# docker-compose up --abort-on-container-exit
```

**Make it executable:**
```bash
chmod +x /path/to/JobHunter/run_jobhunter.sh
```

**Then use in cron:**
```bash
0 9,18 * * * /path/to/JobHunter/run_jobhunter.sh >> /path/to/JobHunter/logs/cron.log 2>&1
```

### Environment Variables

If you need additional environment variables:

**For Cron:**
```bash
0 9,18 * * * cd /path/to/JobHunter && export CUSTOM_VAR=value && source venv/bin/activate && python main.py
```

**For Systemd:**
Add to the `[Service]` section:
```ini
Environment="CUSTOM_VAR=value"
```

### Log Rotation

To prevent log files from growing too large, set up log rotation:

**Create `/etc/logrotate.d/jobhunter`:**
```
/path/to/JobHunter/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## Troubleshooting

### General Issues

**Check if scheduler is running:**
- Cron: `sudo systemctl status cron` (or `crond`)
- Systemd: `sudo systemctl status jobhunter.timer`

**Verify paths:**
- Always use absolute paths in cron/systemd
- Test commands manually before adding to scheduler

**Check permissions:**
- Ensure user has read/write access to project directory
- For Docker, ensure user is in `docker` group

**View recent runs:**
- Cron: Check application logs in `logs/` directory
- Systemd: `journalctl -u jobhunter.service` (or `--user` for user service)

---

## Next Steps

- Test your scheduled job manually first
- Monitor logs for the first few runs
- Adjust schedule times as needed
- See `SETUP_NATIVE.md` or `SETUP_DOCKER.md` for application setup


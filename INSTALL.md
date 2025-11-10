# JobHunter Installation Guide

## Quick Installation

### For Development (Editable Install)

This allows you to make changes and have them immediately reflected:

```bash
# From the JobHunter directory
pip install -e .
```

### For Production Use

```bash
pip install .
```

## After Installation

Once installed, you can use the `jh` command from anywhere:

```bash
# Show help
jh

# Run the application
jh run

# Create scheduled tasks
jh create

# List scheduled tasks
jh list

# Delete scheduled tasks
jh delete
```

## Verify Installation

```bash
# Check that jh is available
jh help

# Check where jh is installed
where jh      # Windows
which jh      # Linux/Mac
```

## Uninstall

```bash
pip uninstall jobhunter
```

## Virtual Environment (Recommended)

It's recommended to install JobHunter in a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Install JobHunter
pip install -e .

# Now use jh commands
jh run
```

## Troubleshooting

### "jh: command not found"

Make sure pip's scripts directory is in your PATH:

**Windows:**
- Add `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts` to PATH

**Linux/Mac:**
- Add `~/.local/bin` to PATH (usually already done)

### Verify pip installation location

```bash
pip show jobhunter
```

This will show where JobHunter is installed and confirm the installation was successful.


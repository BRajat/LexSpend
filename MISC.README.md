## INSTALL UV

### Step 1: Install uv fresh via PowerShell
Open a standard PowerShell window and run the official installer:

```PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
This script will safely download the latest standalone binary, place it in the correct directory, and automatically configure your system PATH variables so it works everywhere.

### Step 2: Restart your terminal
Close your current Git Bash or terminal window completely and open a new one.

### Step 3: Verify it works
Type:

```Bash
uv --version
```

It will instantly respond with the version number, and you can jump straight into managing your virtual environments.
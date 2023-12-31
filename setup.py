import os
import shutil
import subprocess
import sys

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Get the path to the "prohunt.py" script
script_path = os.path.join(os.getcwd(), "prohunt.py")

# Get the system's PATH environment variable
path_env = os.environ.get("PATH", "")

# Check if the script path is already in the PATH
if script_path not in path_env:
    # Add the script path to the PATH
    new_path = os.pathsep.join([path_env, script_path])

    # Update the PATH environment variable
    os.environ["PATH"] = new_path

    # Move the script file to a directory in the PATH
    shutil.copy(script_path, "/usr/local/bin/prohunt")  # Update the destination directory if needed

    # Give the "prohunt" script executable permissions
    script_executable_path = "/usr/local/bin/prohunt/prohunt.py"  # Update the path if needed
    os.chmod(script_executable_path, 0o755)

# Set permissions for the wordlist file
wordlist_path = os.path.join(os.getcwd(), "default_wordlist.txt")  # Update the path if needed
if os.path.isfile(wordlist_path):
    os.chmod(wordlist_path, 0o644)  # Set read permissions for the wordlist file

# Provide setup completion message
print("Prohunt setup completed successfully.")

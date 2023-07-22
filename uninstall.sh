#!/bin/bash

# Function to uninstall the launch agent
function uninstall_launch_agent() {
    echo "Unloading and removing the launch agent..."
    launchctl unload "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist"
    rm -f "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist"
}

# Function to uninstall Python and Python-related packages
function uninstall_python_and_packages() {
    echo "Uninstalling Python and related packages..."
    # Uninstall Python
    brew uninstall python-tk

    # Uninstall PySimpleGUI
    /usr/local/bin/python3 -m pip uninstall PySimpleGUI
    /usr/local/bin/python3 -m pip uninstall Requests
    /usr/local/bin/python3 -m pip uninstall qrcode

    # Uninstall Homebrew (if needed)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
}

# Function to remove .myscript directory
function remove_myscript_directory() {
    echo "Removing .myscript directory..."
    rm -rf "$HOME/.myscript"
    rm -rf "$HOME/.zprofile"
}

# Function to delete the password from the keychain
function delete_password_from_keychain() {
    echo "Deleting password from keychain..."
    security delete-generic-password -s "com.example.app_password" -a "app_user"
}

# Main execution
uninstall_launch_agent
remove_myscript_directory
delete_password_from_keychain
uninstall_python_and_packages

echo "Uninstall completed successfully!"

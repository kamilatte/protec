function remove_launch_agent() {
    echo "Removing the launch agent..."
    launchctl unload "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist" || display_error "Failed to unload the launch agent"
    rm -f "$HOME/Library/LaunchAgents/com.$USER.run_new_script.plist"
}

function remove_shell_script() {
    echo "Removing the shell script..."
    rm -f "$HOME/.myscript/run_new_script.sh"
}

function remove_script() {
    echo "Removing the Python script..."
    rm -f "$HOME/.myscript/new.py"
}

function remove_myscript_directory() {
    echo "Removing .myscript directory..."
    rm -rf "$HOME/.myscript"
}

function uninstall_python_tkinter() {
    echo "Uninstalling Python with Tkinter support..."
    brew uninstall python-tk
}

function uninstall_get_pip() {
    echo "Uninstalling pip..."
    /usr/local/bin/python3 -m pip uninstall pip -y
}

function uninstall_python_packages() {
    echo "Uninstalling PySimpleGUI and required packages..."
    /usr/local/bin/python3 -m pip uninstall PySimpleGUI qrcode requests pyotp -y
}

function uninstall_homebrew() {
    echo "Do you want to uninstall Homebrew? (Y/N)"
    read -r uninstall_brew
    if [ "$uninstall_brew" = "Y" ] || [ "$uninstall_brew" = "y" ]; then
        echo "Uninstalling Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall.sh)"
    else
        echo "Skipping Homebrew uninstallation."
    fi
}

function display_error() {
    echo "Error: $1"
    exit 1
}

function main() {
    remove_launch_agent
    remove_shell_script
    remove_script
    uninstall_python_packages
    uninstall_python_tkinter
    remove_myscript_directory
    uninstall_get_pip
    uninstall_homebrew

    echo "Uninstallation completed successfully!"
}

main

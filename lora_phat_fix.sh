#!/bin/bash

# Comprehensive LoRa pHAT Fix Script
# This script performs checks and fixes for common LoRa pHAT issues

# Function to log messages
log_message() {
    echo "$1"
}

# Check and fix UART configuration
fix_uart_config() {
    if ! grep -q "enable_uart=1" /boot/config.txt; then
        log_message "Adding enable_uart=1 to /boot/config.txt"
        echo "enable_uart=1" | sudo tee -a /boot/config.txt
    fi

    if ! grep -q "dtoverlay=disable-bt" /boot/config.txt; then
        log_message "Adding dtoverlay=disable-bt to /boot/config.txt"
        echo "dtoverlay=disable-bt" | sudo tee -a /boot/config.txt
    fi
}

# Stop and disable serial-getty service
fix_serial_getty() {
    log_message "Stopping and disabling serial-getty@ttyAMA0.service"
    sudo systemctl stop serial-getty@ttyAMA0.service
    sudo systemctl disable serial-getty@ttyAMA0.service
    sudo systemctl mask serial-getty@ttyAMA0.service
}

# Check RAK811 version
check_rak_version() {
    log_message "Checking RAK811 version:"
    rak811 -v -d version || log_message "Failed to get RAK811 version"
    rak811v3 -v -d version || log_message "Failed to get RAK811v3 version"
}

# Perform hard reset
perform_hard_reset() {
    log_message "Performing hard reset:"
    rak811 -v -d hard-reset || log_message "Failed to perform hard reset"
}

# Reset LoRa
reset_lora() {
    log_message "Resetting LoRa:"
    rak811 -v -d reset lora || log_message "Failed to reset LoRa"
}

# Check for processes using ttyAMA0
check_ttyAMA0_usage() {
    log_message "Checking for processes using ttyAMA0:"
    sudo fuser -v /dev/ttyAMA0 || log_message "No processes found using ttyAMA0"
}

# Main execution
log_message "Starting Comprehensive LoRa pHAT Fix Script"

fix_uart_config
fix_serial_getty
check_rak_version
perform_hard_reset
reset_lora
check_ttyAMA0_usage

log_message "Checks and fixes applied. Please reboot your Raspberry Pi."
log_message "After reboot, run this script again to verify all issues are resolved."
log_message "If problems persist, please check physical connections and antenna configuration."
log_message "Remember: If using an external antenna, ensure the INT inductor is desoldered for best range."

# Prompt for reboot
read -p "Would you like to reboot now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo reboot
fi
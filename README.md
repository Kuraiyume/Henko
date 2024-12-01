# Henko
Henko is a Python script designed to change the MAC address of network interfaces on Linux systems. It supports generating random MAC addresses, specifying a custom MAC address, and reverting to the original MAC address. 

## Features

- Change the MAC address of a network interface.
- Generate random MAC addresses.
- Specify a custom MAC address.
- Backup and revert to the original MAC address.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kUrOSH1R0oo/Henko
   ```

2. Navigate to the directory and make the script executable:
   ```bash
   chmod +x henko.py
   ```

## Usage

   *Note: Henko needs root privileges to run.*

1. Changing MAC Address (Custom)
   ```bash
   sudo ./henko.py <interface> -m <new_mac>
   ```

2. Generate Random MAC Address
   ```bash
   sudo ./henko.py <interface> -r
   ```

3. Revert to Original MAC Address
   ```bash
   sudo ./henko.py <interface> -R
   ```

4. Backup Current MAC Address
   ```bash
   sudo ./henko.py <interface> -r -b
   ```

## License

- This project is licensed under the MIT License

## Author

- Kuroshiro


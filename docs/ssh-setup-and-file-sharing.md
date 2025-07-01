# SSH Setup and File Sharing Guide

This document provides step-by-step instructions for setting up SSH access to your Vision Trax server using a private PEM key, and configuring folder sharing for seamless file transfer from Windows and macOS machines.

## SSH Setup with Private PEM Key

### Prerequisites
- Vision Trax server with Ubuntu 20.04/22.04 LTS installed
- Private PEM key file for authentication
- SSH client installed on your local machine

### 1. Server-Side SSH Configuration

#### Install and Configure SSH Server
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install OpenSSH server
sudo apt install -y openssh-server

# Start and enable SSH service
sudo systemctl start ssh
sudo systemctl enable ssh

# Check SSH service status
sudo systemctl status ssh
```

#### Configure SSH for Key-Based Authentication
```bash
# Create SSH directory for root user (if needed)
sudo mkdir -p /root/.ssh
sudo chmod 700 /root/.ssh

# Create SSH directory for regular user
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Create authorized_keys file
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### Configure SSH Server Settings
```bash
# Backup original SSH config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Edit SSH configuration
sudo nano /etc/ssh/sshd_config
```

Add or modify these settings in `/etc/ssh/sshd_config`:
```bash
# Security settings
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys

# Connection settings
Port 22
Protocol 2
ClientAliveInterval 300
ClientAliveCountMax 2

# Logging
LogLevel INFO
SyslogFacility AUTH
```

#### Restart SSH Service
```bash
# Test SSH configuration
sudo sshd -t

# Restart SSH service
sudo systemctl restart ssh

# Verify SSH is running
sudo systemctl status ssh
```

### 2. Client-Side SSH Configuration

#### Windows Setup

**Using PuTTY:**
1. Download and install PuTTY from https://www.putty.org/
2. Convert PEM key to PPK format:
   ```bash
   # Using PuTTYgen (included with PuTTY)
   # Load your .pem file and save as .ppk
   ```
3. Configure PuTTY:
   - Host Name: `your-server-ip`
   - Port: `22`
   - Connection type: `SSH`
   - In Connection > SSH > Auth > Credentials, browse to your .ppk file

**Using Windows Subsystem for Linux (WSL):**
```bash
# Copy PEM key to WSL
cp /mnt/c/path/to/your/key.pem ~/.ssh/

# Set correct permissions
chmod 600 ~/.ssh/key.pem

# Connect to server
ssh -i ~/.ssh/key.pem username@your-server-ip
```

**Using PowerShell/Command Prompt:**
```powershell
# If using OpenSSH client (Windows 10 1803+)
ssh -i "C:\path\to\your\key.pem" username@your-server-ip
```

#### macOS Setup
```bash
# Copy PEM key to SSH directory
cp /path/to/your/key.pem ~/.ssh/

# Set correct permissions
chmod 600 ~/.ssh/key.pem

# Connect to server
ssh -i ~/.ssh/key.pem username@your-server-ip
```

#### Linux Setup
```bash
# Copy PEM key to SSH directory
cp /path/to/your/key.pem ~/.ssh/

# Set correct permissions
chmod 600 ~/.ssh/key.pem

# Connect to server
ssh -i ~/.ssh/key.pem username@your-server-ip
```

### 3. SSH Configuration File (Optional)

Create `~/.ssh/config` on your client machine for easier connections:
```bash
# Create SSH config file
nano ~/.ssh/config
```

Add the following configuration:
```bash
Host vision-trax-server
    HostName your-server-ip
    User your-username
    Port 22
    IdentityFile ~/.ssh/your-key.pem
    ServerAliveInterval 300
    ServerAliveCountMax 2
```

Now you can connect simply with:
```bash
ssh vision-trax-server
```

### 4. Testing SSH Connection
```bash
# Test connection
ssh -i ~/.ssh/your-key.pem username@your-server-ip

# Test with verbose output for troubleshooting
ssh -v -i ~/.ssh/your-key.pem username@your-server-ip
```

## File Sharing Setup

### 1. Samba Server Configuration

#### Install Samba
```bash
# Install Samba server
sudo apt update
sudo apt install -y samba samba-common

# Check Samba version
samba --version
```

#### Configure Samba
```bash
# Backup original Samba config
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.backup

# Edit Samba configuration
sudo nano /etc/samba/smb.conf
```

Replace the content with this configuration:
```ini
[global]
   workgroup = WORKGROUP
   server string = Vision Trax Server
   server role = standalone server
   server signing = auto
   smb encrypt = desired
   log level = 1
   log file = /var/log/samba/%m.log
   max log size = 50
   dns proxy = no
   unix charset = UTF-8
   dos charset = CP850
   passdb backend = tdbsam
   security = user
   map to guest = bad user
   usershare allow guests = yes
   create mask = 0644
   directory mask = 0755
   force user = vision-trax
   force group = vision-trax

[Videos]
   comment = Video Processing Directory
   path = /home/vision-trax/videos
   browseable = yes
   writable = yes
   guest ok = yes
   create mask = 0644
   directory mask = 0755
   force user = vision-trax
   force group = vision-trax

[Results]
   comment = Processing Results Directory
   path = /home/vision-trax/results
   browseable = yes
   writable = yes
   guest ok = yes
   create mask = 0644
   directory mask = 0755
   force user = vision-trax
   force group = vision-trax

[Uploads]
   comment = File Upload Directory
   path = /home/vision-trax/uploads
   browseable = yes
   writable = yes
   guest ok = yes
   create mask = 0644
   directory mask = 0755
   force user = vision-trax
   force group = vision-trax
```

#### Create Required Directories
```bash
# Create vision-trax user and group
sudo useradd -m -s /bin/bash vision-trax
sudo usermod -aG sudo vision-trax

# Create shared directories
sudo mkdir -p /home/vision-trax/videos
sudo mkdir -p /home/vision-trax/results
sudo mkdir -p /home/vision-trax/uploads

# Set ownership and permissions
sudo chown -R vision-trax:vision-trax /home/vision-trax/
sudo chmod -R 755 /home/vision-trax/
```

#### Configure Samba User
```bash
# Add Samba user (you'll be prompted for password)
sudo smbpasswd -a vision-trax

# Enable Samba user
sudo smbpasswd -e vision-trax
```

#### Start and Enable Samba Services
```bash
# Start Samba services
sudo systemctl start smbd
sudo systemctl start nmbd

# Enable Samba services to start on boot
sudo systemctl enable smbd
sudo systemctl enable nmbd

# Check service status
sudo systemctl status smbd
sudo systemctl status nmbd
```

#### Configure Firewall
```bash
# Allow Samba through firewall
sudo ufw allow samba

# Or manually open required ports
sudo ufw allow 139/tcp
sudo ufw allow 445/tcp

# Check firewall status
sudo ufw status
```

### 2. Client-Side Connection

#### Windows Connection

**Using File Explorer:**
1. Open File Explorer
2. In the address bar, type: `\\your-server-ip`
3. Enter credentials when prompted:
   - Username: `vision-trax`
   - Password: (the password you set with smbpasswd)

**Using Command Line:**
```cmd
# Map network drive
net use Z: \\your-server-ip\Videos /user:vision-trax

# Or connect to specific share
net use Z: \\your-server-ip\Uploads /user:vision-trax
```

**Using PowerShell:**
```powershell
# Create new PSDrive
New-PSDrive -Name "VisionTrax" -PSProvider FileSystem -Root "\\your-server-ip\Videos" -Credential (Get-Credential)

# Or map network drive
net use Z: \\your-server-ip\Videos /user:vision-trax /persistent:yes
```

#### macOS Connection

**Using Finder:**
1. Open Finder
2. Press `Cmd + K` or go to Go > Connect to Server
3. Enter: `smb://your-server-ip`
4. Select the share you want to connect to
5. Enter credentials when prompted

**Using Command Line:**
```bash
# Mount Samba share
sudo mkdir -p /Volumes/VisionTrax
sudo mount -t smbfs //vision-trax@your-server-ip/Videos /Volumes/VisionTrax

# Or using mount_smbfs
sudo mount_smbfs //vision-trax@your-server-ip/Videos /Volumes/VisionTrax
```

**Using Automator for Auto-Mount:**
1. Open Automator
2. Create new document > Application
3. Add "Run Shell Script" action
4. Add the mount command
5. Save as application and add to login items

#### Linux Connection

**Using GUI:**
1. Open file manager
2. Press `Ctrl + L`
3. Enter: `smb://your-server-ip`
4. Navigate to desired share

**Using Command Line:**
```bash
# Install Samba client
sudo apt install -y smbclient cifs-utils

# Create mount point
sudo mkdir -p /mnt/vision-trax

# Mount Samba share
sudo mount -t cifs //your-server-ip/Videos /mnt/vision-trax -o username=vision-trax,password=your-password

# Or add to /etc/fstab for permanent mount
echo "//your-server-ip/Videos /mnt/vision-trax cifs username=vision-trax,password=your-password,iocharset=utf8,uid=1000,gid=1000 0 0" | sudo tee -a /etc/fstab
```

### 3. Testing File Transfer

#### Test Upload
```bash
# From Windows (PowerShell)
Copy-Item "C:\path\to\video.mp4" "Z:\"

# From macOS (Terminal)
cp /path/to/video.mp4 /Volumes/VisionTrax/

# From Linux (Terminal)
cp /path/to/video.mp4 /mnt/vision-trax/
```

#### Test Download
```bash
# Download processed results
# Windows
Copy-Item "Z:\results\*" "C:\downloads\"

# macOS
cp /Volumes/VisionTrax/results/* ~/Downloads/

# Linux
cp /mnt/vision-trax/results/* ~/Downloads/
```

### 4. Troubleshooting

#### Common Samba Issues

**Permission Denied:**
```bash
# Check Samba user exists
sudo pdbedit -L

# Reset Samba password
sudo smbpasswd -a vision-trax

# Check file permissions
ls -la /home/vision-trax/
```

**Connection Refused:**
```bash
# Check Samba services
sudo systemctl status smbd nmbd

# Check firewall
sudo ufw status

# Test Samba configuration
testparm
```

**Slow Transfer Speeds:**
```bash
# Optimize Samba settings in smb.conf
socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=65536 SO_SNDBUF=65536
read raw = yes
write raw = yes
max xmit = 65535
dead time = 15
getwd cache = yes
```

#### Network Troubleshooting
```bash
# Test network connectivity
ping your-server-ip

# Test Samba ports
telnet your-server-ip 139
telnet your-server-ip 445

# Check Samba logs
sudo tail -f /var/log/samba/log.smbd
```

## Security Considerations

### 1. SSH Security
- Use strong private keys (2048-bit or higher)
- Regularly rotate SSH keys
- Monitor SSH access logs
- Consider changing default SSH port
- Use fail2ban for brute force protection

### 2. Samba Security
- Use strong passwords for Samba users
- Regularly update Samba software
- Monitor Samba access logs
- Consider encrypting Samba traffic
- Restrict access to specific IP ranges if possible

### 3. Network Security
- Use VPN for remote access when possible
- Implement network segmentation
- Regular security audits
- Keep systems updated

## Automation Scripts

### 1. SSH Connection Script
```bash
#!/bin/bash
# connect.sh - Quick SSH connection script

SERVER_IP="your-server-ip"
USERNAME="your-username"
KEY_PATH="~/.ssh/your-key.pem"

echo "Connecting to Vision Trax server..."
ssh -i $KEY_PATH $USERNAME@$SERVER_IP
```

### 2. Samba Status Check Script
```bash
#!/bin/bash
# samba-status.sh - Check Samba services

echo "Checking Samba services..."
sudo systemctl status smbd nmbd

echo "Checking Samba shares..."
smbclient -L localhost -U%

echo "Checking Samba connections..."
sudo smbstatus
```

### 3. File Transfer Monitor Script
```bash
#!/bin/bash
# monitor-transfers.sh - Monitor file transfers

WATCH_DIR="/home/vision-trax/uploads"

echo "Monitoring file transfers in $WATCH_DIR..."
inotifywait -m -r -e create,modify,delete $WATCH_DIR
```

## Conclusion

This guide provides comprehensive instructions for setting up secure SSH access and file sharing for your Vision Trax server. The combination of SSH for remote administration and Samba for file sharing enables seamless integration with Windows and macOS workstations.

Remember to:
- Regularly update and maintain security configurations
- Monitor access logs for suspicious activity
- Test file transfer speeds and optimize as needed
- Keep backup copies of configuration files
- Document any customizations for your specific environment

For additional support or questions, refer to the main project documentation or contact the development team. 
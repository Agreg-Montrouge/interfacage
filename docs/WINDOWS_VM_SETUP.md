# Windows VM Setup Guide for TPMontrouge

Complete guide for setting up a local Windows VM for building and testing TPMontrouge Windows executables.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [VM Setup](#vm-setup)
4. [Windows Configuration](#windows-configuration)
5. [Development Tools Installation](#development-tools-installation)
6. [Repository Setup](#repository-setup)
7. [Usage](#usage)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance](#maintenance)

---

## Overview

This setup provides a local Windows build environment that complements GitHub Actions:

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│ Linux Host                                                   │
│ /home/pierre/python-projects/montrouge/                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ VirtualBox VM: Windows 10/11                         │  │
│  │                                                       │  │
│  │  • SSH: localhost:2222 → 22 (builds)                │  │
│  │  • RDP: localhost:3389 → 3389 (GUI testing)         │  │
│  │                                                       │  │
│  │  C:\builds\interfacage\tpmontrouge\                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Use Cases:**
- ✅ Test builds locally before pushing to GitHub
- ✅ Debug PyInstaller/Inno Setup issues interactively
- ✅ Quick iteration during development
- ✅ Test GUI applications with full Windows environment

---

## Prerequisites

### Linux Host Requirements
- **VirtualBox** 6.1+ installed
- **SSH client** (openssh-client)
- **rsync** for file synchronization
- At least **20 GB free disk space**
- At least **4 GB RAM** (2-3 GB for VM)

**Install on Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install virtualbox virtualbox-ext-pack openssh-client rsync
```

### Windows ISO
Download Windows 10/11 Evaluation (free, 90-180 days):
- **Windows 10**: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise
- **Windows 11**: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise
- **Size**: ~5-6 GB download

---

## VM Setup

### Step 1: Create Virtual Machine

**Using VirtualBox GUI:**

1. **Open VirtualBox** → New

2. **Basic Settings:**
   - Name: `tpmontrouge-build-win`
   - Type: Microsoft Windows
   - Version: Windows 10 (64-bit) or Windows 11 (64-bit)
   - Memory: 2048-3072 MB (2-3 GB)
   - Hard disk: Create a virtual hard disk (40-50 GB, dynamically allocated)

3. **System Settings** (Settings → System):
   - **Processor**: 2 CPUs
   - **Boot Order**: Optical, Hard Disk
   - **Enable PAE/NX**: ✓
   - **Paravirtualization**: Hyper-V (for better performance)

4. **Display Settings** (Settings → Display):
   - Video Memory: 128 MB
   - Graphics Controller: VBoxVGA or VMSVGA

5. **Network Settings** (Settings → Network):
   - Adapter 1: Attached to NAT
   - **Port Forwarding** (click Advanced → Port Forwarding):
     ```
     Name     Protocol   Host IP     Host Port   Guest IP   Guest Port
     SSH      TCP        127.0.0.1   2222                   22
     RDP      TCP        127.0.0.1   3389                   3389
     ```

6. **Attach ISO:**
   - Settings → Storage → Controller: IDE → Empty
   - Click disk icon → Choose disk file
   - Select downloaded Windows ISO

**Using Command Line:**

```bash
# Create VM
VBoxManage createvm --name "tpmontrouge-build-win" --ostype "Windows10_64" --register

# Configure VM
VBoxManage modifyvm "tpmontrouge-build-win" \
  --memory 2048 \
  --cpus 2 \
  --vram 128 \
  --nic1 nat \
  --natpf1 "SSH,tcp,127.0.0.1,2222,,22" \
  --natpf1 "RDP,tcp,127.0.0.1,3389,,3389" \
  --graphicscontroller vmsvga \
  --paravirtprovider hyperv

# Create disk (50 GB, dynamic)
VBoxManage createhd --filename ~/VirtualBox\ VMs/tpmontrouge-build-win/tpmontrouge-build-win.vdi --size 51200

# Attach disk
VBoxManage storagectl "tpmontrouge-build-win" --name "SATA" --add sata --controller IntelAhci
VBoxManage storageattach "tpmontrouge-build-win" --storagectl "SATA" --port 0 --device 0 --type hdd \
  --medium ~/VirtualBox\ VMs/tpmontrouge-build-win/tpmontrouge-build-win.vdi

# Attach ISO
VBoxManage storagectl "tpmontrouge-build-win" --name "IDE" --add ide
VBoxManage storageattach "tpmontrouge-build-win" --storagectl "IDE" --port 0 --device 0 --type dvddrive \
  --medium ~/Downloads/Windows10_Eval.iso
```

### Step 2: Install Windows

1. **Start VM:**
   ```bash
   VBoxManage startvm "tpmontrouge-build-win"
   # Or use VirtualBox GUI: Right-click → Start → Normal Start
   ```

2. **Windows Installation:**
   - Language: English (or your preference)
   - **Edition**: Windows 10/11 Enterprise Evaluation
   - **License**: Skip (evaluation doesn't need key)
   - **Installation Type**: Custom: Install Windows only
   - **Partition**: Select unallocated space → Next

3. **Initial Setup:**
   - **Account**: Create local account (e.g., `builduser`)
     - Skip Microsoft account sign-in
   - **Privacy**: Disable telemetry options (optional)
   - **Cortana**: Decline (optional)

4. **First Boot:**
   - Wait for desktop to load
   - Check for Windows Updates: Settings → Update & Security → Check for updates
   - Install updates and reboot if needed

---

## Windows Configuration

### Step 3: Install OpenSSH Server

Windows 10/11 includes OpenSSH as an optional feature.

**Method 1: Via Settings (GUI)**

1. **Open Settings** → Apps → Optional Features
2. **Add a feature** → Search "OpenSSH Server"
3. Install and wait for completion
4. **Start service:**
   - Press Win+R → `services.msc` → Enter
   - Find "OpenSSH SSH Server"
   - Right-click → Properties
   - Startup type: Automatic
   - Click "Start"

**Method 2: Via PowerShell (Administrator)**

```powershell
# Open PowerShell as Administrator
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start and enable service
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Verify firewall rule (should be created automatically)
Get-NetFirewallRule -Name *ssh*

# If no rule exists, create one
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' `
  -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

**Test SSH from Linux:**
```bash
# Test connection (use Windows password)
ssh builduser@localhost -p 2222

# Expected output:
# Microsoft Windows [Version 10.0.xxxxx]
# (c) Microsoft Corporation. All rights reserved.
# builduser@HOSTNAME C:\Users\builduser>
```

### Step 4: Configure SSH Key Authentication

**On Linux Host:**
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "tpmontrouge-build-vm" -f ~/.ssh/tpmontrouge_vm
# Press Enter for no passphrase (or set one)

# Display public key
cat ~/.ssh/tpmontrouge_vm.pub
# Copy the output (starts with ssh-ed25519...)
```

**On Windows VM (PowerShell):**
```powershell
# Create .ssh directory
mkdir $HOME\.ssh

# Create authorized_keys file
# Paste your public key on a single line
notepad $HOME\.ssh\authorized_keys

# Set correct permissions (important!)
icacls $HOME\.ssh\authorized_keys /inheritance:r
icacls $HOME\.ssh\authorized_keys /grant:r "$env:USERNAME:F"
icacls $HOME\.ssh\authorized_keys /remove "NT AUTHORITY\Authenticated Users"
```

**Test passwordless SSH:**
```bash
# On Linux
ssh -i ~/.ssh/tpmontrouge_vm builduser@localhost -p 2222 "echo SSH works"

# Add to ~/.ssh/config for convenience
cat >> ~/.ssh/config <<EOF

Host tpmontrouge-vm
    HostName localhost
    Port 2222
    User builduser
    IdentityFile ~/.ssh/tpmontrouge_vm
EOF

# Now you can just use:
ssh tpmontrouge-vm "echo test"
```

### Step 5: Enable Remote Desktop (Optional)

**Windows Settings:**
1. Settings → System → Remote Desktop
2. Enable Remote Desktop: On
3. Confirm firewall prompt

**Connect from Linux:**
```bash
# Install RDP client
sudo apt install freerdp2-x11
# or
sudo apt install remmina

# Connect
xfreerdp /v:localhost:3389 /u:builduser /w:1280 /h:720
```

### Step 6: Install VirtualBox Guest Additions

**Purpose**: Better performance, clipboard sharing, drag-and-drop

1. VM menu → Devices → Insert Guest Additions CD image
2. Open File Explorer → This PC → CD Drive (VBox Guest Additions)
3. Run `VBoxWindowsAdditions.exe`
4. Follow installer (defaults are fine)
5. Reboot when prompted

---

## Development Tools Installation

### Step 7: Install Git for Windows

**Download**: https://git-scm.com/download/win

**Installation options:**
- ✓ Add to PATH (default)
- ✓ Use Git from command line and 3rd party software
- Editor: Nano or Notepad++ (your preference)
- Line endings: Checkout as-is, commit as-is
- Terminal: Use Windows default console

**Verify installation:**
```powershell
git --version
# Output: git version 2.x.x.windows.x
```

### Step 8: Install Python 3.12

**Download**: https://www.python.org/downloads/windows/
- Get "Windows installer (64-bit)"

**Installation (IMPORTANT):**
- ✅ **Check "Add Python 3.12 to PATH"** (at bottom)
- ✅ **Check "Install for all users"** (if prompted)
- Click "Install Now"

**Verify installation:**
```powershell
python --version
# Output: Python 3.12.x

pip --version
# Output: pip 24.x.x from ...
```

**Install Python packages:**
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install TPMontrouge dependencies
pip install numpy scipy matplotlib PyQt5 pyqtgraph pyinstaller

# Verify installations
pip list
```

### Step 9: Install Inno Setup

**Download**: https://jrsoftware.org/isdl.php
- Download "Inno Setup 6.x.x"

**Installation:**
- Install to default location: `C:\Program Files (x86)\Inno Setup 6\`
- Accept all defaults

**Add to PATH (PowerShell Administrator):**
```powershell
# Add Inno Setup to system PATH
$path = [Environment]::GetEnvironmentVariable("Path", "Machine")
$innoPath = "C:\Program Files (x86)\Inno Setup 6"
if ($path -notlike "*$innoPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$path;$innoPath", "Machine")
}

# Restart PowerShell to pick up changes
```

**Verify:**
```powershell
# After restarting PowerShell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /?
# Should show Inno Setup help
```

---

## Repository Setup

### Step 10: Clone Repository

**On Windows VM (PowerShell):**
```powershell
# Create build directory
mkdir C:\builds
cd C:\builds

# Clone repository
git clone https://github.com/Agreg-Montrouge/interfacage.git
cd interfacage\tpmontrouge

# Switch to development branch
git checkout dev2026

# Verify
git branch
# Should show: * dev2026
```

### Step 11: Copy Build Scripts

**The build scripts were created on Linux host, so copy them to VM:**

**Option A: Via SSH/SCP (from Linux):**
```bash
# Copy PowerShell scripts to VM
scp -P 2222 /home/pierre/python-projects/montrouge/tpmontrouge/build_local.ps1 \
  builduser@localhost:C:/builds/interfacage/tpmontrouge/

scp -P 2222 /home/pierre/python-projects/montrouge/tpmontrouge/test_builds.ps1 \
  builduser@localhost:C:/builds/interfacage/tpmontrouge/
```

**Option B: Via Git (if scripts are committed):**
```powershell
# On Windows VM
cd C:\builds\interfacage\tpmontrouge
git pull origin dev2026
```

**Option C: Manual copy (via RDP):**
- Connect via RDP
- Copy files from shared clipboard or network location

---

## Usage

### Basic Workflow

**From Linux Host:**

```bash
# 1. Edit code on Linux
cd /home/pierre/python-projects/montrouge/tpmontrouge
# ... make changes ...

# 2. Trigger build on Windows VM
../scripts/build-windows-vm.sh

# 3. Test artifacts (copied to dist-windows/)
ls -lh dist-windows/
```

**From Windows VM directly:**

```powershell
# SSH into VM
ssh -p 2222 builduser@localhost

# Run build
cd C:\builds\interfacage\tpmontrouge
powershell -ExecutionPolicy Bypass -File build_local.ps1

# Run tests
powershell -ExecutionPolicy Bypass -File test_builds.ps1

# Test GUI applications via RDP
# Connect with RDP and double-click .exe files in scripts\dist\
```

### Build Script Options

**build_local.ps1 options:**
```powershell
# Full build
powershell -ExecutionPolicy Bypass -File build_local.ps1

# Skip installer (faster)
powershell -ExecutionPolicy Bypass -File build_local.ps1 -SkipInstaller

# Skip tests
powershell -ExecutionPolicy Bypass -File build_local.ps1 -SkipTests

# Verbose output
powershell -ExecutionPolicy Bypass -File build_local.ps1 -Verbose

# Combine options
powershell -ExecutionPolicy Bypass -File build_local.ps1 -SkipTests -Verbose
```

**build-windows-vm.sh options (Linux):**
```bash
# Full build with sync and fetch
./scripts/build-windows-vm.sh

# Skip syncing code (use existing code on VM)
./scripts/build-windows-vm.sh --no-sync

# Skip fetching artifacts
./scripts/build-windows-vm.sh --no-fetch

# Quick build (skip installer and tests)
./scripts/build-windows-vm.sh --skip-installer --skip-tests

# Verbose PyInstaller output
./scripts/build-windows-vm.sh --verbose

# Show help
./scripts/build-windows-vm.sh --help
```

### Example Workflows

**Workflow 1: Quick Development Test**
```bash
# On Linux - edit code, quick test
cd /home/pierre/python-projects/montrouge
# ... edit files ...
./scripts/build-windows-vm.sh --skip-installer --skip-tests
```

**Workflow 2: Full Build Before Push**
```bash
# Complete build with all checks
./scripts/build-windows-vm.sh

# If successful, commit and push
cd tpmontrouge
git add .
git commit -m "Update feature"
git push origin dev2026
```

**Workflow 3: Debug Build Issue**
```bash
# SSH into VM for investigation
ssh -p 2222 builduser@localhost

# Try verbose build
cd C:\builds\interfacage\tpmontrouge
powershell -ExecutionPolicy Bypass -File build_local.ps1 -Verbose

# Check logs, dependencies, etc.
pip list
python -c "import tpmontrouge; print(tpmontrouge.__version__)"
```

---

## Troubleshooting

### SSH Issues

**Problem: "Connection refused"**
```powershell
# On Windows VM - check SSH service
Get-Service sshd
# If stopped:
Start-Service sshd

# Check if listening on port 22
netstat -an | findstr :22
```

**Problem: "Permission denied (publickey)"**
```powershell
# Check authorized_keys permissions
icacls $HOME\.ssh\authorized_keys

# Should only show your username
# If not, reset permissions:
icacls $HOME\.ssh\authorized_keys /inheritance:r
icacls $HOME\.ssh\authorized_keys /grant:r "$env:USERNAME:F"
```

**Problem: VM not accessible**
```bash
# Check VM is running
VBoxManage list runningvms

# Start if needed
VBoxManage startvm tpmontrouge-build-win --type headless

# Check port forwarding
VBoxManage showvminfo tpmontrouge-build-win | grep "NIC.*Rule"
```

### Build Issues

**Problem: "Module not found" errors**
```powershell
# Reinstall dependencies
pip install --force-reinstall numpy scipy matplotlib PyQt5 pyqtgraph pyinstaller

# Check Python can import modules
python -c "import numpy, scipy, matplotlib, PyQt5, pyqtgraph"
```

**Problem: PyInstaller fails**
```powershell
# Clean PyInstaller cache
python -m PyInstaller --clean empty_bode.spec

# Try with verbose output
pyinstaller -y --log-level DEBUG empty_bode.spec
```

**Problem: Inno Setup not found**
```powershell
# Check installation
Test-Path "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

# Add to PATH temporarily
$env:Path += ";C:\Program Files (x86)\Inno Setup 6\"

# Add permanently (requires admin)
[Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Program Files (x86)\Inno Setup 6\", "Machine")
```

### Performance Issues

**Slow VM performance:**
1. Enable VT-x/AMD-V in BIOS
2. Install VirtualBox Guest Additions
3. Increase RAM: Settings → System → Base Memory → 3072 MB
4. Use paravirtualization: Settings → System → Paravirtualization → Hyper-V

**Slow file transfers:**
```bash
# Use compression with rsync
rsync -avz -e "ssh -p 2222 -C" ...
```

### RDP Issues

**Can't connect via RDP:**
1. Check RDP is enabled on Windows:
   ```powershell
   Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections"
   # Should return 0 (enabled)
   ```

2. Enable RDP:
   ```powershell
   Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
   ```

3. Check firewall:
   ```powershell
   Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
   ```

---

## Maintenance

### VM Management

**Start/Stop VM:**
```bash
# Start (headless mode - no GUI)
VBoxManage startvm tpmontrouge-build-win --type headless

# Save state (fast pause/resume)
VBoxManage controlvm tpmontrouge-build-win savestate

# Graceful shutdown
VBoxManage controlvm tpmontrouge-build-win acpipowerbutton

# Force power off (not recommended)
VBoxManage controlvm tpmontrouge-build-win poweroff
```

**Snapshots (backup before changes):**
```bash
# Create snapshot
VBoxManage snapshot tpmontrouge-build-win take "clean-build-env" \
  --description "Fresh build environment with all tools"

# List snapshots
VBoxManage snapshot tpmontrouge-build-win list

# Restore snapshot
VBoxManage snapshot tpmontrouge-build-win restore "clean-build-env"
```

### Windows Updates

**Monthly maintenance:**
```powershell
# Check for updates
Start-Process "ms-settings:windowsupdate"

# Or via PowerShell (Windows 11)
Get-WindowsUpdate
Install-WindowsUpdate
```

### Extend Evaluation License

**When license expires (90 days):**
```powershell
# Run as Administrator
slmgr /rearm

# Restart VM
shutdown /r /t 0
```

**Note**: Can rearm 3-6 times (depends on edition), giving 270-540 days total.

### Update Python Packages

**Quarterly updates:**
```powershell
# Update pip
python -m pip install --upgrade pip

# Update all packages
pip list --outdated
pip install --upgrade pyinstaller setuptools wheel
pip install --upgrade numpy scipy matplotlib PyQt5 pyqtgraph
```

### Cleanup Disk Space

```powershell
# Clean build artifacts
cd C:\builds\interfacage\tpmontrouge
Remove-Item -Recurse -Force scripts\dist\, scripts\build\

# Clean Python cache
py -m pip cache purge

# Windows Disk Cleanup
cleanmgr /d C:
```

---

## Quick Reference

### Essential Commands

**Linux Host:**
```bash
# Start VM
VBoxManage startvm tpmontrouge-build-win --type headless

# Trigger build
./scripts/build-windows-vm.sh

# SSH to VM
ssh -p 2222 builduser@localhost

# RDP to VM
xfreerdp /v:localhost:3389 /u:builduser

# Stop VM
VBoxManage controlvm tpmontrouge-build-win acpipowerbutton
```

**Windows VM:**
```powershell
# Build
cd C:\builds\interfacage\tpmontrouge
powershell -ExecutionPolicy Bypass -File build_local.ps1

# Test
powershell -ExecutionPolicy Bypass -File test_builds.ps1

# Update code
git pull origin dev2026

# Check status
python --version
pip list
git status
```

### Resource Requirements

- **RAM**: 2-3 GB for VM
- **Disk**: 40-50 GB (20 GB Windows + 20-30 GB builds)
- **CPU**: 2 cores
- **Build time**: 3-5 minutes (full build)
- **Network**: Required for initial setup, optional after

### Comparison: VM vs GitHub Actions

| Feature | VM | GitHub Actions |
|---------|----|----|
| Setup time | 1-2 hours | ✓ Done |
| Build speed | 3-5 min | 8-10 min |
| Cost | Host resources | Free (public) |
| Debugging | Full control | Logs only |
| Iteration | Instant | Push required |
| Multi-platform | Windows only | Linux + Windows |
| Maintenance | Manual | Automatic |

**Recommendation**: Use VM for development, GitHub Actions for releases.

---

## Next Steps

1. **Create VM** following this guide
2. **Test build** with `build-windows-vm.sh`
3. **Test GUI** via RDP
4. **Create snapshot** after successful setup
5. **Integrate** into your development workflow

For questions or issues, refer to the Troubleshooting section or check:
- VirtualBox documentation: https://www.virtualbox.org/manual/
- Python packaging guide: https://packaging.python.org/
- PyInstaller docs: https://pyinstaller.org/

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-03  
**Maintained in**: `/home/pierre/python-projects/montrouge/docs/WINDOWS_VM_SETUP.md`

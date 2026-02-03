# Windows VM Quick Start Guide

**Quick reference for experienced users. For detailed instructions, see [WINDOWS_VM_SETUP.md](WINDOWS_VM_SETUP.md).**

## Prerequisites
- VirtualBox installed
- Windows 10/11 Evaluation ISO downloaded
- SSH key generated (`~/.ssh/id_rsa.pub`)

## Setup Checklist

### 1. Create VM (5 minutes)
```bash
VM_NAME="tpmontrouge-build-win"

VBoxManage createvm --name "$VM_NAME" --ostype "Windows10_64" --register
VBoxManage modifyvm "$VM_NAME" \
  --memory 3072 \
  --cpus 2 \
  --vram 128 \
  --nic1 nat \
  --natpf1 "ssh,tcp,,2222,,22" \
  --natpf1 "rdp,tcp,,3389,,3389" \
  --audio none \
  --clipboard bidirectional

VBoxManage createhd --filename ~/VirtualBox\ VMs/$VM_NAME/$VM_NAME.vdi --size 51200
VBoxManage storagectl "$VM_NAME" --name "SATA" --add sata --controller IntelAhci
VBoxManage storageattach "$VM_NAME" --storagectl "SATA" --port 0 --device 0 \
  --type hdd --medium ~/VirtualBox\ VMs/$VM_NAME/$VM_NAME.vdi
VBoxManage storageattach "$VM_NAME" --storagectl "SATA" --port 1 --device 0 \
  --type dvddrive --medium ~/path/to/windows.iso

VBoxManage startvm "$VM_NAME"
```

### 2. Install Windows (20-30 minutes)
- Boot from ISO, install Windows 10/11 Evaluation
- Username: `builduser`, Password: `<your-choice>`
- Skip network setup initially
- Let Windows update

### 3. Configure SSH (5 minutes)
**Run in PowerShell (Admin):**
```powershell
# Install OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# Start and enable SSH service
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# Configure firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' `
  -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

# Configure public key authentication
mkdir C:\Users\builduser\.ssh
# Paste your public key into C:\Users\builduser\.ssh\authorized_keys
# Set proper permissions
icacls C:\Users\builduser\.ssh\authorized_keys /inheritance:r
icacls C:\Users\builduser\.ssh\authorized_keys /grant "builduser:R"
```

**Test from Linux host:**
```bash
ssh -p 2222 builduser@localhost
```

### 4. Install Development Tools (10 minutes)
**Run in PowerShell (Admin):**
```powershell
# Install Chocolatey (package manager)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install -y git python312 innosetup

# Verify installations
git --version
python --version
pip --version
iscc /?
```

**Install Python packages:**
```powershell
pip install --upgrade pip
pip install pyinstaller numpy scipy matplotlib PyQt5 pyqtgraph pyvisa pyvisa-py
```

### 5. Clone Repository (2 minutes)
```powershell
mkdir C:\builds
cd C:\builds
git clone https://github.com/Agreg-Montrouge/interfacage.git
cd interfacage\tpmontrouge
git checkout dev2026
```

### 6. Test Build System (5 minutes)
**From Linux host:**
```bash
cd /home/pierre/python-projects/montrouge

# Start VM
./scripts/vm-manage.sh start

# Trigger build
./scripts/build-windows-vm.sh

# Check artifacts
ls -lh tpmontrouge/dist-windows/
```

**Expected output:**
```
tpmontrouge/dist-windows/
├── empty_bode-2025.01.r0-win64.exe (~93 MB)
├── interface-2025.01.r0-win64.exe (~93 MB)
└── interface_agreg_setup-2025.01.r0.exe (~62 MB)
```

### 7. Create Clean Snapshot
```bash
./scripts/vm-manage.sh snapshot "clean-build-env"
```

## Common Commands

### VM Management
```bash
./scripts/vm-manage.sh start         # Start VM
./scripts/vm-manage.sh stop          # Stop VM
./scripts/vm-manage.sh status        # Check if running
./scripts/vm-manage.sh ssh           # SSH into VM
./scripts/vm-manage.sh rdp           # RDP into VM (GUI)
./scripts/vm-manage.sh info          # Show VM details
```

### Building
```bash
# Full build (tests + installer)
./scripts/build-windows-vm.sh

# Fast build (skip tests and installer)
./scripts/build-windows-vm.sh --skip-installer --skip-tests

# Verbose output for debugging
./scripts/build-windows-vm.sh --verbose

# Build without syncing code (use existing VM files)
./scripts/build-windows-vm.sh --no-sync
```

### Testing Executables
**Via RDP:**
```bash
./scripts/vm-manage.sh rdp
# Navigate to C:\builds\interfacage\tpmontrouge\scripts\dist\
# Double-click interface.exe or empty_bode.exe
```

**Manual SSH test:**
```bash
ssh -p 2222 builduser@localhost
cd C:\builds\interfacage\tpmontrouge
powershell -ExecutionPolicy Bypass -File test_builds.ps1
```

## Troubleshooting Quick Fixes

### SSH connection refused
```bash
# Restart SSH service on Windows
ssh -p 2222 builduser@localhost "Restart-Service sshd"
```

### Build fails with "Module not found"
```bash
ssh -p 2222 builduser@localhost "pip install --force-reinstall numpy scipy matplotlib PyQt5 pyqtgraph"
```

### VM won't start
```bash
# Check VM state
VBoxManage showvminfo tpmontrouge-build-win | grep State

# Force stop and restart
VBoxManage controlvm tpmontrouge-build-win poweroff
./scripts/vm-manage.sh start
```

### Restore to clean state
```bash
./scripts/vm-manage.sh restore "clean-build-env"
```

## Development Workflow

### Typical iteration cycle:
1. Edit code on Linux host
2. Run `./scripts/build-windows-vm.sh --skip-installer --skip-tests` (fast)
3. Check artifacts in `tpmontrouge/dist-windows/`
4. Test via RDP if needed
5. Commit when satisfied

### Before pushing to GitHub:
```bash
# Full build with all checks
./scripts/build-windows-vm.sh

# If successful:
git add .
git commit -m "Update feature"
git push origin dev2026

# GitHub Actions runs automatically for full CI
```

## File Locations

**Linux Host:**
- Build script: `/home/pierre/python-projects/montrouge/scripts/build-windows-vm.sh`
- VM manager: `/home/pierre/python-projects/montrouge/scripts/vm-manage.sh`
- Artifacts: `/home/pierre/python-projects/montrouge/tpmontrouge/dist-windows/`

**Windows VM:**
- Repository: `C:\builds\interfacage\tpmontrouge\`
- Build script: `C:\builds\interfacage\tpmontrouge\build_local.ps1`
- Test script: `C:\builds\interfacage\tpmontrouge\test_builds.ps1`
- Artifacts: `C:\builds\interfacage\tpmontrouge\scripts\dist\`

## Resources

- **Detailed Setup Guide:** [WINDOWS_VM_SETUP.md](WINDOWS_VM_SETUP.md)
- **Windows Evaluation ISOs:**
  - Windows 10: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise
  - Windows 11: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise
- **Repository:** https://github.com/Agreg-Montrouge/interfacage
- **CI/CD Status:** https://github.com/Agreg-Montrouge/interfacage/actions

## Maintenance

### Weekly
```bash
# Update Windows (in RDP)
# Update Python packages
ssh -p 2222 builduser@localhost "pip install --upgrade pip pyinstaller numpy scipy matplotlib PyQt5 pyqtgraph"

# Create new snapshot
./scripts/vm-manage.sh snapshot "weekly-$(date +%Y%m%d)"
```

### Before VM expires (90 days)
```powershell
# Extend evaluation period (up to 5 times)
slmgr /rearm
# Reboot VM
```

---

**Total setup time:** ~45-60 minutes  
**Subsequent builds:** 3-5 minutes

For questions or issues, refer to the detailed guide: [WINDOWS_VM_SETUP.md](WINDOWS_VM_SETUP.md)

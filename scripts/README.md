# Build Scripts

This directory contains scripts for building TPMontrouge Windows executables.

## Overview

TPMontrouge uses a **hybrid build system**:
- **GitHub Actions**: Automated CI/CD on every push (primary release method)
- **Local Windows VM**: Fast iteration and debugging during development

## Scripts in This Directory

### `build-windows-vm.sh` ⭐ Main Build Script
**Purpose:** Trigger Windows builds from Linux host via VirtualBox VM

**Usage:**
```bash
./scripts/build-windows-vm.sh [options]

Options:
  --no-sync        Skip syncing code to VM
  --no-fetch       Skip fetching artifacts back
  --skip-installer Skip building Inno Setup installer (faster)
  --skip-tests     Skip running tests
  --verbose        Show detailed PyInstaller output
  --help           Show help message
```

**What it does:**
1. Syncs current code to Windows VM via rsync
2. Executes PowerShell build script remotely
3. Fetches built executables back to `tpmontrouge/dist-windows/`
4. Shows build summary and artifact locations

**Examples:**
```bash
# Full build (tests + installer)
./scripts/build-windows-vm.sh

# Fast build (skip tests and installer for quick iteration)
./scripts/build-windows-vm.sh --skip-installer --skip-tests

# Debug build issues with verbose output
./scripts/build-windows-vm.sh --verbose

# Build without re-syncing code (use existing VM files)
./scripts/build-windows-vm.sh --no-sync
```

**Requirements:**
- VirtualBox VM running Windows 10/11
- SSH access configured (port 2222)
- Development tools installed on VM (see docs/WINDOWS_VM_SETUP.md)

---

### `vm-manage.sh` - VM Management Helper
**Purpose:** Manage VirtualBox VM lifecycle and connections

**Usage:**
```bash
./scripts/vm-manage.sh <command>

Commands:
  start             Start the VM
  stop              Stop the VM gracefully
  restart           Restart the VM
  status            Check if VM is running
  ssh               SSH into VM
  rdp               Open RDP connection (GUI)
  snapshot <name>   Create snapshot
  restore <name>    Restore snapshot
  list-snapshots    List all snapshots
  info              Show VM configuration
  help              Show help message
```

**Examples:**
```bash
# Start VM
./scripts/vm-manage.sh start

# Check status
./scripts/vm-manage.sh status

# SSH into VM for debugging
./scripts/vm-manage.sh ssh

# Open GUI for testing executables
./scripts/vm-manage.sh rdp

# Create snapshot before major changes
./scripts/vm-manage.sh snapshot "before-python-upgrade"

# Restore to clean state
./scripts/vm-manage.sh restore "clean-build-env"
```

---

## PowerShell Scripts (in `tpmontrouge/`)

These scripts run **inside the Windows VM**:

### `build_local.ps1` - Windows Build Script
Builds executables using PyInstaller and creates Inno Setup installer.

**Triggered by:** `build-windows-vm.sh` (or run manually in VM)

**Location on Windows VM:** `C:\builds\interfacage\tpmontrouge\build_local.ps1`

### `test_builds.ps1` - Executable Testing
Smoke tests for built executables (verifies they launch without crashing).

**Location on Windows VM:** `C:\builds\interfacage\tpmontrouge\test_builds.ps1`

---

## PyInstaller Spec Files

Located in this directory (`scripts/`):

- **`empty_bode.spec`** - Spec for empty_bode.exe (Bode plot generator)
- **`interface.spec`** - Spec for interface.exe (main GUI application)
- **`interface_folder.spec`** - Alternative spec (folder distribution)
- **`interface_gui.iss.tpl`** - Inno Setup installer template

These are used by both GitHub Actions and the local VM build system.

---

## Build Artifacts

### GitHub Actions Artifacts
**Location:** GitHub Actions run page → Artifacts section  
**Retention:** 90 days  
**Access:** Download from GitHub web interface or via `gh run download`

**Files:**
- `empty_bode-VERSION-win64.exe` (~93 MB)
- `interface-VERSION-win64.exe` (~93 MB)
- `interface_agreg_setup-VERSION.exe` (~62 MB) - Installer

### Local VM Artifacts
**Location:** `tpmontrouge/dist-windows/` (on Linux host)  
**Created by:** `build-windows-vm.sh`

**Same files as GitHub Actions**, but available immediately on your local machine.

---

## Typical Workflows

### Development Iteration (Fast)
```bash
# 1. Edit code on Linux
vim tpmontrouge/tpmontrouge/interface/bode_plot.py

# 2. Quick build (3-5 minutes)
./scripts/build-windows-vm.sh --skip-installer --skip-tests

# 3. Check artifacts
ls -lh tpmontrouge/dist-windows/

# 4. Test via RDP if needed
./scripts/vm-manage.sh rdp
```

### Pre-Push Validation (Full)
```bash
# 1. Full build with all checks
./scripts/build-windows-vm.sh

# 2. If successful, push
git add .
git commit -m "Update feature"
git push origin dev2026

# 3. GitHub Actions runs automatically for official CI
```

### Debugging Build Issues
```bash
# 1. SSH into VM
./scripts/vm-manage.sh ssh

# 2. Run build manually with verbose output
cd C:\builds\interfacage\tpmontrouge
powershell -ExecutionPolicy Bypass -File build_local.ps1 -Verbose

# 3. Check PyInstaller warnings
cat scripts\build\interface\warn-interface.txt
```

### Testing GUI Applications
```bash
# 1. Open RDP connection
./scripts/vm-manage.sh rdp

# 2. In Windows VM, navigate to:
C:\builds\interfacage\tpmontrouge\scripts\dist\

# 3. Double-click interface.exe or empty_bode.exe
```

---

## Setup Instructions

See detailed setup guides in `docs/`:

- **[WINDOWS_VM_SETUP.md](../docs/WINDOWS_VM_SETUP.md)** - Comprehensive guide with troubleshooting
- **[WINDOWS_VM_QUICKSTART.md](../docs/WINDOWS_VM_QUICKSTART.md)** - Quick reference for experienced users

**TL;DR:**
1. Create VirtualBox VM with Windows 10/11 Evaluation
2. Configure SSH server (OpenSSH)
3. Install: Git, Python 3.12, PyInstaller, Inno Setup
4. Clone repository to `C:\builds\interfacage\tpmontrouge`
5. Run `./scripts/build-windows-vm.sh` from Linux host

**Setup time:** ~45-60 minutes  
**Subsequent builds:** 3-5 minutes

---

## Environment Variables

You can customize VM connection settings:

```bash
# VM connection settings
export VM_HOST="localhost"        # VM hostname
export VM_PORT="2222"             # SSH port
export VM_USER="builduser"        # SSH username
export REPO_PATH="C:/builds/interfacage/tpmontrouge"  # Windows path

# Then run build
./scripts/build-windows-vm.sh
```

---

## Troubleshooting

### VM not accessible
```bash
# Check VM status
./scripts/vm-manage.sh status

# Start VM if stopped
./scripts/vm-manage.sh start

# Verify SSH service in VM
ssh -p 2222 builduser@localhost "Get-Service sshd"
```

### Build fails with "Module not found"
```bash
# Reinstall Python packages in VM
ssh -p 2222 builduser@localhost "pip install --force-reinstall numpy scipy matplotlib PyQt5 pyqtgraph pyinstaller"
```

### Inno Setup not found
```bash
# Check installation
ssh -p 2222 builduser@localhost 'Test-Path "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"'

# Or skip installer for faster builds
./scripts/build-windows-vm.sh --skip-installer
```

### Restore to clean state
```bash
# List available snapshots
./scripts/vm-manage.sh list-snapshots

# Restore to clean build environment
./scripts/vm-manage.sh restore "clean-build-env"
```

---

## File Locations Reference

### Linux Host
```
/home/pierre/python-projects/montrouge/
├── scripts/
│   ├── build-windows-vm.sh       ← Main build trigger
│   ├── vm-manage.sh               ← VM management
│   ├── empty_bode.spec            ← PyInstaller specs
│   ├── interface.spec
│   └── interface_gui.iss.tpl      ← Inno Setup template
├── tpmontrouge/
│   ├── build_local.ps1            ← Windows build script
│   ├── test_builds.ps1            ← Windows test script
│   └── dist-windows/              ← Build artifacts (created by build-windows-vm.sh)
└── docs/
    ├── WINDOWS_VM_SETUP.md        ← Detailed setup guide
    └── WINDOWS_VM_QUICKSTART.md   ← Quick reference
```

### Windows VM
```
C:\builds\interfacage\tpmontrouge\
├── build_local.ps1                ← Main build script
├── test_builds.ps1                ← Test script
├── scripts\
│   ├── dist\                      ← Build artifacts (executables)
│   ├── build\                     ← PyInstaller build cache
│   ├── empty_bode.spec
│   ├── interface.spec
│   └── interface_gui.iss.tpl
└── tpmontrouge\                   ← Python package source
```

---

## CI/CD Integration

**GitHub Actions workflows** (`.github/workflows/`):
- `test.yml` - Run tests on Linux + Windows (Python 3.10, 3.11, 3.12)
- `build-windows.yml` - Build Windows executables
- `release.yml` - Create GitHub releases on tags

**When to use what:**
- **Local VM**: Fast iteration, debugging, GUI testing
- **GitHub Actions**: Official releases, multi-platform CI, automated on every push

**Build times:**
- Local VM: 3-5 minutes (fast iteration), 8-10 minutes (full build)
- GitHub Actions: 8-10 minutes (official releases)

---

## Resources

- **Repository:** https://github.com/Agreg-Montrouge/interfacage
- **CI/CD Status:** https://github.com/Agreg-Montrouge/interfacage/actions
- **Windows Evaluation ISOs:**
  - Windows 10: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise
  - Windows 11: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise

---

For questions or issues, refer to the detailed guides in `docs/` or check GitHub Actions logs.

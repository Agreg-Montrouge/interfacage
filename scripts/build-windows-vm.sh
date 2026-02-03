#!/bin/bash
# Trigger Windows build on local VM
# Usage: ./build-windows-vm.sh [options]
#
# Options:
#   --no-sync        Skip syncing code to VM (use existing code)
#   --no-fetch       Skip fetching artifacts back
#   --skip-installer Skip building installer (faster)
#   --skip-tests     Skip running tests
#   --verbose        Show detailed PyInstaller output
#   --help           Show this help message

set -e

# Configuration - EDIT THESE VALUES
VM_HOST="${VM_HOST:-localhost}"
VM_PORT="${VM_PORT:-2222}"
VM_USER="${VM_USER:-builduser}"
REPO_PATH="${REPO_PATH:-C:/builds/interfacage/tpmontrouge}"
LOCAL_REPO="$(cd "$(dirname "$0")/../tpmontrouge" && pwd)"

# Parse arguments
SYNC=true
FETCH=true
SKIP_INSTALLER=""
SKIP_TESTS=""
VERBOSE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-sync)
            SYNC=false
            shift
            ;;
        --no-fetch)
            FETCH=false
            shift
            ;;
        --skip-installer)
            SKIP_INSTALLER="-SkipInstaller"
            shift
            ;;
        --skip-tests)
            SKIP_TESTS="-SkipTests"
            shift
            ;;
        --verbose)
            VERBOSE="-Verbose"
            shift
            ;;
        --help)
            grep "^#" "$0" | grep -v "^#!/" | sed 's/^# //'
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Triggering Windows VM Build${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Check VM is reachable
echo -e "${YELLOW}Checking VM connection...${NC}"
if ! ssh -p $VM_PORT -o ConnectTimeout=5 -o BatchMode=yes $VM_USER@$VM_HOST "echo VM is accessible" > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Cannot connect to Windows VM${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Make sure VM is running:"
    echo "     VBoxManage list runningvms"
    echo "  2. Start VM if needed:"
    echo "     VBoxManage startvm tpmontrouge-build-win --type headless"
    echo "  3. Check SSH service on Windows:"
    echo "     ssh -p $VM_PORT $VM_USER@$VM_HOST 'Get-Service sshd'"
    echo "  4. Verify port forwarding:"
    echo "     VBoxManage showvminfo tpmontrouge-build-win | grep 'NIC.*Rule'"
    exit 1
fi
echo -e "${GREEN}✓ VM is accessible${NC}"

# Sync code to VM
if [ "$SYNC" = true ]; then
    echo ""
    echo -e "${YELLOW}Syncing code to Windows VM...${NC}"
    
    # Check if local repo exists
    if [ ! -d "$LOCAL_REPO" ]; then
        echo -e "${RED}ERROR: Local repository not found: $LOCAL_REPO${NC}"
        exit 1
    fi
    
    # Use rsync for efficient transfer
    rsync -avz --delete \
        -e "ssh -p $VM_PORT" \
        --exclude='.git/' \
        --exclude='__pycache__/' \
        --exclude='*.pyc' \
        --exclude='dist/' \
        --exclude='build/' \
        --exclude='scripts/dist/' \
        --exclude='scripts/build/' \
        --exclude='*.egg-info/' \
        --exclude='.pytest_cache/' \
        --exclude='dist-windows/' \
        $LOCAL_REPO/ $VM_USER@$VM_HOST:$REPO_PATH/ | grep -v "/$"
    
    echo -e "${GREEN}✓ Code synced successfully${NC}"
else
    echo -e "${CYAN}Skipping code sync (--no-sync)${NC}"
fi

# Run build
echo ""
echo -e "${YELLOW}Running build on Windows VM...${NC}"
echo -e "${CYAN}Build command: powershell -ExecutionPolicy Bypass -File build_local.ps1 $SKIP_INSTALLER $SKIP_TESTS $VERBOSE${NC}"
echo ""

# Execute build with proper error handling
BUILD_CMD="cd $REPO_PATH && powershell -ExecutionPolicy Bypass -File build_local.ps1 $SKIP_INSTALLER $SKIP_TESTS $VERBOSE"
if ssh -p $VM_PORT $VM_USER@$VM_HOST "$BUILD_CMD"; then
    echo ""
    echo -e "${GREEN}✓ Build completed successfully${NC}"
else
    EXIT_CODE=$?
    echo ""
    echo -e "${RED}ERROR: Build failed with exit code $EXIT_CODE${NC}"
    echo ""
    echo "Check the error messages above for details."
    echo "You can connect to the VM to investigate:"
    echo "  ssh -p $VM_PORT $VM_USER@$VM_HOST"
    exit $EXIT_CODE
fi

# Copy artifacts back
if [ "$FETCH" = true ]; then
    echo ""
    echo -e "${YELLOW}Fetching artifacts from Windows VM...${NC}"
    
    # Create local directory for Windows builds
    mkdir -p $LOCAL_REPO/dist-windows/
    
    # Check if artifacts exist on VM
    if ! ssh -p $VM_PORT $VM_USER@$VM_HOST "Test-Path $REPO_PATH/scripts/dist/*.exe" 2>/dev/null; then
        echo -e "${YELLOW}WARNING: No .exe files found on VM${NC}"
    else
        # Copy all .exe files
        scp -P $VM_PORT "$VM_USER@$VM_HOST:$REPO_PATH/scripts/dist/*.exe" $LOCAL_REPO/dist-windows/ 2>/dev/null || true
        
        # Copy build summary if exists
        scp -P $VM_PORT "$VM_USER@$VM_HOST:$REPO_PATH/scripts/dist/build_summary.txt" $LOCAL_REPO/dist-windows/ 2>/dev/null || true
        
        echo -e "${GREEN}✓ Artifacts fetched successfully${NC}"
    fi
else
    echo -e "${CYAN}Skipping artifact fetch (--no-fetch)${NC}"
fi

# Display summary
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Build Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

if [ "$FETCH" = true ] && [ -d "$LOCAL_REPO/dist-windows" ]; then
    echo "Artifacts saved to: $LOCAL_REPO/dist-windows/"
    echo ""
    
    # List artifacts with sizes
    if ls $LOCAL_REPO/dist-windows/*.exe >/dev/null 2>&1; then
        echo "Built executables:"
        ls -lh $LOCAL_REPO/dist-windows/*.exe | awk '{printf "  %-40s %6s\n", $9, $5}'
        
        # Show build summary if available
        if [ -f "$LOCAL_REPO/dist-windows/build_summary.txt" ]; then
            echo ""
            echo "Build summary:"
            cat $LOCAL_REPO/dist-windows/build_summary.txt | grep -E "(Version:|Build Date:)" | sed 's/^/  /'
        fi
    else
        echo -e "${YELLOW}No executables found${NC}"
    fi
else
    echo "Artifacts remain on VM at: $REPO_PATH/scripts/dist/"
    echo "Connect to VM to access: ssh -p $VM_PORT $VM_USER@$VM_HOST"
fi

echo ""
echo "Next steps:"
echo "  • Test executables: wine $LOCAL_REPO/dist-windows/interface.exe"
echo "  • Connect to VM via RDP to test GUI: xfreerdp /v:localhost:3389"
echo "  • View VM files: ssh -p $VM_PORT $VM_USER@$VM_HOST"

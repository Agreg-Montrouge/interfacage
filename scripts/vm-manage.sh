#!/bin/bash
# VM Management Helper for TPMontrouge Windows Build VM
# Simplifies common VirtualBox operations

VM_NAME="tpmontrouge-build-win"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_help() {
    cat <<EOF
TPMontrouge Windows VM Management Tool

Usage: $0 <command> [options]

Commands:
  start           Start the VM (headless mode)
  stop            Gracefully shutdown the VM
  restart         Restart the VM
  status          Show VM status
  ssh             SSH into the VM
  rdp             Connect via RDP (requires freerdp or remmina)
  snapshot        Create a snapshot
  restore         Restore from snapshot
  list-snapshots  List all snapshots
  info            Show VM details
  help            Show this help message

Examples:
  $0 start                          # Start VM
  $0 status                         # Check if running
  $0 ssh                            # SSH to VM
  $0 snapshot "before-update"       # Create snapshot
  $0 restore "clean-build-env"      # Restore snapshot

Options:
  --force         Force power off (stop command only)
  --gui           Start VM with GUI (start command only)
EOF
}

check_vm_exists() {
    if ! VBoxManage list vms | grep -q "\"$VM_NAME\""; then
        echo -e "${RED}ERROR: VM '$VM_NAME' not found${NC}"
        echo "Available VMs:"
        VBoxManage list vms
        exit 1
    fi
}

get_vm_state() {
    VBoxManage showvminfo "$VM_NAME" --machinereadable | grep "VMState=" | cut -d'"' -f2
}

is_vm_running() {
    state=$(get_vm_state)
    [[ "$state" == "running" ]]
}

cmd_start() {
    check_vm_exists
    
    if is_vm_running; then
        echo -e "${YELLOW}VM is already running${NC}"
        return 0
    fi
    
    echo -e "${CYAN}Starting VM '$VM_NAME'...${NC}"
    
    if [[ "$1" == "--gui" ]]; then
        VBoxManage startvm "$VM_NAME"
    else
        VBoxManage startvm "$VM_NAME" --type headless
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ VM started successfully${NC}"
        echo ""
        echo "Connect via:"
        echo "  SSH: ssh -p 2222 builduser@localhost"
        echo "  RDP: xfreerdp /v:localhost:3389 /u:builduser"
    else
        echo -e "${RED}✗ Failed to start VM${NC}"
        return 1
    fi
}

cmd_stop() {
    check_vm_exists
    
    if ! is_vm_running; then
        echo -e "${YELLOW}VM is not running${NC}"
        return 0
    fi
    
    if [[ "$1" == "--force" ]]; then
        echo -e "${YELLOW}Force stopping VM...${NC}"
        VBoxManage controlvm "$VM_NAME" poweroff
    else
        echo -e "${CYAN}Sending shutdown signal to VM...${NC}"
        VBoxManage controlvm "$VM_NAME" acpipowerbutton
        echo "Waiting for VM to shutdown (this may take 30-60 seconds)..."
        
        # Wait up to 60 seconds for shutdown
        for i in {1..60}; do
            sleep 1
            if ! is_vm_running; then
                echo -e "${GREEN}✓ VM stopped successfully${NC}"
                return 0
            fi
        done
        
        echo -e "${YELLOW}VM did not shutdown within 60 seconds${NC}"
        echo "Use '$0 stop --force' to force power off"
        return 1
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ VM stopped${NC}"
    else
        echo -e "${RED}✗ Failed to stop VM${NC}"
        return 1
    fi
}

cmd_restart() {
    echo -e "${CYAN}Restarting VM...${NC}"
    cmd_stop "$@"
    sleep 2
    cmd_start "$@"
}

cmd_status() {
    check_vm_exists
    
    state=$(get_vm_state)
    
    echo "VM Status: $VM_NAME"
    echo "========================"
    
    case "$state" in
        running)
            echo -e "State: ${GREEN}Running${NC}"
            
            # Get more details
            echo ""
            echo "Connection Info:"
            echo "  SSH: ssh -p 2222 builduser@localhost"
            echo "  RDP: xfreerdp /v:localhost:3389 /u:builduser"
            
            # Check if SSH is responding
            echo ""
            echo -n "SSH Status: "
            if timeout 2 ssh -p 2222 -o BatchMode=yes -o ConnectTimeout=2 builduser@localhost "exit" 2>/dev/null; then
                echo -e "${GREEN}Accessible${NC}"
            else
                echo -e "${YELLOW}Not responding (VM may still be booting)${NC}"
            fi
            ;;
        saved)
            echo -e "State: ${YELLOW}Saved${NC}"
            echo "Use '$0 start' to resume"
            ;;
        poweroff)
            echo -e "State: ${RED}Powered Off${NC}"
            echo "Use '$0 start' to start"
            ;;
        *)
            echo "State: $state"
            ;;
    esac
    
    # Show resource allocation
    echo ""
    echo "Resources:"
    VBoxManage showvminfo "$VM_NAME" --machinereadable | grep -E "(memory|cpus|vram)=" | while read line; do
        key=$(echo $line | cut -d'=' -f1)
        value=$(echo $line | cut -d'=' -f2 | tr -d '"')
        
        case "$key" in
            memory) echo "  RAM: $value MB" ;;
            cpus) echo "  CPUs: $value" ;;
            vram) echo "  Video RAM: $value MB" ;;
        esac
    done
}

cmd_ssh() {
    check_vm_exists
    
    if ! is_vm_running; then
        echo -e "${RED}ERROR: VM is not running${NC}"
        echo "Start it with: $0 start"
        exit 1
    fi
    
    echo -e "${CYAN}Connecting via SSH...${NC}"
    ssh -p 2222 builduser@localhost "$@"
}

cmd_rdp() {
    check_vm_exists
    
    if ! is_vm_running; then
        echo -e "${RED}ERROR: VM is not running${NC}"
        echo "Start it with: $0 start"
        exit 1
    fi
    
    echo -e "${CYAN}Connecting via RDP...${NC}"
    
    # Try freerdp first
    if command -v xfreerdp &> /dev/null; then
        xfreerdp /v:localhost:3389 /u:builduser /w:1280 /h:720
    elif command -v remmina &> /dev/null; then
        remmina -c rdp://builduser@localhost:3389
    else
        echo -e "${RED}ERROR: No RDP client found${NC}"
        echo "Install one:"
        echo "  sudo apt install freerdp2-x11"
        echo "  or"
        echo "  sudo apt install remmina"
        exit 1
    fi
}

cmd_snapshot() {
    check_vm_exists
    
    if [ -z "$1" ]; then
        echo -e "${RED}ERROR: Snapshot name required${NC}"
        echo "Usage: $0 snapshot <name>"
        exit 1
    fi
    
    snapshot_name="$1"
    description="${2:-Snapshot created on $(date)}"
    
    echo -e "${CYAN}Creating snapshot '$snapshot_name'...${NC}"
    
    # Snapshots can be taken while running
    VBoxManage snapshot "$VM_NAME" take "$snapshot_name" --description "$description"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Snapshot created successfully${NC}"
    else
        echo -e "${RED}✗ Failed to create snapshot${NC}"
        return 1
    fi
}

cmd_restore() {
    check_vm_exists
    
    if [ -z "$1" ]; then
        echo -e "${RED}ERROR: Snapshot name required${NC}"
        echo "Usage: $0 restore <name>"
        echo ""
        echo "Available snapshots:"
        cmd_list_snapshots
        exit 1
    fi
    
    snapshot_name="$1"
    
    echo -e "${YELLOW}WARNING: This will revert VM to snapshot '$snapshot_name'${NC}"
    echo "All changes since the snapshot will be lost."
    read -p "Continue? (y/N) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi
    
    # Stop VM if running
    if is_vm_running; then
        echo "Stopping VM first..."
        cmd_stop --force
        sleep 2
    fi
    
    echo -e "${CYAN}Restoring snapshot '$snapshot_name'...${NC}"
    VBoxManage snapshot "$VM_NAME" restore "$snapshot_name"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Snapshot restored successfully${NC}"
        echo "Start VM with: $0 start"
    else
        echo -e "${RED}✗ Failed to restore snapshot${NC}"
        return 1
    fi
}

cmd_list_snapshots() {
    check_vm_exists
    
    echo "Snapshots for '$VM_NAME':"
    echo "========================"
    
    VBoxManage snapshot "$VM_NAME" list --machinereadable 2>/dev/null | \
        grep -E "(SnapshotName|SnapshotDescription)" | \
        sed 's/SnapshotName[^=]*=//; s/SnapshotDescription[^=]*=/ - /; s/"//g' | \
        paste -d " " - - | \
        nl -w3 -s'. '
    
    if [ ${PIPESTATUS[0]} -ne 0 ]; then
        echo "No snapshots found"
    fi
}

cmd_info() {
    check_vm_exists
    
    echo "VM Information: $VM_NAME"
    echo "=============================="
    echo ""
    
    VBoxManage showvminfo "$VM_NAME" | grep -E "(Name:|Guest OS:|Memory size:|Number of CPUs:|VRAM size:|State:|NIC)"
}

# Main script
case "$1" in
    start)
        shift
        cmd_start "$@"
        ;;
    stop)
        shift
        cmd_stop "$@"
        ;;
    restart)
        shift
        cmd_restart "$@"
        ;;
    status)
        cmd_status
        ;;
    ssh)
        shift
        cmd_ssh "$@"
        ;;
    rdp)
        cmd_rdp
        ;;
    snapshot)
        shift
        cmd_snapshot "$@"
        ;;
    restore)
        shift
        cmd_restore "$@"
        ;;
    list-snapshots)
        cmd_list_snapshots
        ;;
    info)
        cmd_info
        ;;
    help|--help|-h)
        show_help
        ;;
    "")
        echo -e "${RED}ERROR: No command specified${NC}"
        echo ""
        show_help
        exit 1
        ;;
    *)
        echo -e "${RED}ERROR: Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

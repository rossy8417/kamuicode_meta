#!/usr/bin/env python3
"""
Update settings.local.json with all MCP permissions
"""
import json
import sys

def load_mcp_permissions():
    """Load generated MCP permissions"""
    with open('generated/mcp-all-permissions.json', 'r') as f:
        data = json.load(f)
    return data['mcp_permissions']

def update_settings():
    """Update settings.local.json with all MCP permissions"""
    settings_file = '.claude/settings.local.json'
    
    # Load existing settings
    with open(settings_file, 'r') as f:
        settings = json.load(f)
    
    # Get existing permissions
    existing_permissions = settings.get('permissions', {}).get('allow', [])
    
    # Filter out existing MCP permissions to avoid duplicates
    non_mcp_permissions = [p for p in existing_permissions if not p.startswith('mcp__')]
    
    # Load all MCP permissions
    mcp_permissions = load_mcp_permissions()
    
    # Combine permissions
    all_permissions = non_mcp_permissions + mcp_permissions
    
    # Update settings
    settings['permissions']['allow'] = all_permissions
    
    # Save updated settings
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"Updated {settings_file} with {len(mcp_permissions)} MCP permissions")
    print(f"Total permissions: {len(all_permissions)}")
    
    # Also create a clean version with only MCP permissions
    mcp_only_settings = {
        "permissions": {
            "allow": mcp_permissions,
            "deny": []
        }
    }
    
    mcp_only_file = '.claude/settings.mcp-only.json'
    with open(mcp_only_file, 'w') as f:
        json.dump(mcp_only_settings, f, indent=2)
    
    print(f"\nAlso created {mcp_only_file} with only MCP permissions")

if __name__ == "__main__":
    try:
        update_settings()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
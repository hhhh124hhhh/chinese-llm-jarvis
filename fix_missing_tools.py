#!/usr/bin/env python3
"""
Script to fix missing base tools in Letta database.
This script ensures all base tools are properly registered in the database.
"""

from letta.server.server import SyncServer
from letta.config import LettaConfig
from letta.constants import BASE_TOOLS, BASE_MEMORY_TOOLS, BASE_SLEEPTIME_TOOLS

def fix_missing_tools():
    """Fix missing base tools by upserting them into the database."""
    print("Loading Letta configuration...")
    config = LettaConfig.load()
    
    print("Initializing Letta server...")
    server = SyncServer()
    
    print("Getting default user...")
    user = server.user_manager.get_user_or_default()
    
    print("Upserting base tools...")
    tools = server.tool_manager.upsert_base_tools(actor=user)
    
    print(f"Successfully upserted {len(tools)} tools:")
    for tool in tools:
        print(f"  - {tool.name} ({tool.tool_type})")
    
    # Verify that the required tools are present
    required_tools = {"memory_replace", "conversation_search", "memory_insert", "send_message"}
    existing_tools = {tool.name for tool in tools}
    missing_tools = required_tools - existing_tools
    
    if missing_tools:
        print(f"\nWARNING: Still missing tools: {missing_tools}")
        return False
    else:
        print("\nAll required tools are present!")
        return True

if __name__ == "__main__":
    try:
        success = fix_missing_tools()
        if success:
            print("\nSUCCESS: Base tools fixed!")
        else:
            print("\nFAILURE: Some tools are still missing.")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
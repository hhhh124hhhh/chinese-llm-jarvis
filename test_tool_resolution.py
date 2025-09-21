#!/usr/bin/env python3
"""
Test script to verify tool resolution logic.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from letta.server.server import SyncServer
from letta.config import LettaConfig

def test_tool_resolution():
    """Test tool resolution logic."""
    print("Loading Letta configuration...")
    config = LettaConfig.load()
    
    print("Initializing Letta server...")
    server = SyncServer()
    
    print("Getting default user...")
    user = server.user_manager.get_user_or_default()
    print(f"User ID: {user.id}")
    print(f"Organization ID: {user.organization_id}")
    
    # Test resolving specific tools
    required_tools = ["memory_replace", "conversation_search", "memory_insert", "send_message"]
    
    print("\nTesting tool resolution...")
    async def test_async():
        from letta.services.agent_manager import AgentManager
        from sqlalchemy import create_engine
        from letta.server.db import db_registry
        
        # Initialize database registry
        db_registry.init_db_engine()
        
        agent_manager = AgentManager()
        
        # Test resolving tools
        tool_names = set(required_tools)
        supplied_ids = set()
        
        try:
            # This mimics the logic in create_agent_async
            from sqlalchemy.orm import sessionmaker
            from letta.orm.tool import Tool as ToolModel
            
            async with db_registry.async_session() as session:
                name_to_id, id_to_name, requires_approval = await agent_manager._resolve_tools_async(
                    session,
                    tool_names,
                    supplied_ids,
                    user.organization_id,
                )
                
                print(f"Resolved tools:")
                print(f"  name_to_id: {name_to_id}")
                print(f"  id_to_name: {id_to_name}")
                print(f"  requires_approval: {requires_approval}")
                
                return True, name_to_id, id_to_name
        except Exception as e:
            print(f"Error resolving tools: {e}")
            import traceback
            traceback.print_exc()
            return False, None, None
    
    # Run the async test
    import asyncio
    success, name_to_id, id_to_name = asyncio.run(test_async())
    
    if success:
        print("\nSUCCESS: Tool resolution works correctly!")
        return True
    else:
        print("\nFAILURE: Tool resolution failed!")
        return False

if __name__ == "__main__":
    try:
        success = test_tool_resolution()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
#!/usr/bin/env python3
"""
Script to test agent creation with base tools.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from letta.server.server import SyncServer
from letta.config import LettaConfig
from letta.schemas.agent import CreateAgent

def test_agent_creation():
    """Test agent creation with base tools."""
    print("Loading Letta configuration...")
    config = LettaConfig.load()
    
    print("Initializing Letta server...")
    server = SyncServer()
    
    print("Getting default user...")
    user = server.user_manager.get_user_or_default()
    print(f"User ID: {user.id}")
    print(f"Organization ID: {user.organization_id}")
    
    # Create an agent with base tools
    print("\nCreating agent with base tools...")
    try:
        agent_state = server.create_agent(
            request=CreateAgent(
                name="test_agent_fix",
                include_base_tools=True,  # This should include the required tools
                model="gpt-4o-mini",
                embedding="text-embedding-3-small",
            ),
            actor=user,
        )
        print(f"SUCCESS: Agent created with ID {agent_state.id}")
        print(f"Agent tools: {[t.name for t in agent_state.tools]}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_agent_creation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
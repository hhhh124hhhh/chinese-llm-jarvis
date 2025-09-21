import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from letta.server.server import SyncServer
from letta.constants import DEFAULT_ORG_ID, DEFAULT_ORG_NAME

async def verify_fix():
    """Verify that our fix for the default organization and user creation works correctly."""
    print("Verifying the fix for default organization and user creation...")
    
    # Create a server instance
    server = SyncServer()
    
    # Test 1: Create default organization
    print("Test 1: Creating default organization...")
    try:
        default_org = await server.organization_manager.create_default_organization_async()
        print(f"✓ Default organization created: {default_org.id} - {default_org.name}")
        
        # Verify the organization ID matches the expected default
        assert default_org.id == DEFAULT_ORG_ID, f"Expected {DEFAULT_ORG_ID}, got {default_org.id}"
        assert default_org.name == DEFAULT_ORG_NAME, f"Expected {DEFAULT_ORG_NAME}, got {default_org.name}"
        print("✓ Organization ID and name verified correctly")
    except Exception as e:
        print(f"✗ Failed to create default organization: {e}")
        return False
    
    # Test 2: Create default user
    print("Test 2: Creating default user...")
    try:
        default_user = await server.user_manager.create_default_actor_async(org_id=default_org.id)
        print(f"✓ Default user created: {default_user.id} - {default_user.name}")
        
        # Verify the user is associated with the correct organization
        assert default_user.organization_id == default_org.id, f"Expected {default_org.id}, got {default_user.organization_id}"
        print("✓ User organization association verified correctly")
    except Exception as e:
        print(f"✗ Failed to create default user: {e}")
        return False
    
    # Test 3: Try to get the default user (should not create a new one)
    print("Test 3: Getting default user (should not create a new one)...")
    try:
        existing_user = await server.user_manager.get_default_actor_async()
        print(f"✓ Default user retrieved: {existing_user.id} - {existing_user.name}")
        
        # Verify it's the same user
        assert existing_user.id == default_user.id, f"Expected {default_user.id}, got {existing_user.id}"
        print("✓ Retrieved the same default user")
    except Exception as e:
        print(f"✗ Failed to get default user: {e}")
        return False
    
    print("\n🎉 All tests passed! The fix is working correctly.")
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(verify_fix())
        if success:
            print("\n✅ Verification successful - the fix resolves the original error.")
        else:
            print("\n❌ Verification failed - there may be issues with the fix.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during verification: {e}")
        sys.exit(1)
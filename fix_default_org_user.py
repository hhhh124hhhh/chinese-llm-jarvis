import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from letta.server.server import SyncServer
from letta.constants import DEFAULT_ORG_ID, DEFAULT_ORG_NAME
from letta.orm.errors import NoResultFound

async def fix_default_org_user():
    """Fix the default organization and user creation issue."""
    print("Fixing the default organization and user creation issue...")
    
    # Create a server instance
    server = SyncServer()
    
    # Try to get or create the default organization
    print("Checking for default organization...")
    try:
        default_org = await server.organization_manager.get_default_organization_async()
        print(f"✓ Default organization already exists: {default_org.id} - {default_org.name}")
    except NoResultFound:
        print("Default organization not found. Creating it...")
        try:
            default_org = await server.organization_manager.create_default_organization_async()
            print(f"✓ Default organization created: {default_org.id} - {default_org.name}")
        except Exception as e:
            print(f"✗ Failed to create default organization: {e}")
            return False
    except Exception as e:
        print(f"✗ Error checking for default organization: {e}")
        return False
    
    # Verify the organization ID matches the expected default
    if default_org.id != DEFAULT_ORG_ID:
        print(f"⚠ Warning: Organization ID mismatch. Expected {DEFAULT_ORG_ID}, got {default_org.id}")
    
    if default_org.name != DEFAULT_ORG_NAME:
        print(f"⚠ Warning: Organization name mismatch. Expected {DEFAULT_ORG_NAME}, got {default_org.name}")
    
    # Try to get or create the default user
    print("Checking for default user...")
    try:
        default_user = await server.user_manager.get_default_actor_async()
        print(f"✓ Default user already exists: {default_user.id} - {default_user.name}")
    except NoResultFound:
        print("Default user not found. Creating it...")
        try:
            default_user = await server.user_manager.create_default_actor_async(org_id=default_org.id)
            print(f"✓ Default user created: {default_user.id} - {default_user.name}")
        except Exception as e:
            print(f"✗ Failed to create default user: {e}")
            return False
    except Exception as e:
        print(f"✗ Error checking for default user: {e}")
        return False
    
    # Verify the user is associated with the correct organization
    if default_user.organization_id != default_org.id:
        print(f"⚠ Warning: User organization mismatch. Expected {default_org.id}, got {default_user.organization_id}")
    
    print("\n🎉 Fix applied successfully! The default organization and user should now exist.")
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(fix_default_org_user())
        if success:
            print("\n✅ Fix successful - the default organization and user issue should be resolved.")
        else:
            print("\n❌ Fix failed - there may be issues with the database or configuration.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during fix: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
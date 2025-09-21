import asyncio
from letta.server.server import SyncServer
from letta.constants import DEFAULT_ORG_ID, DEFAULT_ORG_NAME

async def test_default_org_user_creation():
    # Create a server instance
    server = SyncServer()
    
    # Create default organization
    print("Creating default organization...")
    default_org = await server.organization_manager.create_default_organization_async()
    print(f"Default organization created: {default_org.id} - {default_org.name}")
    
    # Verify the organization ID matches the expected default
    assert default_org.id == DEFAULT_ORG_ID
    assert default_org.name == DEFAULT_ORG_NAME
    print("Organization ID and name verified correctly")
    
    # Create default user
    print("Creating default user...")
    default_user = await server.user_manager.create_default_actor_async(org_id=default_org.id)
    print(f"Default user created: {default_user.id} - {default_user.name}")
    
    # Verify the user is associated with the correct organization
    assert default_user.organization_id == default_org.id
    print("User organization association verified correctly")
    
    print("Test passed!")

if __name__ == "__main__":
    asyncio.run(test_default_org_user_creation())
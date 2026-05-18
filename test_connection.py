"""
Test script to verify watsonx.orchestrate connection
"""
import sys
from pathlib import Path
from loguru import logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.base_agent import BaseAgent


def test_connection():
    """Test connection to watsonx.orchestrate"""
    
    logger.info("=" * 60)
    logger.info("Testing watsonx.orchestrate Connection")
    logger.info("=" * 60)
    
    try:
        # Create a test agent
        agent = BaseAgent(
            name="TestAgent",
            description="Test agent for verifying watsonx.orchestrate connection"
        )
        
        # Test credential loading
        logger.info("\n1. Loading credentials...")
        credentials = agent.load_credentials()
        logger.success(f"✓ Credentials loaded successfully")
        logger.info(f"  - URL: {credentials.get('url')}")
        logger.info(f"  - Region: {credentials.get('region')}")
        logger.info(f"  - Instance ID: {credentials.get('instance_id')}")
        
        # Test connection
        logger.info("\n2. Connecting to watsonx.orchestrate...")
        agent.connect()
        logger.success("✓ Connection established successfully")
        
        # Test agent creation
        logger.info("\n3. Creating test agent...")
        agent.create_agent()
        logger.success("✓ Agent created successfully")
        
        # Disconnect
        logger.info("\n4. Disconnecting...")
        agent.disconnect()
        logger.success("✓ Disconnected successfully")
        
        logger.info("\n" + "=" * 60)
        logger.success("ALL TESTS PASSED! ✓")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error("\n" + "=" * 60)
        logger.error(f"TEST FAILED: {e}")
        logger.error("=" * 60)
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

# Made with Bob

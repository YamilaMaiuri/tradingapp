"""
Deploy agent to watsonx.orchestrate instance
This script will actually create the agent in your watsonx.orchestrate instance
"""
import sys
import json
from pathlib import Path
from loguru import logger
from ibm_watsonx_orchestrate.agent_builder.agents import AssistantAgent, AssistantAgentSpec
from ibm_watsonx_orchestrate_clients import AIServiceClient


def load_credentials():
    """Load credentials from config file"""
    config_path = Path(__file__).parent / "config" / "credentials.json"
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config.get('watsonx_orchestrate', {})


def deploy_trading_agent():
    """Deploy the trading agent to watsonx.orchestrate"""
    
    logger.info("=" * 70)
    logger.info("DEPLOYING TRADING AGENT TO WATSONX.ORCHESTRATE")
    logger.info("=" * 70)
    
    try:
        # Load credentials
        logger.info("\n1. Loading credentials...")
        credentials = load_credentials()
        logger.success(f"✓ Credentials loaded")
        logger.info(f"   URL: {credentials['url']}")
        logger.info(f"   Instance ID: {credentials['instance_id']}")
        
        # Create AI Service Client
        logger.info("\n2. Creating AI Service Client...")
        client = AIServiceClient(
            api_key=credentials['api_key'],
            url=credentials['url']
        )
        logger.success("✓ Client created")
        
        # Create Agent Specification
        logger.info("\n3. Creating agent specification...")
        agent_spec = AssistantAgentSpec(
            name="TradingAnalystAgent",
            description="AI agent specialized in analyzing market trends and providing trading insights for ICBC demo",
            instructions="""You are a professional trading analyst AI agent. Your role is to:
            
1. Analyze market trends and conditions
2. Provide trading recommendations (BUY, SELL, HOLD)
3. Assess risk levels for different trading opportunities
4. Generate detailed analysis reports
5. Help traders make informed decisions

Always provide clear reasoning for your recommendations and consider:
- Technical indicators
- Market sentiment
- Risk management
- Current market conditions

Be professional, accurate, and helpful in your responses."""
        )
        logger.success("✓ Agent specification created")
        
        # Deploy the agent
        logger.info("\n4. Deploying agent to watsonx.orchestrate...")
        logger.info("   This will create the agent in your instance...")
        
        agent = AssistantAgent(
            spec=agent_spec,
            client=client
        )
        
        # Create/deploy the agent
        logger.info("   Calling create() method...")
        result = agent.create()
        
        logger.success("✓ Agent deployed successfully!")
        logger.info(f"\n   Agent Details:")
        logger.info(f"   - Name: {agent_spec.name}")
        logger.info(f"   - Description: {agent_spec.description}")
        logger.info(f"   - Status: Deployed")
        
        logger.info("\n" + "=" * 70)
        logger.success("DEPLOYMENT COMPLETED! ✓")
        logger.info("=" * 70)
        
        logger.info("\n📍 Next Steps:")
        logger.info("   1. Go to your watsonx.orchestrate UI")
        logger.info(f"   2. Navigate to: {credentials['url']}")
        logger.info("   3. Look for 'TradingAnalystAgent' in your agents list")
        logger.info("   4. You can now interact with the agent through the UI")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Deployment failed: {e}")
        logger.error(f"   Error type: {type(e).__name__}")
        logger.error(f"   Error details: {str(e)}")
        
        logger.info("\n💡 Troubleshooting:")
        logger.info("   - Verify your API key is valid")
        logger.info("   - Check that the instance URL is correct")
        logger.info("   - Ensure you have permissions to create agents")
        logger.info("   - Try logging into the watsonx.orchestrate UI first")
        
        return False


if __name__ == "__main__":
    success = deploy_trading_agent()
    sys.exit(0 if success else 1)

# Made with Bob

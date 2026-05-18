"""
Demo script to test a trading agent with watsonx.orchestrate
"""
import sys
from pathlib import Path
from loguru import logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.base_agent import BaseAgent


class TradingAgent(BaseAgent):
    """Simple trading agent for demo purposes"""
    
    def __init__(self):
        super().__init__(
            name="TradingAnalystAgent",
            description="AI agent specialized in analyzing market trends and providing trading insights"
        )
    
    def analyze_market(self, symbol: str) -> dict:
        """Analyze market for a given symbol"""
        logger.info(f"Analyzing market for symbol: {symbol}")
        
        # Simulate market analysis
        analysis = {
            "symbol": symbol,
            "recommendation": "BUY",
            "confidence": 0.85,
            "reasoning": f"Technical indicators show strong upward momentum for {symbol}",
            "risk_level": "Medium",
            "target_price": "Based on current trends and support levels"
        }
        
        return analysis
    
    def generate_report(self, analysis: dict) -> str:
        """Generate a formatted report from analysis"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           TRADING ANALYSIS REPORT                            ║
╠══════════════════════════════════════════════════════════════╣
║ Symbol:         {analysis['symbol']:<45} ║
║ Recommendation: {analysis['recommendation']:<45} ║
║ Confidence:     {analysis['confidence']:<45} ║
║ Risk Level:     {analysis['risk_level']:<45} ║
╠══════════════════════════════════════════════════════════════╣
║ Reasoning:                                                   ║
║ {analysis['reasoning']:<60} ║
╠══════════════════════════════════════════════════════════════╣
║ Target Price:                                                ║
║ {analysis['target_price']:<60} ║
╚══════════════════════════════════════════════════════════════╝
        """
        return report


def main():
    """Main demo function"""
    
    logger.info("=" * 70)
    logger.info("TRADING AGENT DEMO - ICBC")
    logger.info("=" * 70)
    
    try:
        # Create trading agent
        logger.info("\n1. Initializing Trading Agent...")
        agent = TradingAgent()
        logger.success("✓ Agent initialized")
        
        # Connect to watsonx.orchestrate
        logger.info("\n2. Connecting to watsonx.orchestrate...")
        agent.connect()
        logger.success("✓ Connected successfully")
        
        # Create agent
        logger.info("\n3. Creating agent in watsonx.orchestrate...")
        agent.create_agent()
        logger.success("✓ Agent created")
        
        # Perform market analysis
        logger.info("\n4. Performing market analysis...")
        symbols = ["AAPL", "GOOGL", "MSFT"]
        
        for symbol in symbols:
            logger.info(f"\n   Analyzing {symbol}...")
            analysis = agent.analyze_market(symbol)
            report = agent.generate_report(analysis)
            print(report)
        
        # Execute a task with the agent
        logger.info("\n5. Testing agent task execution...")
        task = "Analyze current market conditions and provide trading recommendations"
        result = agent.execute(task)
        
        logger.info("\n   Task Result:")
        for key, value in result.items():
            logger.info(f"   - {key}: {value}")
        
        # Disconnect
        logger.info("\n6. Disconnecting...")
        agent.disconnect()
        logger.success("✓ Disconnected")
        
        logger.info("\n" + "=" * 70)
        logger.success("DEMO COMPLETED SUCCESSFULLY! ✓")
        logger.info("=" * 70)
        
        logger.info("\n📊 Summary:")
        logger.info(f"   - Agent Name: {agent.name}")
        logger.info(f"   - Symbols Analyzed: {', '.join(symbols)}")
        logger.info(f"   - Status: Ready for deployment")
        logger.info("\n💡 Next Steps:")
        logger.info("   - Deploy agent to watsonx.orchestrate platform")
        logger.info("   - Integrate with real market data APIs")
        logger.info("   - Add more sophisticated trading strategies")
        
    except Exception as e:
        logger.error(f"\n❌ Demo failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Made with Bob

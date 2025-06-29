#!/usr/bin/env python3
"""
Enhanced SaaS Discovery Launcher
Run comprehensive SaaS opportunity discovery with advanced capabilities
"""

import asyncio
import sys
from pathlib import Path

# Add the agents directory to the path
sys.path.append(str(Path(__file__).parent / "luciq" / "src" / "agents"))

from enhanced_discovery_orchestrator import EnhancedDiscoveryOrchestrator

def main():
    """Main launcher function"""
    print("🚀 Luciq Enhanced Discovery System")
    print("=" * 50)
    print("🎯 Advanced SaaS opportunity discovery with:")
    print("   • AI-powered pain point analysis")
    print("   • Market validation & competitive intelligence")
    print("   • Trend analysis & future predictions")
    print("   • Comprehensive investment recommendations")
    print("=" * 50)
    
    # Run the enhanced discovery
    orchestrator = EnhancedDiscoveryOrchestrator()
    
    try:
        # Run async discovery
        report = asyncio.run(orchestrator.run_comprehensive_discovery())
        
        if report:
            print("\n🎉 SUCCESS! Enhanced discovery completed successfully!")
            print("\n📋 Generated Reports:")
            print("   • comprehensive-discovery-report.json - Complete analysis")
            print("   • enhanced-opportunities.json - AI-enhanced opportunities")
            print("   • trend-analysis-results.json - Market trend insights")
            print("\n🚀 Ready to build the next big SaaS!")
        else:
            print("\n❌ Discovery failed. Check the logs above for details.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Discovery interrupted by user")
    except Exception as e:
        print(f"\n❌ Discovery failed with error: {e}")

if __name__ == "__main__":
    main() 
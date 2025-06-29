#!/usr/bin/env python3
"""
Mega Opportunity Scanner for Luciq
Runs 20 discovery cycles with maximum diversity across subreddits and time periods
"""

import time
import subprocess
import sys
from datetime import datetime

def run_discovery_cycle():
    """Run a single discovery cycle"""
    try:
        result = subprocess.run([
            sys.executable, 
            "luciq/src/agents/pain_point_scraper_agent.py"
        ], capture_output=True, text=True, timeout=90)
        
        if result.returncode == 0:
            return True, "Success"
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def run_opportunity_ranking():
    """Run opportunity ranking"""
    try:
        result = subprocess.run([
            sys.executable,
            "luciq/src/agents/opportunity_ranker_fixed.py"
        ], capture_output=True, text=True, timeout=90)
        
        return result.returncode == 0
    except:
        return False

def run_concept_generation():
    """Run concept generation"""
    try:
        result = subprocess.run([
            sys.executable,
            "luciq/src/agents/concept_generator.py"
        ], capture_output=True, text=True, timeout=90)
        
        return result.returncode == 0
    except:
        return False

def mega_scan(num_cycles=20, delay_between_cycles=2):
    """Run mega opportunity scanning with maximum diversity"""
    print("🚀 LUCIQ MEGA OPPORTUNITY SCANNER")
    print("=" * 70)
    print(f"Starting {num_cycles} discovery cycles with {delay_between_cycles}s delays")
    print(f"Focus: Maximum diversity across subreddits and historical periods")
    print(f"Target: Deep historical analysis (2+ years) and fresh content")
    print()
    
    start_time = datetime.now()
    successful_cycles = 0
    failed_cycles = 0
    
    for cycle in range(1, num_cycles + 1):
        print(f"🔄 MEGA CYCLE {cycle}/{num_cycles}")
        print("-" * 35)
        
        cycle_start = datetime.now()
        
        # Step 1: Pain Point Discovery
        print(">> Running pain point discovery...")
        success, message = run_discovery_cycle()
        
        if success:
            print("   ✅ Pain points discovered")
            
            # Step 2: Opportunity Ranking
            print(">> Running opportunity ranking...")
            if run_opportunity_ranking():
                print("   ✅ Opportunities ranked")
                
                # Step 3: Concept Generation
                print(">> Running concept generation...")
                if run_concept_generation():
                    print("   ✅ Concepts generated")
                    successful_cycles += 1
                else:
                    print("   ❌ Concept generation failed")
                    failed_cycles += 1
            else:
                print("   ❌ Opportunity ranking failed")
                failed_cycles += 1
        else:
            print(f"   ❌ Pain point discovery failed: {message}")
            failed_cycles += 1
        
        cycle_duration = datetime.now() - cycle_start
        print(f"   Duration: {cycle_duration.total_seconds():.1f}s")
        
        # Show progress
        progress = (cycle / num_cycles) * 100
        print(f"   Progress: {progress:.1f}% complete")
        print()
        
        # Delay between cycles (except last one)
        if cycle < num_cycles:
            print(f"⏳ Waiting {delay_between_cycles}s before next cycle...")
            time.sleep(delay_between_cycles)
            print()
    
    # Final summary
    total_duration = datetime.now() - start_time
    success_rate = (successful_cycles / num_cycles) * 100
    
    print("🎯 MEGA SCAN COMPLETE!")
    print("=" * 50)
    print(f"Total Duration: {total_duration.total_seconds()/60:.1f} minutes")
    print(f"Successful Cycles: {successful_cycles}/{num_cycles} ({success_rate:.1f}%)")
    print(f"Failed Cycles: {failed_cycles}")
    print()
    
    if successful_cycles > 0:
        print("📊 ANALYSIS READY:")
        print("- Run 'python historical_insights_report.py' for comprehensive analysis")
        print("- Check 'python system_status_report.py' for system overview")
        print("- Review concepts in luciq/memory/saas-concepts.json")
        print()
        print("🔍 EXPECTED RESULTS:")
        print(f"- {successful_cycles * 8} new pain points analyzed")
        print(f"- {successful_cycles * 3} new opportunities ranked")
        print(f"- Enhanced historical trend data")
        print(f"- Cross-community validation patterns")
    
    return successful_cycles > 0

if __name__ == "__main__":
    # Run mega scan with 20 cycles
    mega_scan(num_cycles=20, delay_between_cycles=2) 
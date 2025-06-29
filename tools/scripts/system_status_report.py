#!/usr/bin/env python3
"""
Luciq System Status Report
Shows complete system state after rehydration and orchestrator activation
"""

import json
from pathlib import Path
from datetime import datetime

def generate_system_status_report():
    """Generate comprehensive system status report"""
    print("🎯 LUCIQ SYSTEM STATUS REPORT")
    print("=" * 60)
    print()
    
    # Check agent configurations
    print("📁 AGENT CONFIGURATIONS:")
    cursor_mdc = Path('.cursor/mdc')
    if cursor_mdc.exists():
        agents = list(cursor_mdc.glob('*.mdc'))
        print(f"   ✅ {len(agents)} agents configured in .cursor/mdc/")
        for agent in sorted(agents):
            print(f"      • {agent.name}")
    
    luciq_agents = Path('luciq/agents')
    if luciq_agents.exists():
        saas_agents = list(luciq_agents.glob('*.mdc'))
        print(f"   ✅ {len(saas_agents)} Luciq-specific agents")
        for agent in sorted(saas_agents):
            print(f"      • {agent.name}")
    print()
    
    # Check memory system
    print("🧠 MEMORY SYSTEM:")
    
    # Base memory
    memory_dir = Path('memory')
    if memory_dir.exists():
        memory_files = list(memory_dir.glob('*'))
        print(f"   ✅ Base memory: {len(memory_files)} files")
        for mem_file in sorted(memory_files):
            if mem_file.is_file():
                print(f"      • {mem_file.name}")
    
    # Luciq memory
    luciq_memory = Path('luciq/memory')
    if luciq_memory.exists():
        saas_memory_files = list(luciq_memory.glob('*'))
        print(f"   ✅ Luciq memory: {len(saas_memory_files)} files")
        for mem_file in sorted(saas_memory_files):
            if mem_file.is_file():
                print(f"      • {mem_file.name}")
    
    # Working memory
    working_memory = Path('working-memory')
    if working_memory.exists():
        working_files = list(working_memory.glob('*'))
        print(f"   ✅ Working memory: {len(working_files)} files")
        for work_file in sorted(working_files):
            if work_file.is_file():
                print(f"      • {work_file.name}")
    print()
    
    # Check discovery pipeline status
    print("🔍 DISCOVERY PIPELINE STATUS:")
    
    # Pain points
    pain_points_file = luciq_memory / "pain-points-database.json"
    if pain_points_file.exists():
        with open(pain_points_file, 'r') as f:
            pain_data = json.load(f)
            total_posts = pain_data.get('total_posts_scraped', 0)
            pain_points = pain_data.get('pain_points_found', 0)
            print(f"   ✅ Pain Point Discovery: {total_posts} posts scraped, {pain_points} pain points found")
    
    # Opportunities
    opportunities_file = luciq_memory / "ranked-opportunities.json"
    if opportunities_file.exists():
        with open(opportunities_file, 'r') as f:
            opp_data = json.load(f)
            total_ops = opp_data.get('total_opportunities', 0)
            high_value = opp_data.get('high_value_count', 0)
            medium_value = opp_data.get('medium_value_count', 0)
            avg_score = opp_data.get('average_score', 0)
            print(f"   ✅ Opportunity Ranking: {total_ops} opportunities (avg: {avg_score:.1f}/10)")
            print(f"      • High value (≥7.0): {high_value}")
            print(f"      • Medium value (5.0-6.9): {medium_value}")
    
    # Concepts
    concepts_file = luciq_memory / "saas-concepts.json"
    if concepts_file.exists():
        with open(concepts_file, 'r') as f:
            concept_data = json.load(f)
            total_concepts = concept_data.get('total_concepts', 0)
            concepts = concept_data.get('concepts', [])
            print(f"   ✅ Concept Generation: {total_concepts} SaaS concepts generated")
            for i, concept in enumerate(concepts, 1):
                saas_concept = concept['saas_concept']
                score = concept['source_opportunity']['score']
                print(f"      {i}. {saas_concept['name']} (score: {score}/10)")
    print()
    
    # Check agent activity
    print("📊 AGENT ACTIVITY:")
    agent_log = luciq_memory / "agent-log.jsonl"
    if agent_log.exists():
        with open(agent_log, 'r') as f:
            log_lines = f.readlines()
            print(f"   ✅ {len(log_lines)} agent events logged")
            
            # Show recent events
            recent_events = []
            for line in log_lines[-5:]:  # Last 5 events
                try:
                    event = json.loads(line.strip())
                    recent_events.append(event)
                except:
                    continue
            
            print("   📝 Recent events:")
            for event in recent_events:
                agent = event.get('agent', 'unknown')
                action = event.get('event', 'unknown')
                status = event.get('status', 'unknown')
                print(f"      • {agent}: {action} ({status})")
    print()
    
    # System readiness
    print("🚀 SYSTEM READINESS:")
    
    # Check if all components are operational
    components_ready = 0
    total_components = 4
    
    if pain_points_file.exists():
        print("   ✅ Pain Point Scraper: OPERATIONAL")
        components_ready += 1
    else:
        print("   ❌ Pain Point Scraper: NOT READY")
    
    if opportunities_file.exists():
        print("   ✅ Opportunity Ranker: OPERATIONAL")
        components_ready += 1
    else:
        print("   ❌ Opportunity Ranker: NOT READY")
    
    if concepts_file.exists():
        print("   ✅ Concept Generator: OPERATIONAL")
        components_ready += 1
    else:
        print("   ❌ Concept Generator: NOT READY")
    
    if cursor_mdc.exists() and len(list(cursor_mdc.glob('*.mdc'))) >= 7:
        print("   ✅ Orchestrator: OPERATIONAL")
        components_ready += 1
    else:
        print("   ❌ Orchestrator: NOT READY")
    
    print()
    readiness_percentage = (components_ready / total_components) * 100
    print(f"🎯 OVERALL SYSTEM READINESS: {readiness_percentage:.0f}% ({components_ready}/{total_components} components)")
    
    if readiness_percentage == 100:
        print("   🎉 SYSTEM FULLY OPERATIONAL - Ready for autonomous discovery!")
    elif readiness_percentage >= 75:
        print("   ⚡ SYSTEM MOSTLY READY - Minor components need attention")
    else:
        print("   ⚠️  SYSTEM NEEDS ATTENTION - Major components missing")
    
    print()
    print("=" * 60)
    print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    generate_system_status_report() 
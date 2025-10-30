"""
Lead Generator Agent Example
Demonstrates lead generation with batch processing.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agents import LeadGeneratorAgent
from backend.config import get_settings


async def single_lead_search():
    """Example: Single lead generation search."""
    print("\n" + "="*60)
    print("Example 1: Single Lead Generation Search")
    print("="*60)
    
    settings = get_settings()
    agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    
    task = {
        "query": "restaurants",
        "location": "San Francisco, CA",
        "max_results": 10
    }
    
    print(f"\n🔍 Searching for: {task['query']} in {task['location']}")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        print(f"✅ Found {result['count']} leads")
        for i, lead in enumerate(result["leads"][:3], 1):
            print(f"\n  Lead {i}:")
            print(f"    Name: {lead['name']}")
            print(f"    Location: {lead['location']}")
            print(f"    Score: {lead['score']}")
    else:
        print(f"❌ Error: {result.get('error')}")


async def batch_lead_generation():
    """Example: Batch processing multiple queries."""
    print("\n" + "="*60)
    print("Example 2: Batch Lead Generation")
    print("="*60)
    
    settings = get_settings()
    agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    
    queries = [
        "tech startups",
        "marketing agencies",
        "software companies"
    ]
    location = "New York, NY"
    
    print(f"\n🔄 Processing {len(queries)} queries in batch...")
    result = await agent.batch_process(queries, location)
    
    if result["status"] == "success":
        print(f"✅ Total leads generated: {result['total_leads']}")
        print(f"✅ Queries processed: {result['queries_processed']}")
        print(f"\n📊 Breakdown:")
        for query in queries:
            count = len([l for l in result['leads'] if l['query'] == query])
            print(f"  {query}: {count} leads")
    else:
        print(f"❌ Error: {result.get('error')}")


async def search_with_qualification():
    """Example: Search businesses with qualification."""
    print("\n" + "="*60)
    print("Example 3: Search with Lead Qualification")
    print("="*60)
    
    settings = get_settings()
    agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    
    # First search
    leads = await agent.search_businesses(
        query="design agencies",
        location="Los Angeles, CA",
        max_results=5
    )
    
    print(f"✅ Found {len(leads)} potential leads")
    print("\n📋 Lead Details:")
    for lead in leads:
        print(f"\n  • {lead['name']}")
        print(f"    Status: {lead['status']}")
        print(f"    Quality Score: {lead['score']:.2f}")


async def export_leads():
    """Example: Generate and export leads."""
    print("\n" + "="*60)
    print("Example 4: Export Leads to File")
    print("="*60)
    
    settings = get_settings()
    agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    
    # Generate leads
    task = {
        "query": "coffee shops",
        "location": "Seattle, WA",
        "max_results": 20
    }
    
    print(f"📥 Generating leads: {task['query']} in {task['location']}")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        # Simulate export
        output_file = Path(settings.output_dir_leads) / "coffee_shops_seattle.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Exported {result['count']} leads to: {output_file}")
        print(f"📁 File size: {output_file.stat().st_size} bytes")
    else:
        print(f"❌ Error: {result.get('error')}")


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("🤖 Lead Generator Agent - Examples")
    print("="*60)
    
    try:
        await single_lead_search()
        await batch_lead_generation()
        await search_with_qualification()
        await export_leads()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

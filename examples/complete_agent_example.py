"""
Complete Agent Framework Example
Demonstrates all 3 agents working together in an integrated workflow.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agents import (
    LeadGeneratorAgent,
    SocialMediaManagerAgent,
    WordPressBloggerAgent
)
from backend.config import get_settings


async def complete_marketing_workflow():
    """
    Example: Complete marketing workflow using all 3 agents.
    
    Workflow:
    1. Generate leads for a business niche
    2. Create social media campaign about the niche
    3. Write blog articles about the niche
    """
    print("\n" + "="*60)
    print("🚀 Complete Marketing Workflow")
    print("="*60)
    
    settings = get_settings()
    niche = "AI SaaS Companies"
    location = "San Francisco, CA"
    
    # Initialize all agents
    lead_agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    social_agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    blog_agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    print(f"\n📋 Campaign: {niche} in {location}")
    print("="*60)
    
    # Step 1: Generate Leads
    print(f"\n🔍 Step 1/3: Lead Generation")
    print("-" * 60)
    
    lead_result = await lead_agent.execute({
        "query": niche.lower(),
        "location": location,
        "max_results": 10
    })
    
    if lead_result["status"] == "success":
        print(f"✅ Generated {lead_result['count']} leads")
        print(f"   Top lead: {lead_result['leads'][0]['name']}")
    else:
        print(f"❌ Lead generation failed: {lead_result.get('error')}")
        return
    
    # Step 2: Create Social Media Campaign
    print(f"\n📱 Step 2/3: Social Media Campaign")
    print("-" * 60)
    
    campaign_result = await social_agent.create_campaign(
        topic=f"Best {niche} in {location.split(',')[0]}",
        duration_days=5,
        platforms=["twitter", "linkedin"]
    )
    
    if campaign_result["status"] == "success":
        print(f"✅ Created campaign with {campaign_result['total_posts']} posts")
        print(f"   Duration: {campaign_result['duration']} days")
        print(f"   Platforms: {', '.join(campaign_result['platforms'])}")
    else:
        print(f"❌ Campaign creation failed")
        return
    
    # Step 3: Generate Blog Article
    print(f"\n✍️  Step 3/3: Blog Article Generation")
    print("-" * 60)
    
    article_result = await blog_agent.execute({
        "topic": f"Top {niche} in {location.split(',')[0]} - 2025 Guide",
        "word_count": 1500,
        "tone": "professional"
    })
    
    if article_result["status"] == "success":
        print(f"✅ Generated article: {article_result['article']['title']}")
        print(f"   Word count: {article_result['word_count']}")
        print(f"   SEO score: {article_result['seo_score']['overall']}/100")
    else:
        print(f"❌ Article generation failed")
        return
    
    # Summary
    print("\n" + "="*60)
    print("📊 Workflow Summary")
    print("="*60)
    print(f"✅ Leads Generated: {lead_result['count']}")
    print(f"✅ Social Posts Created: {campaign_result['total_posts']}")
    print(f"✅ Blog Articles: 1")
    print(f"\n🎯 Total Marketing Assets: {lead_result['count'] + campaign_result['total_posts'] + 1}")


async def parallel_agent_execution():
    """Example: Execute multiple agents in parallel."""
    print("\n" + "="*60)
    print("⚡ Parallel Agent Execution")
    print("="*60)
    
    settings = get_settings()
    
    # Initialize agents
    lead_agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    social_agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    blog_agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    print("\n🚀 Executing all agents simultaneously...")
    
    # Run all agents in parallel
    results = await asyncio.gather(
        lead_agent.execute({
            "query": "tech startups",
            "location": "Austin, TX",
            "max_results": 5
        }),
        social_agent.execute({
            "type": "post",
            "topic": "Startup Culture",
            "platform": "linkedin"
        }),
        blog_agent.execute({
            "topic": "Startup Success Stories",
            "word_count": 1200
        })
    )
    
    lead_result, social_result, blog_result = results
    
    print("\n✅ All agents completed!")
    print(f"\n📊 Results:")
    print(f"  Leads: {lead_result.get('count', 0)}")
    print(f"  Social Post: {'✓' if social_result.get('status') == 'success' else '✗'}")
    print(f"  Blog Article: {'✓' if blog_result.get('status') == 'success' else '✗'}")


async def agent_collaboration():
    """Example: Agents working together on related tasks."""
    print("\n" + "="*60)
    print("🤝 Agent Collaboration Example")
    print("="*60)
    
    settings = get_settings()
    topic = "Cloud Computing Solutions"
    
    # Initialize agents
    social_agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    blog_agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    print(f"\n📝 Topic: {topic}")
    
    # Step 1: Generate blog article
    print(f"\n1️⃣  Generating blog article...")
    blog_result = await blog_agent.execute({
        "topic": topic,
        "word_count": 1500
    })
    
    if blog_result["status"] != "success":
        print(f"❌ Blog generation failed")
        return
    
    print(f"✅ Article created: {blog_result['article']['title']}")
    
    # Step 2: Create social posts to promote the blog
    print(f"\n2️⃣  Creating social media promotion...")
    
    # Use the blog's keywords for social posts
    keywords = [kw["keyword"] for kw in blog_result["keywords"][:3]]
    
    social_posts = []
    for platform in ["twitter", "linkedin", "facebook"]:
        result = await social_agent.execute({
            "type": "post",
            "topic": f"New article: {topic}",
            "platform": platform
        })
        if result["status"] == "success":
            social_posts.append(result["content"])
    
    print(f"✅ Created {len(social_posts)} promotional posts")
    
    # Summary
    print("\n" + "="*60)
    print("📊 Collaboration Results")
    print("="*60)
    print(f"✅ Blog Article: {blog_result['article']['title']}")
    print(f"✅ Keywords Used: {', '.join(keywords)}")
    print(f"✅ Promotional Posts: {len(social_posts)} across multiple platforms")


async def export_all_results():
    """Example: Generate content and export everything."""
    print("\n" + "="*60)
    print("💾 Export All Results Example")
    print("="*60)
    
    settings = get_settings()
    
    # Initialize agents
    lead_agent = LeadGeneratorAgent(max_results=settings.lead_gen_max_results)
    social_agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    blog_agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    campaign_name = "tech_campaign_2025"
    
    print(f"\n📦 Campaign: {campaign_name}")
    
    # Generate all content
    results = await asyncio.gather(
        lead_agent.execute({
            "query": "technology companies",
            "location": "Boston, MA",
            "max_results": 15
        }),
        social_agent.create_campaign(
            topic="Technology Trends 2025",
            duration_days=7,
            platforms=["twitter", "linkedin", "instagram"]
        ),
        blog_agent.batch_generate([
            "Future of Technology",
            "AI in Business",
            "Tech Innovation 2025"
        ])
    )
    
    # Export all results
    import json
    from datetime import datetime
    
    campaign_data = {
        "campaign_name": campaign_name,
        "created_at": datetime.now().isoformat(),
        "leads": results[0],
        "social_campaign": results[1],
        "blog_articles": results[2]
    }
    
    # Save to output directory
    output_file = Path("./output") / f"{campaign_name}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(campaign_data, f, indent=2)
    
    print(f"\n✅ Campaign exported to: {output_file}")
    print(f"📊 Summary:")
    print(f"  Leads: {results[0].get('count', 0)}")
    print(f"  Social Posts: {results[1].get('total_posts', 0)}")
    print(f"  Blog Articles: {results[2].get('successful', 0)}")
    print(f"  File Size: {output_file.stat().st_size:,} bytes")


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("🤖 Complete Agent Framework - Examples")
    print("All 3 agents working together")
    print("="*60)
    
    try:
        await complete_marketing_workflow()
        await parallel_agent_execution()
        await agent_collaboration()
        await export_all_results()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

"""
Social Media Manager Agent Example
Demonstrates social media content creation and campaign management.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agents import SocialMediaManagerAgent
from backend.config import get_settings


async def generate_single_post():
    """Example: Generate a single social media post."""
    print("\n" + "="*60)
    print("Example 1: Generate Single Social Media Post")
    print("="*60)
    
    settings = get_settings()
    agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    
    task = {
        "type": "post",
        "topic": "Artificial Intelligence in Business",
        "platform": "linkedin",
        "tone": "professional"
    }
    
    print(f"\n📝 Generating post for {task['platform']}...")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        content = result["content"]
        print(f"✅ Post generated!")
        print(f"\n📱 Platform: {content['platform']}")
        print(f"✍️  Text: {content['text']}")
        print(f"#️⃣  Hashtags: {', '.join(content['hashtags'])}")
        print(f"🖼️  Image Prompt: {content['image_prompt']}")
        print(f"📊 Character Count: {content['char_count']}")
    else:
        print(f"❌ Error: {result.get('error')}")


async def create_content_calendar():
    """Example: Create a 7-day content calendar."""
    print("\n" + "="*60)
    print("Example 2: Create Content Calendar")
    print("="*60)
    
    settings = get_settings()
    agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    
    task = {
        "type": "calendar",
        "topic": "Digital Marketing Tips",
        "count": 7
    }
    
    print(f"\n📅 Creating {task['count']}-day content calendar...")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        calendar = result["content"]
        print(f"✅ Calendar created with {len(calendar)} posts")
        print("\n📆 Schedule:")
        for day in calendar[:3]:  # Show first 3 days
            print(f"\n  Day {day['day']}: {day['topic']}")
            print(f"    Type: {day['post_type']}")
            print(f"    Platform: {day['platform']}")
            print(f"    Status: {day['status']}")
        if len(calendar) > 3:
            print(f"\n  ... and {len(calendar) - 3} more days")
    else:
        print(f"❌ Error: {result.get('error')}")


async def research_hashtags():
    """Example: Research relevant hashtags."""
    print("\n" + "="*60)
    print("Example 3: Hashtag Research")
    print("="*60)
    
    settings = get_settings()
    agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    
    task = {
        "type": "hashtags",
        "topic": "Content Marketing",
        "platform": "twitter"
    }
    
    print(f"\n🔍 Researching hashtags for: {task['topic']}")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        hashtags = result["content"]
        print(f"✅ Found {len(hashtags)} relevant hashtags")
        print("\n#️⃣  Top Hashtags:")
        for i, tag in enumerate(hashtags[:5], 1):
            print(f"  {i}. {tag['tag']}")
            print(f"     Popularity: {tag['popularity']}")
            print(f"     Relevance: {tag['relevance']:.0%}")
    else:
        print(f"❌ Error: {result.get('error')}")


async def create_complete_campaign():
    """Example: Create a complete multi-platform campaign."""
    print("\n" + "="*60)
    print("Example 4: Complete Social Media Campaign")
    print("="*60)
    
    settings = get_settings()
    agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    
    topic = "Product Launch: AI Assistant"
    platforms = ["twitter", "linkedin", "instagram"]
    duration = 5
    
    print(f"\n🚀 Creating {duration}-day campaign for: {topic}")
    print(f"📱 Platforms: {', '.join(platforms)}")
    
    result = await agent.create_campaign(
        topic=topic,
        duration_days=duration,
        platforms=platforms
    )
    
    if result["status"] == "success":
        print(f"\n✅ Campaign created successfully!")
        print(f"📊 Statistics:")
        print(f"  Duration: {result['duration']} days")
        print(f"  Platforms: {len(result['platforms'])}")
        print(f"  Total Posts: {result['total_posts']}")
        print(f"  Posts per Platform: {result['total_posts'] // len(result['platforms'])}")
        
        print(f"\n📅 Sample Posts:")
        for post in result['posts'][:3]:
            print(f"\n  Day {post['day']} - {post['platform']}:")
            print(f"    {post['text'][:60]}...")
    else:
        print(f"❌ Error: {result.get('error')}")


async def multi_platform_posting():
    """Example: Generate posts for multiple platforms."""
    print("\n" + "="*60)
    print("Example 5: Multi-Platform Post Generation")
    print("="*60)
    
    settings = get_settings()
    agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    
    topic = "Remote Work Best Practices"
    platforms = ["twitter", "linkedin", "facebook"]
    
    print(f"\n📱 Generating posts for {len(platforms)} platforms...")
    print(f"📝 Topic: {topic}\n")
    
    for platform in platforms:
        task = {
            "type": "post",
            "topic": topic,
            "platform": platform,
            "tone": "professional"
        }
        
        result = await agent.execute(task)
        
        if result["status"] == "success":
            content = result["content"]
            print(f"✅ {platform.title()}:")
            print(f"   {content['text'][:80]}...")
            print(f"   Hashtags: {', '.join(content['hashtags'][:3])}")
        else:
            print(f"❌ {platform.title()}: Error")


async def export_campaign():
    """Example: Create and export campaign to file."""
    print("\n" + "="*60)
    print("Example 6: Export Campaign to File")
    print("="*60)
    
    settings = get_settings()
    agent = SocialMediaManagerAgent(default_tone=settings.default_tone)
    
    result = await agent.create_campaign(
        topic="Holiday Season Marketing",
        duration_days=7,
        platforms=["twitter", "linkedin", "instagram"]
    )
    
    if result["status"] == "success":
        # Export to file
        output_file = Path(settings.output_dir_social) / "holiday_campaign.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Campaign exported to: {output_file}")
        print(f"📁 File size: {output_file.stat().st_size} bytes")
        print(f"📊 Campaign includes {result['total_posts']} posts")
    else:
        print(f"❌ Error: {result.get('error')}")


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("🤖 Social Media Manager Agent - Examples")
    print("="*60)
    
    try:
        await generate_single_post()
        await create_content_calendar()
        await research_hashtags()
        await create_complete_campaign()
        await multi_platform_posting()
        await export_campaign()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

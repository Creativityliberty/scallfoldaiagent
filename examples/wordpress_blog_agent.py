"""
WordPress Blogger Agent Example
Demonstrates SEO-optimized article generation and WordPress publishing.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.agents import WordPressBloggerAgent
from backend.config import get_settings


async def generate_single_article():
    """Example: Generate a single SEO-optimized article."""
    print("\n" + "="*60)
    print("Example 1: Generate SEO-Optimized Article")
    print("="*60)
    
    settings = get_settings()
    agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    task = {
        "topic": "Machine Learning for Beginners",
        "tone": "educational",
        "word_count": 1500
    }
    
    print(f"\n✍️  Generating article: {task['topic']}")
    print(f"📊 Target word count: {task['word_count']}")
    
    result = await agent.execute(task)
    
    if result["status"] == "success":
        article = result["article"]
        seo = result["seo_score"]
        
        print(f"\n✅ Article generated successfully!")
        print(f"\n📄 Article Details:")
        print(f"  Title: {article['title']}")
        print(f"  Slug: {article['slug']}")
        print(f"  Word Count: {article['word_count']}")
        print(f"  Sections: {len(article['sections'])}")
        
        print(f"\n📈 SEO Score: {seo['overall']}/100")
        print(f"  Keyword Optimization: {seo['keyword_density']}/100")
        print(f"  Readability: {seo['readability']}/100")
        print(f"  Title Optimization: {seo['title_optimization']}/100")
        
        print(f"\n🔑 Keywords ({len(result['keywords'])}):")
        for kw in result['keywords'][:3]:
            print(f"  • {kw['keyword']} (volume: {kw['search_volume']}, difficulty: {kw['difficulty']})")
    else:
        print(f"❌ Error: {result.get('error')}")


async def generate_with_publishing():
    """Example: Generate and publish article to WordPress."""
    print("\n" + "="*60)
    print("Example 2: Generate and Publish to WordPress")
    print("="*60)
    
    settings = get_settings()
    
    if not settings.wordpress_url:
        print("⚠️  WordPress URL not configured, skipping publish...")
        print("   Set WORDPRESS_URL in .env to enable publishing")
        return
    
    agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    task = {
        "topic": "Content Marketing Strategies",
        "tone": "professional",
        "word_count": 2000,
        "publish": True  # Enable publishing
    }
    
    print(f"\n✍️  Generating and publishing: {task['topic']}")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        print(f"✅ Article created!")
        
        if result.get("published"):
            print(f"🚀 Published to WordPress!")
            print(f"   URL: {result.get('post_url')}")
        else:
            print(f"📝 Saved as draft (not published)")
    else:
        print(f"❌ Error: {result.get('error')}")


async def batch_article_generation():
    """Example: Generate multiple articles in batch."""
    print("\n" + "="*60)
    print("Example 3: Batch Article Generation")
    print("="*60)
    
    settings = get_settings()
    agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    topics = [
        "Python Programming Best Practices",
        "Web Development Trends 2025",
        "Cloud Computing Essentials"
    ]
    
    print(f"\n🔄 Generating {len(topics)} articles in batch...")
    result = await agent.batch_generate(topics, publish=False)
    
    if result["status"] == "success":
        print(f"\n✅ Batch generation completed!")
        print(f"📊 Statistics:")
        print(f"  Total Topics: {result['total_topics']}")
        print(f"  Successful: {result['successful']}")
        print(f"  Failed: {result['failed']}")
        
        print(f"\n📚 Generated Articles:")
        for article in result['articles']:
            print(f"  • {article['topic']}")
            print(f"    Word Count: {article['word_count']}")
            print(f"    SEO Score: {article['seo_score']['overall']}/100")
    else:
        print(f"❌ Error: {result.get('error')}")


async def article_with_seo_analysis():
    """Example: Generate article with detailed SEO analysis."""
    print("\n" + "="*60)
    print("Example 4: Article with SEO Analysis")
    print("="*60)
    
    settings = get_settings()
    agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    task = {
        "topic": "Artificial Intelligence Ethics",
        "word_count": 1800
    }
    
    print(f"\n🔍 Generating article with SEO analysis...")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        seo = result["seo_score"]
        meta = result["meta"]
        
        print(f"\n✅ Article: {result['topic']}")
        
        print(f"\n📊 Detailed SEO Scores:")
        for metric, score in seo.items():
            if isinstance(score, (int, float)):
                status = "✅" if score >= 70 else "⚠️" if score >= 50 else "❌"
                print(f"  {status} {metric.replace('_', ' ').title()}: {score}/100")
        
        print(f"\n🏷️  Meta Information:")
        print(f"  Title: {meta['title']}")
        print(f"  Description: {meta['description'][:60]}...")
        print(f"  Keywords: {', '.join(meta['keywords'][:3])}")
    else:
        print(f"❌ Error: {result.get('error')}")


async def export_article():
    """Example: Generate article and export to file."""
    print("\n" + "="*60)
    print("Example 5: Export Article to File")
    print("="*60)
    
    settings = get_settings()
    agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    task = {
        "topic": "DevOps Best Practices",
        "word_count": 2000,
        "tone": "professional"
    }
    
    print(f"\n✍️  Generating article: {task['topic']}")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        # Export to JSON
        output_file = Path(settings.output_dir_blog) / "devops_best_practices.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Article exported to: {output_file}")
        print(f"📁 File size: {output_file.stat().st_size} bytes")
        
        # Also save HTML version
        html_file = output_file.with_suffix(".html")
        with open(html_file, "w") as f:
            f.write(f"<html><head><title>{result['article']['title']}</title></head>")
            f.write(f"<body>{result['article']['content']}</body></html>")
        
        print(f"📄 HTML version: {html_file}")
    else:
        print(f"❌ Error: {result.get('error')}")


async def article_sections_breakdown():
    """Example: Show article structure and sections."""
    print("\n" + "="*60)
    print("Example 6: Article Structure Analysis")
    print("="*60)
    
    settings = get_settings()
    agent = WordPressBloggerAgent(
        wordpress_url=settings.wordpress_url,
        target_word_count=settings.target_word_count,
        min_seo_score=settings.min_seo_score
    )
    
    task = {
        "topic": "Cybersecurity Fundamentals",
        "word_count": 1800
    }
    
    print(f"\n📝 Analyzing article structure for: {task['topic']}")
    result = await agent.execute(task)
    
    if result["status"] == "success":
        article = result["article"]
        
        print(f"\n✅ Article Structure:")
        print(f"  Title: {article['title']}")
        print(f"  Total Word Count: {article['word_count']}")
        print(f"  Number of Sections: {len(article['sections'])}")
        
        print(f"\n📑 Section Breakdown:")
        for i, section in enumerate(article['sections'], 1):
            print(f"\n  {i}. {section['title']}")
            print(f"     Words: {section['word_count']}")
            print(f"     Percentage: {(section['word_count']/article['word_count'])*100:.1f}%")
    else:
        print(f"❌ Error: {result.get('error')}")


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("🤖 WordPress Blogger Agent - Examples")
    print("="*60)
    
    try:
        await generate_single_article()
        await generate_with_publishing()
        await batch_article_generation()
        await article_with_seo_analysis()
        await export_article()
        await article_sections_breakdown()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

"""
Social Media Manager Agent - Creates and manages social media content.
"""
from typing import Dict, Any, List
from loguru import logger
from .base_agent import BaseAgent


class SocialMediaManagerAgent(BaseAgent):
    """
    Agent specialized in social media content creation and management.
    
    Capabilities:
    - Generate social media posts
    - Create content calendars
    - Research hashtags
    - Generate image prompts for DALL-E
    - Analyze post performance
    """

    def __init__(self, **kwargs):
        super().__init__(
            name="social_media_manager",
            description="Creates and manages social media content across platforms",
            **kwargs
        )

    def initialize_tools(self) -> None:
        """Register social media tools with MCP server."""
        self.tools = [
            "generate_social_post",
            "create_content_calendar",
            "hashtag_research",
            "generate_image_prompt",
            "analyze_post_performance"
        ]
        logger.info(f"Social Media Manager tools initialized: {len(self.tools)} tools")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute social media task.

        Args:
            task: Task configuration with fields:
                - type: Task type (post, calendar, hashtags)
                - topic: Content topic
                - platform: Target platform (twitter, linkedin, instagram, etc.)
                - tone: Content tone (professional, casual, etc.)
                - count: Number of items to generate

        Returns:
            Dictionary with generated content and metadata
        """
        try:
            task_type = task.get("type", "post")
            topic = task.get("topic", "")
            platform = task.get("platform", "twitter")
            tone = task.get("tone", "professional")
            
            if not topic:
                return {
                    "status": "error",
                    "error": "Topic parameter is required"
                }

            logger.info(f"Social media task started: {task_type} for {platform}")

            if task_type == "post":
                content = await self._generate_post(topic, platform, tone)
            elif task_type == "calendar":
                content = await self._create_calendar(topic, task.get("count", 7))
            elif task_type == "hashtags":
                content = await self._research_hashtags(topic, platform)
            else:
                return {
                    "status": "error",
                    "error": f"Unknown task type: {task_type}"
                }

            result = {
                "status": "success",
                "type": task_type,
                "platform": platform,
                "content": content
            }

            self._log_execution(task, result)
            return result

        except Exception as e:
            logger.error(f"Social media task failed: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }

    async def _generate_post(
        self, 
        topic: str, 
        platform: str, 
        tone: str
    ) -> Dict[str, Any]:
        """Generate a social media post."""
        # Simulate post generation
        post = {
            "text": f"Exciting update about {topic}! #Innovation #Growth",
            "platform": platform,
            "tone": tone,
            "hashtags": ["#Innovation", "#Growth", f"#{topic.replace(' ', '')}"],
            "image_prompt": f"Professional image representing {topic}",
            "char_count": 150
        }
        return post

    async def _create_calendar(
        self, 
        topic: str, 
        days: int
    ) -> List[Dict[str, Any]]:
        """Create a content calendar."""
        calendar = []
        for i in range(days):
            calendar.append({
                "day": i + 1,
                "topic": f"{topic} - Day {i+1}",
                "post_type": "educational" if i % 2 == 0 else "promotional",
                "platform": "multi",
                "status": "planned"
            })
        return calendar

    async def _research_hashtags(
        self, 
        topic: str, 
        platform: str
    ) -> List[Dict[str, Any]]:
        """Research relevant hashtags."""
        hashtags = [
            {"tag": f"#{topic.replace(' ', '')}", "popularity": "high", "relevance": 0.95},
            {"tag": "#Business", "popularity": "high", "relevance": 0.85},
            {"tag": "#Marketing", "popularity": "medium", "relevance": 0.80},
            {"tag": "#Growth", "popularity": "medium", "relevance": 0.75},
            {"tag": "#Success", "popularity": "high", "relevance": 0.70}
        ]
        return hashtags

    async def create_campaign(
        self, 
        topic: str, 
        duration_days: int = 7,
        platforms: List[str] = None
    ) -> Dict[str, Any]:
        """
        Create a complete social media campaign.

        Args:
            topic: Campaign topic
            duration_days: Campaign duration in days
            platforms: List of target platforms

        Returns:
            Complete campaign with calendar and posts
        """
        if platforms is None:
            platforms = ["twitter", "linkedin", "instagram"]

        calendar = await self._create_calendar(topic, duration_days)
        posts = []
        
        for day in calendar:
            for platform in platforms:
                post = await self._generate_post(topic, platform, "professional")
                post["day"] = day["day"]
                posts.append(post)

        return {
            "status": "success",
            "topic": topic,
            "duration": duration_days,
            "platforms": platforms,
            "calendar": calendar,
            "posts": posts,
            "total_posts": len(posts)
        }

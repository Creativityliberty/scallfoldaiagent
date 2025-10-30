"""
Lead Generator Agent - Searches and enriches business leads.
"""
from typing import Dict, Any, List
from loguru import logger
from .base_agent import BaseAgent


class LeadGeneratorAgent(BaseAgent):
    """
    Agent specialized in finding and enriching business leads.
    
    Capabilities:
    - Search businesses on Google Maps
    - Extract contact information
    - Enrich lead data
    - Qualify leads based on criteria
    - Batch processing support
    """

    def __init__(self, **kwargs):
        super().__init__(
            name="lead_generator",
            description="Finds and enriches business leads from various sources",
            **kwargs
        )

    def initialize_tools(self) -> None:
        """Register lead generation tools with MCP server."""
        self.tools = [
            "search_google_maps",
            "extract_business_email",
            "enrich_lead_data",
            "qualify_lead",
            "save_leads_to_db"
        ]
        logger.info(f"Lead Generator tools initialized: {len(self.tools)} tools")

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute lead generation task.

        Args:
            task: Task configuration with fields:
                - query: Search query for businesses
                - location: Target location
                - max_results: Maximum number of results
                - qualify: Whether to qualify leads
                - enrich: Whether to enrich lead data

        Returns:
            Dictionary with generated leads and metadata
        """
        try:
            query = task.get("query", "")
            location = task.get("location", "")
            max_results = task.get("max_results", 50)
            
            if not query:
                return {
                    "status": "error",
                    "error": "Query parameter is required"
                }

            logger.info(f"Lead generation started: {query} in {location}")

            # Simulate lead generation process
            leads = []
            for i in range(min(max_results, 10)):  # Limit for demo
                lead = {
                    "id": f"lead_{i+1}",
                    "name": f"Business {i+1}",
                    "location": location,
                    "query": query,
                    "status": "new",
                    "score": 0.8 + (i * 0.01)
                }
                leads.append(lead)

            result = {
                "status": "success",
                "leads": leads,
                "count": len(leads),
                "query": query,
                "location": location
            }

            self._log_execution(task, result)
            return result

        except Exception as e:
            logger.error(f"Lead generation failed: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }

    async def search_businesses(
        self, 
        query: str, 
        location: str, 
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search for businesses matching criteria.

        Args:
            query: Search query
            location: Target location
            max_results: Maximum results to return

        Returns:
            List of business leads
        """
        task = {
            "query": query,
            "location": location,
            "max_results": max_results
        }
        result = await self.execute(task)
        return result.get("leads", [])

    async def batch_process(
        self, 
        queries: List[str], 
        location: str
    ) -> Dict[str, Any]:
        """
        Process multiple lead generation queries in batch.

        Args:
            queries: List of search queries
            location: Target location

        Returns:
            Aggregated results from all queries
        """
        all_leads = []
        for query in queries:
            result = await self.execute({
                "query": query,
                "location": location
            })
            if result["status"] == "success":
                all_leads.extend(result["leads"])

        return {
            "status": "success",
            "total_leads": len(all_leads),
            "queries_processed": len(queries),
            "leads": all_leads
        }

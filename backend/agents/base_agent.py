"""
Base agent class providing common functionality for all agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from loguru import logger


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the framework.
    Provides common initialization and execution patterns.
    """

    def __init__(
        self,
        name: str,
        description: str,
        orchestrator: Optional[Any] = None,
        mcp_server: Optional[Any] = None,
        **kwargs
    ):
        """
        Initialize the base agent.

        Args:
            name: Agent name
            description: Agent description
            orchestrator: Optional orchestrator instance
            mcp_server: Optional MCP server instance for tool registration
            **kwargs: Additional configuration parameters
        """
        self.name = name
        self.description = description
        self.orchestrator = orchestrator
        self.mcp_server = mcp_server
        self.config = kwargs
        self.tools: List[str] = []
        
        logger.info(f"Initializing agent: {self.name}")
        self.initialize_tools()

    @abstractmethod
    def initialize_tools(self) -> None:
        """
        Initialize and register tools specific to this agent.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main task.

        Args:
            task: Task parameters and configuration

        Returns:
            Result dictionary with status and output
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Dictionary with agent metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "tools": self.tools,
            "config": self.config
        }

    def _log_execution(self, task: Dict[str, Any], result: Dict[str, Any]) -> None:
        """
        Log agent execution details.

        Args:
            task: Input task
            result: Execution result
        """
        logger.info(
            f"Agent {self.name} executed | "
            f"Task: {task.get('type', 'unknown')} | "
            f"Status: {result.get('status', 'unknown')}"
        )

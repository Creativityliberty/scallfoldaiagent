import httpx
import re
from typing import Dict, Any, Optional
from loguru import logger

class GitMCPClient:
    """
    Intégration GitMCP pour récupérer le contexte des repos GitHub.
    Convertit les URLs GitHub en URLs GitMCP et récupère llms.txt, README, etc.
    """
    
    GITMCP_BASE = "https://gitmcp.io"
    GITHUB_BASE = "https://github.com"
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Convertit une URL GitHub en URL GitMCP."""
        # github.com/user/repo → gitmcp.io/user/repo
        url = url.strip()
        if "github.com" in url:
            url = url.replace("github.com", "gitmcp.io")
        elif "github.io" in url:
            # username.github.io/repo → username.gitmcp.io/repo
            url = re.sub(r"(\w+)\.github\.io", r"\1.gitmcp.io", url)
        
        # Nettoyer les suffixes
        url = url.rstrip("/")
        if url.endswith(".git"):
            url = url[:-4]
        
        return url
    
    @staticmethod
    async def fetch_context(repo_url: str) -> Dict[str, Any]:
        """
        Récupère le contexte du repo (llms.txt, README, etc).
        """
        try:
            gitmcp_url = GitMCPClient.normalize_url(repo_url)
            logger.info(f"Fetching GitMCP context from: {gitmcp_url}")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Essayer llms.txt d'abord
                llms_txt = await GitMCPClient._fetch_file(client, gitmcp_url, "llms.txt")
                
                # Fallback: llms-full.txt
                if not llms_txt:
                    llms_txt = await GitMCPClient._fetch_file(client, gitmcp_url, "llms-full.txt")
                
                # README
                readme = await GitMCPClient._fetch_file(client, gitmcp_url, "README.md")
                
                return {
                    "success": True,
                    "url": gitmcp_url,
                    "llms_context": llms_txt or "",
                    "readme": readme or "",
                    "source": "gitmcp"
                }
        
        except Exception as e:
            logger.error(f"GitMCP fetch error: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": repo_url
            }
    
    @staticmethod
    async def _fetch_file(client: httpx.AsyncClient, gitmcp_url: str, filename: str) -> Optional[str]:
        """Récupère un fichier spécifique du repo."""
        try:
            # Construire l'URL du fichier brut
            file_url = f"{gitmcp_url}/raw/main/{filename}"
            response = await client.get(file_url, follow_redirects=True)
            
            if response.status_code == 200:
                logger.debug(f"Successfully fetched {filename} from {gitmcp_url}")
                return response.text
            
            # Essayer 'master' si 'main' échoue
            if response.status_code == 404:
                file_url = f"{gitmcp_url}/raw/master/{filename}"
                response = await client.get(file_url, follow_redirects=True)
                if response.status_code == 200:
                    return response.text
        
        except Exception as e:
            logger.debug(f"Could not fetch {filename}: {e}")
        
        return None
    
    @staticmethod
    def extract_summary(context: Dict[str, Any]) -> str:
        """Extrait un résumé du contexte pour injection dans le prompt."""
        if not context.get("success"):
            return ""
        
        summary = f"## Repository Context\n"
        summary += f"**URL**: {context.get('url', 'N/A')}\n\n"
        
        if context.get("llms_context"):
            summary += f"### LLMs Context\n{context['llms_context'][:500]}...\n\n"
        
        if context.get("readme"):
            summary += f"### README\n{context['readme'][:500]}...\n\n"
        
        return summary

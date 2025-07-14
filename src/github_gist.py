"""
GitHub Gist integration for sharing Engoo lessons.
Handles creating and updating gists with generated HTML content.
"""

import os
import requests
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class GitHubGistClient:
    """Client for interacting with GitHub Gists API."""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the GitHub Gist client.
        
        Args:
            github_token: GitHub personal access token. If None, will try to get from environment.
        """
        self.token = github_token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass token directly.")
        
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def create_gist(self, 
                   content: str, 
                   filename: Optional[str] = None, 
                   description: Optional[str] = None, 
                   public: bool = True) -> Dict[str, Any]:
        """
        Create a new GitHub Gist.
        
        Args:
            content: HTML content to upload
            filename: Name for the gist file (default: auto-generated)
            description: Description for the gist (default: auto-generated)
            public: Whether the gist should be public
            
        Returns:
            Dictionary containing gist information including URLs
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"engoo_lesson_{timestamp}.html"
        
        if not description:
            # Try to extract title from HTML content
            title = self._extract_title_from_html(content)
            description = f"Engoo ESL Lesson: {title}" if title else f"Engoo ESL Lesson - {datetime.now().strftime('%Y-%m-%d')}"
        
        gist_data = {
            "description": description,
            "public": public,
            "files": {
                filename: {
                    "content": content
                }
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/gists",
                headers=self.headers,
                data=json.dumps(gist_data)
            )
            response.raise_for_status()
            
            gist_info = response.json()
            
            # Generate the HTMLPreview URL
            raw_url = gist_info["files"][filename]["raw_url"]
            preview_url = f"https://htmlpreview.github.io/?{raw_url}"
            
            result = {
                "gist_id": gist_info["id"],
                "gist_url": gist_info["html_url"],
                "raw_url": raw_url,
                "preview_url": preview_url,
                "filename": filename,
                "description": description
            }
            
            logger.info(f"Created gist {gist_info['id']}: {description}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create gist: {e}")
            raise
    
    def update_gist(self, 
                   gist_id: str, 
                   content: str, 
                   filename: Optional[str] = None, 
                   description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing GitHub Gist.
        
        Args:
            gist_id: ID of the existing gist
            content: New HTML content
            filename: Name for the gist file (if None, uses existing)
            description: New description (if None, keeps existing)
            
        Returns:
            Dictionary containing updated gist information
        """
        # First, get the existing gist to preserve filename if not specified
        existing_gist = self.get_gist(gist_id)
        if not existing_gist:
            raise ValueError(f"Gist {gist_id} not found")
        
        if not filename:
            # Use the first HTML file found in the existing gist
            for file_name, file_info in existing_gist["files"].items():
                if file_name.endswith('.html'):
                    filename = file_name
                    break
            
            if not filename:
                filename = "engoo_lesson.html"
        
        update_data: Dict[str, Any] = {
            "files": {
                filename: {
                    "content": content
                }
            }
        }
        
        if description:
            update_data["description"] = description
        
        try:
            response = requests.patch(
                f"{self.base_url}/gists/{gist_id}",
                headers=self.headers,
                data=json.dumps(update_data)
            )
            response.raise_for_status()
            
            gist_info = response.json()
            
            # Generate the HTMLPreview URL
            raw_url = gist_info["files"][filename]["raw_url"]
            preview_url = f"https://htmlpreview.github.io/?{raw_url}"
            
            result = {
                "gist_id": gist_info["id"],
                "gist_url": gist_info["html_url"],
                "raw_url": raw_url,
                "preview_url": preview_url,
                "filename": filename,
                "description": gist_info.get("description", "")
            }
            
            logger.info(f"Updated gist {gist_id}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update gist {gist_id}: {e}")
            raise
    
    def get_gist(self, gist_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an existing gist.
        
        Args:
            gist_id: ID of the gist
            
        Returns:
            Gist information or None if not found
        """
        try:
            response = requests.get(
                f"{self.base_url}/gists/{gist_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get gist {gist_id}: {e}")
            return None
    
    def _extract_title_from_html(self, html_content: str) -> Optional[str]:
        """
        Extract title from HTML content for gist description.
        
        Args:
            html_content: HTML string
            
        Returns:
            Extracted title or None
        """
        try:
            # Look for <title> tag
            import re
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                # Remove " - Daily News" suffix if present
                title = re.sub(r'\s*-\s*Daily News\s*$', '', title)
                return title
            
            # Look for h1 with article-title class
            h1_match = re.search(r'<h1[^>]*class="[^"]*article-title[^"]*"[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
            if h1_match:
                return h1_match.group(1).strip()
            
            return None
        except Exception:
            return None


def create_shareable_lesson(html_content: str, 
                          description: Optional[str] = None, 
                          gist_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to create or update a shareable lesson gist.
    
    Args:
        html_content: The generated HTML lesson content
        description: Optional description for the gist
        gist_id: If provided, update this existing gist instead of creating new one
        
    Returns:
        Dictionary with gist information and shareable URLs
    """
    client = GitHubGistClient()
    
    if gist_id:
        return client.update_gist(gist_id, html_content, description=description)
    else:
        return client.create_gist(html_content, description=description)

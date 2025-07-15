"""
GitHub Gist integration for sharing Engoo lessons.
Handles creating, updating, listing, and deleting gists with generated HTML content.
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
            raise Exception(f"Failed to create gist: {e}")
    
    def update_gist(self, 
                   gist_id: str, 
                   content: str, 
                   filename: Optional[str] = None, 
                   description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing GitHub Gist.
        
        Args:
            gist_id: ID of the gist to update
            content: New HTML content
            filename: Name for the gist file (if None, uses existing filename)
            description: New description (if None, keeps existing)
            
        Returns:
            Dictionary containing updated gist information
        """
        # First get the existing gist to preserve filename if not specified
        existing_gist_response = self.get_gist(gist_id)
        if not existing_gist_response['success']:
            raise Exception(f"Failed to get existing gist: {existing_gist_response['error']}")
        
        existing_gist = existing_gist_response['gist']
        
        if not filename:
            # Use the first HTML file from existing gist
            html_files = [f for f in existing_gist['files'] if f.endswith('.html')]
            if html_files:
                filename = html_files[0]
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"engoo_lesson_{timestamp}.html"
        
        if not description:
            title = self._extract_title_from_html(content)
            description = f"Engoo ESL Lesson: {title}" if title else existing_gist['description']
        
        gist_data = {
            "description": description,
            "files": {
                filename: {
                    "content": content
                }
            }
        }
        
        try:
            response = requests.patch(
                f"{self.base_url}/gists/{gist_id}",
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
            
            logger.info(f"Updated gist {gist_info['id']}: {description}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update gist {gist_id}: {e}")
            raise Exception(f"Failed to update gist: {e}")
    
    def list_gists(self) -> Dict[str, Any]:
        """
        List all gists for the authenticated user.
        
        Returns:
            Dictionary with gist information
        """
        try:
            response = requests.get(f"{self.base_url}/gists", headers=self.headers)
            response.raise_for_status()
            
            gists = response.json()
            
            # Filter and format gists that look like Engoo lessons
            engoo_gists = []
            for gist in gists:
                # Check if it's likely an Engoo lesson
                is_engoo = False
                for filename, file_info in gist.get('files', {}).items():
                    if (filename.endswith('.html') and 
                        ('engoo' in filename.lower() or 'lesson' in filename.lower() or 'daily' in filename.lower())):
                        is_engoo = True
                        break
                
                # Also check description
                description = gist.get('description', '')
                if any(keyword in description.lower() for keyword in ['engoo', 'lesson', 'esl', 'daily news']):
                    is_engoo = True
                
                if is_engoo:
                    # Get the first HTML file for preview
                    html_files = [f for f in gist['files'].keys() if f.endswith('.html')]
                    preview_url = None
                    if html_files:
                        # Use the gist's HTML URL for HTMLPreview
                        preview_url = f"https://htmlpreview.github.io/?{gist['html_url']}"
                    
                    engoo_gists.append({
                        'id': gist['id'],
                        'description': gist.get('description', 'No description'),
                        'created_at': gist['created_at'],
                        'updated_at': gist['updated_at'],
                        'public': gist['public'],
                        'files': list(gist['files'].keys()),
                        'html_url': gist['html_url'],
                        'preview_url': preview_url
                    })
            
            return {
                'success': True,
                'gists': engoo_gists,
                'total_count': len(engoo_gists)
            }
            
        except requests.RequestException as e:
            logger.error(f"Failed to list gists: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_gist(self, gist_id: str) -> Dict[str, Any]:
        """
        Delete a specific gist.
        
        Args:
            gist_id: ID of the gist to delete
            
        Returns:
            Dictionary with deletion status
        """
        try:
            response = requests.delete(f"{self.base_url}/gists/{gist_id}", headers=self.headers)
            response.raise_for_status()
            
            return {
                'success': True,
                'message': f'Gist {gist_id} deleted successfully'
            }
            
        except requests.RequestException as e:
            logger.error(f"Failed to delete gist {gist_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_gist(self, gist_id: str) -> Dict[str, Any]:
        """
        Get details of a specific gist.
        
        Args:
            gist_id: ID of the gist to retrieve
            
        Returns:
            Dictionary with gist information
        """
        try:
            response = requests.get(f"{self.base_url}/gists/{gist_id}", headers=self.headers)
            response.raise_for_status()
            
            gist = response.json()
            
            # Get the first HTML file for preview
            html_files = [f for f in gist['files'].keys() if f.endswith('.html')]
            preview_url = None
            if html_files:
                preview_url = f"https://htmlpreview.github.io/?{gist['html_url']}"
            
            return {
                'success': True,
                'gist': {
                    'id': gist['id'],
                    'description': gist.get('description', 'No description'),
                    'created_at': gist['created_at'],
                    'updated_at': gist['updated_at'],
                    'public': gist['public'],
                    'files': list(gist['files'].keys()),
                    'html_url': gist['html_url'],
                    'preview_url': preview_url
                }
            }
            
        except requests.RequestException as e:
            logger.error(f"Failed to get gist {gist_id}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_title_from_html(self, html_content: str) -> Optional[str]:
        """
        Extract article title from HTML content.
        
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


# Convenience functions for easier usage
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


def list_engoo_gists() -> Dict[str, Any]:
    """
    Convenience function to list all Engoo lesson gists.
    
    Returns:
        Dictionary with gist listing
    """
    client = GitHubGistClient()
    return client.list_gists()


def delete_engoo_gist(gist_id: str) -> Dict[str, Any]:
    """
    Convenience function to delete an Engoo lesson gist.
    
    Args:
        gist_id: ID of the gist to delete
        
    Returns:
        Dictionary with deletion status
    """
    client = GitHubGistClient()
    return client.delete_gist(gist_id)


def get_engoo_gist(gist_id: str) -> Dict[str, Any]:
    """
    Convenience function to get details of an Engoo lesson gist.
    
    Args:
        gist_id: ID of the gist to retrieve
        
    Returns:
        Dictionary with gist information
    """
    client = GitHubGistClient()
    return client.get_gist(gist_id)


# Additional convenience functions for CLI usage
def list_engoo_gists() -> Dict[str, Any]:
    """
    Convenience function to list all Engoo lesson gists.
    
    Returns:
        Dictionary with gist listing
    """
    client = GitHubGistClient()
    return client.list_gists()


def delete_engoo_gist(gist_id: str) -> Dict[str, Any]:
    """
    Convenience function to delete an Engoo lesson gist.
    
    Args:
        gist_id: ID of the gist to delete
        
    Returns:
        Dictionary with deletion status
    """
    client = GitHubGistClient()
    return client.delete_gist(gist_id)


def get_engoo_gist(gist_id: str) -> Dict[str, Any]:
    """
    Convenience function to get details of an Engoo lesson gist.
    
    Args:
        gist_id: ID of the gist to retrieve
        
    Returns:
        Dictionary with gist information
    """
    client = GitHubGistClient()
    return client.get_gist(gist_id)

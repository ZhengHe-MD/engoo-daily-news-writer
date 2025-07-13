from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
import logging

try:
    from .models import EngooArticle
    from .scraper import WebScraper
    from .processor import ContentProcessor
except ImportError:
    from models import EngooArticle
    from scraper import WebScraper
    from processor import ContentProcessor

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State class for the LangGraph agent."""
    url: str
    raw_content: Dict[str, Any]
    engoo_article: Optional[EngooArticle]
    error: str
    completed: bool


class EngooNewsAgent:
    """Main agent class that orchestrates the conversion process using LangGraph."""
    
    def __init__(self, content_processor: ContentProcessor):
        self.scraper = WebScraper()
        self.processor = content_processor
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("scrape_content", self._scrape_content)
        workflow.add_node("validate_content", self._validate_content)
        workflow.add_node("process_content", self._process_content)
        workflow.add_node("finalize", self._finalize)
        
        # Add edges
        workflow.set_entry_point("scrape_content")
        workflow.add_edge("scrape_content", "validate_content")
        workflow.add_conditional_edges(
            "validate_content",
            self._should_process,
            {
                "process": "process_content",
                "error": "finalize"
            }
        )
        workflow.add_edge("process_content", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    def _scrape_content(self, state: AgentState) -> AgentState:
        """Node: Scrape content from the provided URL."""
        logger.info(f"Scraping content from: {state['url']}")
        
        try:
            raw_content = self.scraper.extract_article_content(state["url"])
            if raw_content:
                state["raw_content"] = raw_content
                logger.info(f"Successfully scraped content: {raw_content['title']}")
            else:
                state["error"] = "Failed to scrape content from URL"
                logger.error(state["error"])
        except Exception as e:
            state["error"] = f"Error during scraping: {str(e)}"
            logger.error(state["error"])
        
        return state
    
    def _validate_content(self, state: AgentState) -> AgentState:
        """Node: Validate that the scraped content is suitable for processing."""
        if state["error"]:
            return state
        
        if not state["raw_content"]:
            state["error"] = "No content was scraped"
            return state
        
        # Check for minimum content requirements
        title = state["raw_content"].get('title', '')
        text = state["raw_content"].get('text', '')
        
        if not title or len(title.strip()) < 10:
            state["error"] = "Article title is too short or missing"
            return state
        
        if not text or len(text.strip()) < 200:
            state["error"] = "Article text is too short (minimum 200 characters)"
            return state
        
        logger.info("Content validation passed")
        return state
    
    def _should_process(self, state: AgentState) -> str:
        """Conditional edge: Determine if content should be processed."""
        return "error" if state["error"] else "process"
    
    def _process_content(self, state: AgentState) -> AgentState:
        """Node: Process the raw content into Engoo format."""
        if state["error"]:
            return state
        
        logger.info("Processing content into Engoo format")
        
        try:
            state["engoo_article"] = self.processor.process_article(state["raw_content"])
            logger.info("Content processing completed successfully")
        except Exception as e:
            state["error"] = f"Error during content processing: {str(e)}"
            logger.error(state["error"])
        
        return state
    
    def _finalize(self, state: AgentState) -> AgentState:
        """Node: Finalize the processing and mark as completed."""
        if not state["error"] and state["engoo_article"]:
            state["completed"] = True
            logger.info("Article conversion completed successfully")
        else:
            logger.error(f"Article conversion failed: {state['error']}")
        
        return state
    
    def convert_article(self, url: str) -> Dict[str, Any]:
        """
        Convert an article from a URL to Engoo daily news format.
        
        Args:
            url: The URL of the article to convert
            
        Returns:
            Dictionary containing the result
        """
        # Initialize state
        initial_state: AgentState = {
            "url": url,
            "raw_content": {},
            "engoo_article": None,
            "error": "",
            "completed": False
        }
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        # Return results
        result = {
            'success': final_state["completed"],
            'url': url,
            'error': final_state["error"] if final_state["error"] else None
        }
        
        if final_state["completed"] and final_state["engoo_article"]:
            engoo_article = final_state["engoo_article"]
            result['article'] = {
                'title': engoo_article.title,
                'vocabulary': [
                    {
                        'word': vocab.word,
                        'definition': vocab.definition,
                        'example': vocab.example
                    }
                    for vocab in engoo_article.vocabulary
                ],
                'article_body': engoo_article.article_body,
                'discussion_questions': [q.question for q in engoo_article.discussion_questions],
                'further_discussion_questions': [q.question for q in engoo_article.further_discussion_questions],
                'html': engoo_article.to_html()
            }
        
        return result

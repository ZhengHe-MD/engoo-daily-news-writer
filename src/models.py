from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import os


@dataclass
class VocabularyItem:
    """Represents a vocabulary word with its definition and example."""
    word: str
    definition: str
    example: str


@dataclass
class DiscussionQuestion:
    """Represents a discussion question."""
    question: str
    level: str = "standard"  # "standard" or "further"


@dataclass
class EngooArticle:
    """Represents the complete Engoo daily news article structure."""
    title: str
    vocabulary: List[VocabularyItem]
    article_body: str
    discussion_questions: List[DiscussionQuestion]
    further_discussion_questions: List[DiscussionQuestion]
    
    def to_html(self) -> str:
        """Convert the article to HTML format exactly like Engoo daily news."""
        # Read the template
        template_path = os.path.join(os.path.dirname(__file__), '..', 'engoo_template.html')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        else:
            # Fallback to simple template if file not found
            return self._simple_html()
        
        # Generate vocabulary HTML
        vocabulary_html = ""
        for vocab in self.vocabulary:
            vocabulary_html += f"""
            <div class="vocabulary-item">
                <div class="vocabulary-word">{vocab.word}</div>
                <div class="vocabulary-definition">{vocab.definition}</div>
                <div class="vocabulary-example">"{vocab.example}"</div>
            </div>"""
        
        # Generate discussion questions HTML
        discussion_html = ""
        for i, question in enumerate(self.discussion_questions, 1):
            discussion_html += f"""
            <div class="question-item">
                <span class="question-number">{i}.</span>
                <span class="question-text">{question.question}</span>
            </div>"""
        
        # Generate further discussion questions HTML
        further_discussion_html = ""
        for i, question in enumerate(self.further_discussion_questions, 1):
            further_discussion_html += f"""
            <div class="question-item">
                <span class="question-number">{i}.</span>
                <span class="question-text">{question.question}</span>
            </div>"""
        
        # Format article content with proper paragraphs
        formatted_content = self._format_article_content(self.article_body)
        
        # Replace placeholders
        html = template.replace('{{title}}', self.title)
        html = html.replace('{{date}}', datetime.now().strftime('%B %d, %Y'))
        html = html.replace('{{vocabulary_items}}', vocabulary_html)
        html = html.replace('{{article_content}}', formatted_content)
        html = html.replace('{{discussion_questions}}', discussion_html)
        html = html.replace('{{further_discussion_questions}}', further_discussion_html)
        
        return html
    
    def _format_article_content(self, content: str) -> str:
        """Format the article content with proper HTML structure."""
        # Split into paragraphs and format
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # Handle headers (marked with **)
            if para.startswith('**') and para.endswith('**'):
                header_text = para.strip('*').strip()
                formatted_paragraphs.append(f'<h3>{header_text}</h3>')
            else:
                # Regular paragraph
                formatted_paragraphs.append(f'<p>{para}</p>')
        
        return '\n'.join(formatted_paragraphs)
    
    def _simple_html(self) -> str:
        """Fallback simple HTML generation."""
        html_parts = []
        
        # Title
        html_parts.append(f"<h1>{self.title}</h1>")
        
        # Vocabulary section
        html_parts.append("<h2>Vocabulary</h2>")
        for vocab in self.vocabulary:
            html_parts.append(f"<div class='vocabulary-item'>")
            html_parts.append(f"<strong>{vocab.word}</strong>: {vocab.definition}")
            html_parts.append(f"<br><em>Example: {vocab.example}</em>")
            html_parts.append("</div>")
        
        # Article body
        html_parts.append("<h2>Article</h2>")
        html_parts.append(f"<div class='article-body'>{self.article_body}</div>")
        
        # Discussion questions
        html_parts.append("<h2>Discussion</h2>")
        for i, question in enumerate(self.discussion_questions, 1):
            html_parts.append(f"<p>{i}. {question.question}</p>")
        
        # Further discussion questions
        html_parts.append("<h2>Further Discussion</h2>")
        for i, question in enumerate(self.further_discussion_questions, 1):
            html_parts.append(f"<p>{i}. {question.question}</p>")
        
        return "\n".join(html_parts)

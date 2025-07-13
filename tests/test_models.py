import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.models import VocabularyItem, DiscussionQuestion, EngooArticle


class TestModels(unittest.TestCase):
    """Test cases for data models."""
    
    def test_vocabulary_item_creation(self):
        """Test VocabularyItem creation."""
        vocab = VocabularyItem(
            word="innovation",
            definition="A new method, idea, or product",
            example="The innovation changed how people work."
        )
        
        self.assertEqual(vocab.word, "innovation")
        self.assertEqual(vocab.definition, "A new method, idea, or product")
        self.assertEqual(vocab.example, "The innovation changed how people work.")
    
    def test_discussion_question_creation(self):
        """Test DiscussionQuestion creation."""
        question = DiscussionQuestion(
            question="What do you think about this topic?",
            level="standard"
        )
        
        self.assertEqual(question.question, "What do you think about this topic?")
        self.assertEqual(question.level, "standard")
    
    def test_engoo_article_creation(self):
        """Test EngooArticle creation."""
        vocab = [VocabularyItem("test", "definition", "example")]
        discussion = [DiscussionQuestion("Question?", "standard")]
        further = [DiscussionQuestion("Advanced question?", "further")]
        
        article = EngooArticle(
            title="Test Article",
            vocabulary=vocab,
            article_body="This is a test article.",
            discussion_questions=discussion,
            further_discussion_questions=further
        )
        
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(len(article.vocabulary), 1)
        self.assertEqual(len(article.discussion_questions), 1)
        self.assertEqual(len(article.further_discussion_questions), 1)
    
    def test_engoo_article_to_html(self):
        """Test HTML generation."""
        vocab = [VocabularyItem("innovation", "New idea", "Innovation helps.")]
        discussion = [DiscussionQuestion("What's your opinion?")]
        further = [DiscussionQuestion("Think deeper?")]
        
        article = EngooArticle(
            title="Test Title",
            vocabulary=vocab,
            article_body="Test content.",
            discussion_questions=discussion,
            further_discussion_questions=further
        )
        
        html = article.to_html()
        
        self.assertIn("<h1>Test Title</h1>", html)
        self.assertIn("<h2>Vocabulary</h2>", html)
        self.assertIn("<strong>innovation</strong>", html)
        self.assertIn("Test content.", html)
        self.assertIn("What's your opinion?", html)
        self.assertIn("Think deeper?", html)


if __name__ == '__main__':
    unittest.main()

from typing import List, Dict, Any
from openai import OpenAI
import json
import logging

try:
    from .models import EngooArticle, VocabularyItem, DiscussionQuestion
except ImportError:
    from models import EngooArticle, VocabularyItem, DiscussionQuestion

logger = logging.getLogger(__name__)


class ContentProcessor:
    """Handles content processing using OpenAI API to generate Engoo-style content."""
    
    def __init__(self, openai_client: OpenAI):
        self.client = openai_client
    
    def process_article(self, raw_content: Dict[str, Any]) -> EngooArticle:
        """
        Process raw article content into Engoo daily news format.
        
        Args:
            raw_content: Dictionary containing title, text, and metadata
            
        Returns:
            EngooArticle object with all sections populated
        """
        # Extract key vocabulary
        vocabulary = self._extract_vocabulary(raw_content['text'])
        
        # Rewrite article body for ESL learners
        article_body = self._rewrite_article_body(raw_content['title'], raw_content['text'])
        
        # Generate discussion questions
        discussion_questions = self._generate_discussion_questions(raw_content['title'], article_body)
        
        # Generate further discussion questions
        further_discussion_questions = self._generate_further_discussion_questions(raw_content['title'], article_body)
        
        return EngooArticle(
            title=raw_content['title'],
            vocabulary=vocabulary,
            article_body=article_body,
            discussion_questions=discussion_questions,
            further_discussion_questions=further_discussion_questions
        )
    
    def _extract_vocabulary(self, text: str) -> List[VocabularyItem]:
        """Extract and define key vocabulary words from the article."""
        prompt = f"""
        From the following article text, extract 8-10 key vocabulary words that would be useful for ESL learners. 
        For each word, provide a clear definition and an example sentence using the word.
        
        Article text:
        {text[:3000]}  # Limit text length
        
        Return the response as a JSON array with objects containing "word", "definition", and "example" fields.
        Focus on words that are:
        - Important for understanding the article
        - Useful for intermediate ESL learners
        - Not too basic (avoid words like "the", "and", "is")
        - Not too advanced (avoid highly technical jargon)
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert ESL teacher creating vocabulary lists for intermediate English learners."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            vocab_data = json.loads(response.choices[0].message.content)
            vocabulary = []
            
            for item in vocab_data.get('vocabulary', []):
                vocabulary.append(VocabularyItem(
                    word=item['word'],
                    definition=item['definition'],
                    example=item['example']
                ))
            
            return vocabulary[:10]  # Limit to 10 items
            
        except Exception as e:
            logger.error(f"Error extracting vocabulary: {e}")
            return []
    
    def _rewrite_article_body(self, title: str, original_text: str) -> str:
        """Rewrite the article body to be suitable for ESL learners."""
        prompt = f"""
        Rewrite the following article to be suitable for intermediate ESL learners while maintaining the key information and news value.
        
        Title: {title}
        
        Original article:
        {original_text[:4000]}  # Limit text length
        
        Guidelines:
        - Use clear, simple sentence structures
        - Avoid overly complex vocabulary
        - Keep sentences reasonably short
        - Maintain the factual content and key points
        - Make it engaging for ESL learners
        - Keep the length appropriate (300-500 words)
        - Use present tense when possible
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert ESL teacher rewriting news articles for intermediate English learners."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error rewriting article body: {e}")
            return original_text[:500]  # Fallback to truncated original
    
    def _generate_discussion_questions(self, title: str, article_body: str) -> List[DiscussionQuestion]:
        """Generate discussion questions based on the article."""
        prompt = f"""
        Based on the following article, create 4-5 discussion questions that would help ESL learners practice speaking and thinking about the topic.
        
        Title: {title}
        Article: {article_body}
        
        Guidelines:
        - Questions should be open-ended and encourage discussion
        - Suitable for intermediate ESL learners
        - Related to the article content
        - Encourage personal opinions and experiences
        - Not too complex or abstract
        
        Return as a JSON array with objects containing "question" field.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert ESL teacher creating discussion questions for intermediate English learners."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response from OpenAI for discussion questions")
                return []
                
            questions_data = json.loads(response_content)
            logger.debug(f"Discussion questions response: {questions_data}")
            questions = []
            
            # Try multiple possible keys for the questions array
            questions_array = (questions_data.get('questions', []) or 
                             questions_data.get('discussion_questions', []) or
                             questions_data.get('items', []) or
                             list(questions_data.values())[0] if questions_data else [])
            
            for item in questions_array:
                if isinstance(item, dict) and 'question' in item:
                    questions.append(DiscussionQuestion(
                        question=item['question'],
                        level="standard"
                    ))
                elif isinstance(item, str):
                    questions.append(DiscussionQuestion(
                        question=item,
                        level="standard"
                    ))
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating discussion questions: {e}")
            return []
    
    def _generate_further_discussion_questions(self, title: str, article_body: str) -> List[DiscussionQuestion]:
        """Generate further discussion questions for more advanced discussion."""
        prompt = f"""
        Based on the following article, create 3-4 more advanced discussion questions that encourage deeper thinking and broader connections.
        
        Title: {title}
        Article: {article_body}
        
        Guidelines:
        - Questions should be more challenging than basic discussion questions
        - Encourage connections to broader topics, personal experiences, or societal issues
        - Suitable for intermediate to advanced ESL learners
        - Promote critical thinking and analysis
        - May involve hypothetical scenarios or future predictions
        
        Return as a JSON array with objects containing "question" field.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert ESL teacher creating advanced discussion questions for intermediate to advanced English learners."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            response_content = response.choices[0].message.content
            if not response_content:
                logger.error("Empty response from OpenAI for further discussion questions")
                return []
                
            questions_data = json.loads(response_content)
            logger.debug(f"Further discussion questions response: {questions_data}")
            questions = []
            
            # Try multiple possible keys for the questions array
            questions_array = (questions_data.get('questions', []) or 
                             questions_data.get('discussion_questions', []) or
                             questions_data.get('items', []) or
                             list(questions_data.values())[0] if questions_data else [])
            
            for item in questions_array:
                if isinstance(item, dict) and 'question' in item:
                    questions.append(DiscussionQuestion(
                        question=item['question'],
                        level="further"
                    ))
                elif isinstance(item, str):
                    questions.append(DiscussionQuestion(
                        question=item,
                        level="further"
                    ))
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating further discussion questions: {e}")
            return []

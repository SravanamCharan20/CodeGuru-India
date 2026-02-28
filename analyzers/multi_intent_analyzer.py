"""
Multi-Intent Analyzer for handling complex user queries with multiple intents.

This module can parse and analyze queries with multiple learning goals.
"""

import logging
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Intent:
    """Single intent extracted from user query."""
    intent_text: str
    intent_type: str  # 'how', 'what', 'why', 'where', 'explain', 'show'
    keywords: List[str]
    priority: int  # 1 (high) to 3 (low)


class MultiIntentAnalyzer:
    """Analyzes user queries to extract multiple intents."""
    
    def __init__(self, langchain_orchestrator):
        """
        Initialize multi-intent analyzer.
        
        Args:
            langchain_orchestrator: LangChainOrchestrator for AI operations
        """
        self.orchestrator = langchain_orchestrator
    
    def analyze_query(self, user_query: str) -> List[Intent]:
        """
        Analyze user query to extract multiple intents.
        
        Args:
            user_query: User's natural language query
            
        Returns:
            List of Intent objects
        """
        try:
            logger.info(f"Analyzing query for multiple intents: {user_query}")
            
            # Use AI to extract intents
            intents = self._extract_intents_with_ai(user_query)
            
            if not intents:
                # Fallback to single intent
                intents = [Intent(
                    intent_text=user_query,
                    intent_type='explain',
                    keywords=self._extract_keywords(user_query),
                    priority=1
                )]
            
            logger.info(f"Extracted {len(intents)} intents")
            return intents
        
        except Exception as e:
            logger.error(f"Intent analysis failed: {e}")
            return [Intent(
                intent_text=user_query,
                intent_type='explain',
                keywords=[],
                priority=1
            )]
    
    def _extract_intents_with_ai(self, query: str) -> List[Intent]:
        """
        Use AI to extract multiple intents from query.
        
        Args:
            query: User query
            
        Returns:
            List of Intent objects
        """
        try:
            prompt = f"""Analyze this user query and extract all distinct learning intents/questions.
For each intent, identify:
1. The specific question or goal
2. The type (how/what/why/where/explain/show)
3. Key technical terms or concepts
4. Priority (1=high, 2=medium, 3=low)

User Query: "{query}"

Respond in this format:
INTENT 1: [intent text]
TYPE: [type]
KEYWORDS: [keyword1, keyword2, ...]
PRIORITY: [1-3]

INTENT 2: ...

Extract all intents:"""
            
            response = self.orchestrator.generate_completion(prompt, max_tokens=500)
            
            # Parse response
            intents = self._parse_intent_response(response)
            
            return intents
        
        except Exception as e:
            logger.warning(f"AI intent extraction failed: {e}")
            return []
    
    def _parse_intent_response(self, response: str) -> List[Intent]:
        """
        Parse AI response into Intent objects.
        
        Args:
            response: AI response text
            
        Returns:
            List of Intent objects
        """
        intents = []
        
        try:
            # Split by INTENT markers
            intent_blocks = response.split('INTENT ')
            
            for block in intent_blocks[1:]:  # Skip first empty split
                lines = block.strip().split('\n')
                
                intent_text = ""
                intent_type = "explain"
                keywords = []
                priority = 2
                
                for line in lines:
                    line = line.strip()
                    
                    if line.startswith('TYPE:'):
                        intent_type = line.replace('TYPE:', '').strip().lower()
                    elif line.startswith('KEYWORDS:'):
                        kw_text = line.replace('KEYWORDS:', '').strip()
                        keywords = [k.strip() for k in kw_text.split(',')]
                    elif line.startswith('PRIORITY:'):
                        try:
                            priority = int(line.replace('PRIORITY:', '').strip()[0])
                        except:
                            priority = 2
                    elif ':' in line and not line.startswith('INTENT'):
                        # This is the intent text
                        intent_text = line.split(':', 1)[1].strip()
                
                if intent_text:
                    intents.append(Intent(
                        intent_text=intent_text,
                        intent_type=intent_type,
                        keywords=keywords,
                        priority=priority
                    ))
        
        except Exception as e:
            logger.warning(f"Failed to parse intent response: {e}")
        
        return intents
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}
        
        words = text.lower().split()
        keywords = [w.strip('.,!?;:()[]{}') for w in words if w.lower() not in stop_words and len(w) > 2]
        
        return keywords

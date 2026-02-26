"""Flashcard manager for spaced repetition learning."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
from session_manager import SessionManager
from analyzers.code_analyzer import CodeAnalysis
import logging
import uuid

logger = logging.getLogger(__name__)


@dataclass
class Flashcard:
    """Represents a learning flashcard."""
    id: str
    front: str
    back: str
    topic: str
    difficulty: str
    last_reviewed: Optional[datetime]
    next_review: datetime
    mastered: bool


class FlashcardManager:
    """Manages flashcard creation, review, and spaced repetition."""
    
    def __init__(self, session_manager: SessionManager):
        """Initialize with session manager."""
        self.session_manager = session_manager
        self._ensure_flashcard_structure()
    
    def _ensure_flashcard_structure(self):
        """Ensure flashcard data structure exists in session."""
        progress = self.session_manager.load_progress()
        
        if "flashcards" not in progress:
            progress["flashcards"] = {
                "cards": [],
                "review_schedule": {}
            }
            self.session_manager.save_progress("flashcard_init", progress)
    
    def generate_flashcards(
        self,
        code_analysis: CodeAnalysis,
        language: str = "english"
    ) -> List[Flashcard]:
        """
        Generate flashcards from code analysis.
        
        Args:
            code_analysis: Code analysis result
            language: Output language
            
        Returns:
            List of generated flashcards
        """
        try:
            flashcards = []
            
            # Generate flashcards from functions
            for func in code_analysis.structure.functions[:5]:  # Limit to 5
                card = Flashcard(
                    id=str(uuid.uuid4()),
                    front=f"What does the function '{func.name}' do?",
                    back=func.docstring or f"Function {func.name} with parameters: {', '.join(func.parameters)}",
                    topic="Functions",
                    difficulty="intermediate",
                    last_reviewed=None,
                    next_review=datetime.now(),
                    mastered=False
                )
                flashcards.append(card)
            
            # Generate flashcards from classes
            for cls in code_analysis.structure.classes[:3]:  # Limit to 3
                card = Flashcard(
                    id=str(uuid.uuid4()),
                    front=f"What is the purpose of the '{cls.name}' class?",
                    back=cls.docstring or f"Class {cls.name} with methods: {', '.join(cls.methods[:5])}",
                    topic="Classes",
                    difficulty="intermediate",
                    last_reviewed=None,
                    next_review=datetime.now(),
                    mastered=False
                )
                flashcards.append(card)
            
            # Generate flashcards from patterns
            for pattern in code_analysis.patterns[:3]:  # Limit to 3
                card = Flashcard(
                    id=str(uuid.uuid4()),
                    front=f"What pattern is used: {pattern.name}?",
                    back=pattern.description,
                    topic="Patterns",
                    difficulty="advanced",
                    last_reviewed=None,
                    next_review=datetime.now(),
                    mastered=False
                )
                flashcards.append(card)
            
            # Save flashcards
            self._save_flashcards(flashcards)
            
            return flashcards
        
        except Exception as e:
            logger.error(f"Failed to generate flashcards: {e}")
            return []
    
    def create_custom_flashcard(
        self,
        front: str,
        back: str,
        topic: str
    ) -> Flashcard:
        """
        Create a custom flashcard.
        
        Args:
            front: Front of card (question)
            back: Back of card (answer)
            topic: Topic category
            
        Returns:
            Created flashcard
        """
        try:
            card = Flashcard(
                id=str(uuid.uuid4()),
                front=front,
                back=back,
                topic=topic,
                difficulty="intermediate",
                last_reviewed=None,
                next_review=datetime.now(),
                mastered=False
            )
            
            self._save_flashcards([card])
            return card
        
        except Exception as e:
            logger.error(f"Failed to create custom flashcard: {e}")
            return None
    
    def get_flashcards_for_review(
        self,
        topic: Optional[str] = None
    ) -> List[Flashcard]:
        """
        Get flashcards due for review.
        
        Args:
            topic: Optional topic filter
            
        Returns:
            List of flashcards due for review
        """
        try:
            progress = self.session_manager.load_progress()
            flashcard_data = progress.get("flashcards", {})
            cards_data = flashcard_data.get("cards", [])
            
            flashcards = []
            now = datetime.now()
            
            for card_dict in cards_data:
                # Parse card
                card = self._dict_to_flashcard(card_dict)
                
                # Filter by topic if specified
                if topic and card.topic != topic:
                    continue
                
                # Check if due for review
                if not card.mastered and card.next_review <= now:
                    flashcards.append(card)
            
            return flashcards
        
        except Exception as e:
            logger.error(f"Failed to get flashcards for review: {e}")
            return []
    
    def mark_reviewed(
        self,
        flashcard_id: str,
        difficulty: str
    ) -> None:
        """
        Mark flashcard as reviewed and update review schedule.
        
        Args:
            flashcard_id: Flashcard ID
            difficulty: Review difficulty (easy, medium, hard)
        """
        try:
            progress = self.session_manager.load_progress()
            flashcard_data = progress.get("flashcards", {})
            cards_data = flashcard_data.get("cards", [])
            
            # Find and update card
            for i, card_dict in enumerate(cards_data):
                if card_dict.get("id") == flashcard_id:
                    # Update review data
                    card_dict["last_reviewed"] = datetime.now().isoformat()
                    
                    # Calculate next review based on difficulty
                    if difficulty == "easy":
                        days_until_next = 7
                    elif difficulty == "medium":
                        days_until_next = 3
                    else:  # hard
                        days_until_next = 1
                    
                    next_review = datetime.now() + timedelta(days=days_until_next)
                    card_dict["next_review"] = next_review.isoformat()
                    
                    cards_data[i] = card_dict
                    break
            
            flashcard_data["cards"] = cards_data
            progress["flashcards"] = flashcard_data
            self.session_manager.save_progress("flashcard_reviewed", progress)
        
        except Exception as e:
            logger.error(f"Failed to mark flashcard as reviewed: {e}")
    
    def mark_mastered(self, flashcard_id: str) -> None:
        """
        Mark flashcard as mastered.
        
        Args:
            flashcard_id: Flashcard ID
        """
        try:
            progress = self.session_manager.load_progress()
            flashcard_data = progress.get("flashcards", {})
            cards_data = flashcard_data.get("cards", [])
            
            # Find and update card
            for i, card_dict in enumerate(cards_data):
                if card_dict.get("id") == flashcard_id:
                    card_dict["mastered"] = True
                    # Set next review far in the future
                    next_review = datetime.now() + timedelta(days=30)
                    card_dict["next_review"] = next_review.isoformat()
                    cards_data[i] = card_dict
                    break
            
            flashcard_data["cards"] = cards_data
            progress["flashcards"] = flashcard_data
            self.session_manager.save_progress("flashcard_mastered", progress)
        
        except Exception as e:
            logger.error(f"Failed to mark flashcard as mastered: {e}")
    
    def _save_flashcards(self, flashcards: List[Flashcard]) -> None:
        """Save flashcards to session."""
        try:
            progress = self.session_manager.load_progress()
            flashcard_data = progress.get("flashcards", {"cards": []})
            
            # Convert flashcards to dicts
            for card in flashcards:
                card_dict = self._flashcard_to_dict(card)
                flashcard_data["cards"].append(card_dict)
            
            progress["flashcards"] = flashcard_data
            self.session_manager.save_progress("flashcards_saved", progress)
        
        except Exception as e:
            logger.error(f"Failed to save flashcards: {e}")
    
    def _flashcard_to_dict(self, card: Flashcard) -> dict:
        """Convert flashcard to dictionary."""
        return {
            "id": card.id,
            "front": card.front,
            "back": card.back,
            "topic": card.topic,
            "difficulty": card.difficulty,
            "last_reviewed": card.last_reviewed.isoformat() if card.last_reviewed else None,
            "next_review": card.next_review.isoformat(),
            "mastered": card.mastered
        }
    
    def _dict_to_flashcard(self, card_dict: dict) -> Flashcard:
        """Convert dictionary to flashcard."""
        return Flashcard(
            id=card_dict.get("id", ""),
            front=card_dict.get("front", ""),
            back=card_dict.get("back", ""),
            topic=card_dict.get("topic", ""),
            difficulty=card_dict.get("difficulty", "intermediate"),
            last_reviewed=datetime.fromisoformat(card_dict["last_reviewed"]) 
                         if card_dict.get("last_reviewed") else None,
            next_review=datetime.fromisoformat(card_dict.get("next_review", datetime.now().isoformat())),
            mastered=card_dict.get("mastered", False)
        )

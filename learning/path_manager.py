"""Learning path manager for structured learning."""
from dataclasses import dataclass
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)


@dataclass
class Resource:
    """Learning resource."""
    title: str
    type: str  # "article", "video", "exercise"
    url: str


@dataclass
class Topic:
    """Learning topic."""
    id: str
    name: str
    description: str
    prerequisites: List[str]
    resources: List[Resource]
    quiz_id: Optional[str]


@dataclass
class LearningPath:
    """Complete learning path."""
    id: str
    name: str
    description: str
    topics: List[Topic]
    estimated_hours: int


class LearningPathManager:
    """Manages structured learning paths and progression."""
    
    def __init__(self):
        """Initialize with predefined learning paths."""
        self.paths = self._initialize_paths()
    
    def get_available_paths(self) -> List[LearningPath]:
        """Get all available learning paths."""
        return list(self.paths.values())
    
    def get_path_details(self, path_id: str) -> Optional[LearningPath]:
        """Get detailed information about a learning path."""
        return self.paths.get(path_id)
    
    def get_next_topic(
        self,
        path_id: str,
        current_progress: Dict[str, bool]
    ) -> Optional[Topic]:
        """
        Get next recommended topic based on progress.
        
        Args:
            path_id: Learning path ID
            current_progress: Dict of completed topic IDs
            
        Returns:
            Next topic to study
        """
        path = self.paths.get(path_id)
        if not path:
            return None
        
        for topic in path.topics:
            # Check if topic is already completed
            if current_progress.get(topic.id, False):
                continue
            
            # Check if prerequisites are met
            if self.check_prerequisites(topic.id, list(current_progress.keys())):
                return topic
        
        return None  # All topics completed
    
    def check_prerequisites(
        self,
        topic_id: str,
        completed_topics: List[str]
    ) -> bool:
        """
        Check if prerequisites are met for a topic.
        
        Args:
            topic_id: Topic ID to check
            completed_topics: List of completed topic IDs
            
        Returns:
            True if prerequisites are met
        """
        # Find the topic
        topic = None
        for path in self.paths.values():
            for t in path.topics:
                if t.id == topic_id:
                    topic = t
                    break
            if topic:
                break
        
        if not topic:
            return False
        
        # Check all prerequisites are completed
        for prereq in topic.prerequisites:
            if prereq not in completed_topics:
                return False
        
        return True
    
    def unlock_topic(self, path_id: str, topic_id: str) -> None:
        """Unlock a topic after prerequisites are met."""
        # In this implementation, topics are unlocked based on prerequisites
        # This method can be extended for additional unlock logic
        logger.info(f"Topic {topic_id} unlocked in path {path_id}")
    
    def _initialize_paths(self) -> Dict[str, LearningPath]:
        """Initialize predefined learning paths."""
        paths = {}
        
        # DSA Fundamentals Path
        paths["dsa"] = LearningPath(
            id="dsa",
            name="DSA Fundamentals",
            description="Master Data Structures and Algorithms",
            topics=[
                Topic(
                    id="dsa_arrays",
                    name="Arrays & Strings",
                    description="Learn array manipulation and string operations",
                    prerequisites=[],
                    resources=[],
                    quiz_id="dsa_arrays_quiz"
                ),
                Topic(
                    id="dsa_linked_lists",
                    name="Linked Lists",
                    description="Understand linked list operations",
                    prerequisites=["dsa_arrays"],
                    resources=[],
                    quiz_id="dsa_linked_lists_quiz"
                ),
                Topic(
                    id="dsa_stacks_queues",
                    name="Stacks & Queues",
                    description="Master stack and queue data structures",
                    prerequisites=["dsa_linked_lists"],
                    resources=[],
                    quiz_id="dsa_stacks_queues_quiz"
                ),
            ],
            estimated_hours=40
        )
        
        # Frontend Development Path
        paths["frontend"] = LearningPath(
            id="frontend",
            name="Frontend Development",
            description="Build beautiful user interfaces",
            topics=[
                Topic(
                    id="frontend_html_css",
                    name="HTML & CSS Basics",
                    description="Learn web page structure and styling",
                    prerequisites=[],
                    resources=[],
                    quiz_id="frontend_html_css_quiz"
                ),
                Topic(
                    id="frontend_javascript",
                    name="JavaScript Fundamentals",
                    description="Master JavaScript programming",
                    prerequisites=["frontend_html_css"],
                    resources=[],
                    quiz_id="frontend_javascript_quiz"
                ),
                Topic(
                    id="frontend_react",
                    name="React Basics",
                    description="Build interactive UIs with React",
                    prerequisites=["frontend_javascript"],
                    resources=[],
                    quiz_id="frontend_react_quiz"
                ),
            ],
            estimated_hours=45
        )
        
        # Backend Development Path
        paths["backend"] = LearningPath(
            id="backend",
            name="Backend Development",
            description="Build robust server-side applications",
            topics=[
                Topic(
                    id="backend_nodejs",
                    name="Node.js Basics",
                    description="Learn server-side JavaScript",
                    prerequisites=[],
                    resources=[],
                    quiz_id="backend_nodejs_quiz"
                ),
                Topic(
                    id="backend_express",
                    name="Express Framework",
                    description="Build APIs with Express",
                    prerequisites=["backend_nodejs"],
                    resources=[],
                    quiz_id="backend_express_quiz"
                ),
                Topic(
                    id="backend_databases",
                    name="Databases & MongoDB",
                    description="Work with databases",
                    prerequisites=["backend_express"],
                    resources=[],
                    quiz_id="backend_databases_quiz"
                ),
            ],
            estimated_hours=50
        )
        
        # AWS Services Path
        paths["aws"] = LearningPath(
            id="aws",
            name="AWS Services",
            description="Cloud computing with Amazon Web Services",
            topics=[
                Topic(
                    id="aws_basics",
                    name="AWS Fundamentals",
                    description="Introduction to AWS cloud",
                    prerequisites=[],
                    resources=[],
                    quiz_id="aws_basics_quiz"
                ),
                Topic(
                    id="aws_lambda",
                    name="AWS Lambda",
                    description="Serverless computing",
                    prerequisites=["aws_basics"],
                    resources=[],
                    quiz_id="aws_lambda_quiz"
                ),
                Topic(
                    id="aws_dynamodb",
                    name="DynamoDB",
                    description="NoSQL database service",
                    prerequisites=["aws_basics"],
                    resources=[],
                    quiz_id="aws_dynamodb_quiz"
                ),
            ],
            estimated_hours=60
        )
        
        # Full-Stack Development Path
        paths["fullstack"] = LearningPath(
            id="fullstack",
            name="Full-Stack Development",
            description="Complete web development mastery",
            topics=[
                Topic(
                    id="fullstack_frontend",
                    name="Frontend Mastery",
                    description="Advanced frontend development",
                    prerequisites=[],
                    resources=[],
                    quiz_id="fullstack_frontend_quiz"
                ),
                Topic(
                    id="fullstack_backend",
                    name="Backend Mastery",
                    description="Advanced backend development",
                    prerequisites=["fullstack_frontend"],
                    resources=[],
                    quiz_id="fullstack_backend_quiz"
                ),
                Topic(
                    id="fullstack_deployment",
                    name="Deployment & DevOps",
                    description="Deploy and maintain applications",
                    prerequisites=["fullstack_backend"],
                    resources=[],
                    quiz_id="fullstack_deployment_quiz"
                ),
            ],
            estimated_hours=80
        )
        
        return paths

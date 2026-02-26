"""Configuration management for CodeGuru India."""
import os
from dataclasses import dataclass
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AWSConfig:
    """AWS Bedrock configuration."""
    region: str
    bedrock_model_id: str
    max_tokens: int
    temperature: float


@dataclass
class AppConfig:
    """Application configuration."""
    supported_languages: List[str]
    max_file_size_mb: int
    max_repo_size_mb: int
    supported_extensions: List[str]
    session_timeout_days: int


def load_config() -> Tuple[AWSConfig, AppConfig]:
    """Load configuration from environment variables."""
    aws_config = AWSConfig(
        region=os.getenv("AWS_REGION", "us-east-1"),
        bedrock_model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-v2"),
        max_tokens=int(os.getenv("MAX_TOKENS", "2000")),
        temperature=float(os.getenv("TEMPERATURE", "0.7"))
    )
    
    app_config = AppConfig(
        supported_languages=["english", "hindi", "telugu"],
        max_file_size_mb=10,
        max_repo_size_mb=100,
        supported_extensions=[".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cpp", ".c", ".go", ".rb"],
        session_timeout_days=30
    )
    
    return aws_config, app_config

"""
Error Handling Utilities for Intent-Driven Repository Analysis.

Provides error handling, validation, and user-friendly error messages.
"""

import logging
import time
from typing import Dict, Any, Optional, Callable
from functools import wraps

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    """Base exception for analysis errors."""
    pass


class RepositoryError(AnalysisError):
    """Repository-related errors."""
    pass


class IntentError(AnalysisError):
    """Intent interpretation errors."""
    pass


class AnalysisTimeoutError(AnalysisError):
    """Analysis timeout errors."""
    pass


# Error message templates
ERROR_MESSAGES = {
    'invalid_github_url': {
        'title': 'Invalid GitHub URL',
        'message': 'The GitHub URL provided is not valid. Please use format: https://github.com/username/repository',
        'suggestion': 'Check the URL and try again'
    },
    'repository_too_large': {
        'title': 'Repository Too Large',
        'message': 'The repository exceeds the maximum size limit of {max_size_mb}MB',
        'suggestion': 'Try analyzing a smaller repository or specific folders'
    },
    'no_code_files': {
        'title': 'No Code Files Found',
        'message': 'No supported code files found in the repository',
        'suggestion': 'Ensure the repository contains Python, JavaScript, TypeScript, Java, C++, Go, or Ruby files'
    },
    'network_error': {
        'title': 'Network Error',
        'message': 'Failed to connect to GitHub. Please check your internet connection',
        'suggestion': 'Try again or upload a ZIP file instead'
    },
    'authentication_error': {
        'title': 'Authentication Failed',
        'message': 'GitHub authentication failed. The repository may be private',
        'suggestion': 'Use a public repository or provide authentication credentials'
    },
    'ai_service_unavailable': {
        'title': 'AI Service Unavailable',
        'message': 'The AI service is currently unavailable',
        'suggestion': 'Basic analysis will be provided. Try again later for full AI-powered features'
    },
    'analysis_failed': {
        'title': 'Analysis Failed',
        'message': 'Failed to analyze the repository: {error}',
        'suggestion': 'Check the repository structure and try again'
    },
    'invalid_intent': {
        'title': 'Invalid Intent',
        'message': 'Could not understand your learning goal',
        'suggestion': 'Please provide more details about what you want to learn'
    },
    'no_files_selected': {
        'title': 'No Files Selected',
        'message': 'No files matched your learning goal',
        'suggestion': 'Try a different learning goal or check the repository contents'
    }
}


def get_error_message(error_type: str, **kwargs) -> Dict[str, str]:
    """
    Get user-friendly error message.
    
    Args:
        error_type: Type of error
        **kwargs: Format parameters for message
        
    Returns:
        Dictionary with title, message, and suggestion
    """
    template = ERROR_MESSAGES.get(error_type, {
        'title': 'Error',
        'message': 'An unexpected error occurred',
        'suggestion': 'Please try again'
    })
    
    return {
        'title': template['title'],
        'message': template['message'].format(**kwargs),
        'suggestion': template['suggestion']
    }


def display_error(error_type: str, **kwargs) -> Dict[str, str]:
    """
    Display user-friendly error message.
    
    Args:
        error_type: Type of error
        **kwargs: Format parameters
        
    Returns:
        Error message dictionary
    """
    error_msg = get_error_message(error_type, **kwargs)
    logger.error(f"{error_msg['title']}: {error_msg['message']}")
    return error_msg


def validate_repository_upload(
    upload_type: str,
    upload_data: Any,
    max_size_mb: int = 100
) -> Dict[str, Any]:
    """
    Validate repository upload.
    
    Args:
        upload_type: Type of upload (github, zip, folder)
        upload_data: Upload data (URL, file, path)
        max_size_mb: Maximum size in MB
        
    Returns:
        Validation result with success flag and error if any
    """
    result = {'success': True, 'error': None}
    
    try:
        if upload_type == 'github':
            # Validate GitHub URL
            if not isinstance(upload_data, str):
                result['success'] = False
                result['error'] = display_error('invalid_github_url')
                return result
            
            url = upload_data.strip()
            if not url.startswith('https://github.com/'):
                result['success'] = False
                result['error'] = display_error('invalid_github_url')
                return result
            
            # Check URL format
            parts = url.replace('https://github.com/', '').split('/')
            if len(parts) < 2:
                result['success'] = False
                result['error'] = display_error('invalid_github_url')
                return result
        
        elif upload_type == 'zip':
            # Validate ZIP file
            if not upload_data:
                result['success'] = False
                result['error'] = display_error('no_code_files')
                return result
            
            # Check file size
            if hasattr(upload_data, 'size'):
                size_mb = upload_data.size / (1024 * 1024)
                if size_mb > max_size_mb:
                    result['success'] = False
                    result['error'] = display_error('repository_too_large', max_size_mb=max_size_mb)
                    return result
        
        elif upload_type == 'folder':
            # Validate folder path
            if not upload_data:
                result['success'] = False
                result['error'] = display_error('no_code_files')
                return result
    
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        result['success'] = False
        result['error'] = display_error('analysis_failed', error=str(e))
    
    return result


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0
):
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                        time.sleep(delay)
                        delay = min(delay * exponential_base, max_delay)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed")
            
            raise last_exception
        
        return wrapper
    return decorator


def validate_input(
    input_value: Any,
    input_type: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    required: bool = True
) -> Dict[str, Any]:
    """
    Validate user input.
    
    Args:
        input_value: Input value to validate
        input_type: Type of input (text, number, url, etc.)
        min_length: Minimum length for text
        max_length: Maximum length for text
        required: Whether input is required
        
    Returns:
        Validation result
    """
    result = {'valid': True, 'error': None}
    
    # Check required
    if required and not input_value:
        result['valid'] = False
        result['error'] = "This field is required"
        return result
    
    if not input_value and not required:
        return result
    
    # Type-specific validation
    if input_type == 'text':
        if not isinstance(input_value, str):
            result['valid'] = False
            result['error'] = "Must be text"
            return result
        
        if min_length and len(input_value) < min_length:
            result['valid'] = False
            result['error'] = f"Must be at least {min_length} characters"
            return result
        
        if max_length and len(input_value) > max_length:
            result['valid'] = False
            result['error'] = f"Must be at most {max_length} characters"
            return result
    
    elif input_type == 'url':
        if not isinstance(input_value, str):
            result['valid'] = False
            result['error'] = "Must be a valid URL"
            return result
        
        if not input_value.startswith(('http://', 'https://')):
            result['valid'] = False
            result['error'] = "Must start with http:// or https://"
            return result
    
    return result


def handle_ai_service_error(func: Callable):
    """
    Decorator to handle AI service errors gracefully.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"AI service error in {func.__name__}: {e}")
            # Return fallback result
            return None
    
    return wrapper

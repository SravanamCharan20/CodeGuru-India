"""AWS Bedrock client for LLM interactions."""
import boto3
import json
import time
from typing import Dict, Iterator, Optional
from config import AWSConfig
import logging

logger = logging.getLogger(__name__)


class BedrockClient:
    """Handles AWS Bedrock API interactions with retry logic."""
    
    def __init__(self, config: AWSConfig):
        """Initialize AWS Bedrock client."""
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize boto3 Bedrock client."""
        try:
            self.client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.config.region
            )
            logger.info(f"Bedrock client initialized for region: {self.config.region}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            # Client will be None, methods will handle gracefully
    
    def invoke_model(
        self, 
        prompt: str, 
        model_id: Optional[str] = None,
        parameters: Optional[Dict] = None
    ) -> str:
        """
        Invoke Bedrock model and return response.
        
        Args:
            prompt: The input prompt for the model
            model_id: Model ID to use (defaults to config)
            parameters: Additional model parameters
            
        Returns:
            Model response as string
        """
        if not self.client:
            logger.warning("Bedrock client not initialized, returning mock response")
            return self._get_mock_response(prompt)
        
        model_id = model_id or self.config.bedrock_model_id
        parameters = parameters or {}
        
        # Merge with default parameters
        model_params = {
            "max_tokens": parameters.get("max_tokens", self.config.max_tokens),
            "temperature": parameters.get("temperature", self.config.temperature),
            "top_p": parameters.get("top_p", 0.9),
        }
        
        # Prepare request body based on model
        if "anthropic" in model_id.lower():
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": model_params["max_tokens"],
                "temperature": model_params["temperature"],
                "top_p": model_params["top_p"],
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        elif "llama" in model_id.lower() or "meta" in model_id.lower():
            # Meta Llama format
            body = {
                "prompt": prompt,
                "max_gen_len": model_params["max_tokens"],
                "temperature": model_params["temperature"],
                "top_p": model_params["top_p"]
            }
        elif "titan" in model_id.lower():
            # Amazon Titan format
            body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": model_params["max_tokens"],
                    "temperature": model_params["temperature"],
                    "topP": model_params["top_p"]
                }
            }
        else:
            # Generic format for other models
            body = {
                "prompt": prompt,
                "max_tokens": model_params["max_tokens"],
                "temperature": model_params["temperature"],
                "top_p": model_params["top_p"]
            }
        
        # Invoke with retry logic
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = self.client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body)
                )
                
                response_body = json.loads(response['body'].read())
                
                # Extract response based on model type
                if "anthropic" in model_id.lower():
                    return response_body['content'][0]['text']
                elif "llama" in model_id.lower() or "meta" in model_id.lower():
                    return response_body.get('generation', response_body.get('text', ''))
                elif "titan" in model_id.lower():
                    return response_body['results'][0]['outputText']
                else:
                    return response_body.get('completion', response_body.get('text', ''))
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    logger.error(f"All retry attempts failed: {e}")
                    return self._get_mock_response(prompt)
        
        return self._get_mock_response(prompt)
    
    def invoke_model_with_streaming(
        self,
        prompt: str,
        model_id: Optional[str] = None,
        parameters: Optional[Dict] = None
    ) -> Iterator[str]:
        """
        Invoke model with streaming response.
        
        Args:
            prompt: The input prompt for the model
            model_id: Model ID to use (defaults to config)
            parameters: Additional model parameters
            
        Yields:
            Response chunks as they arrive
        """
        if not self.client:
            logger.warning("Bedrock client not initialized, returning mock stream")
            yield self._get_mock_response(prompt)
            return
        
        model_id = model_id or self.config.bedrock_model_id
        parameters = parameters or {}
        
        # Prepare request body
        model_params = {
            "max_tokens": parameters.get("max_tokens", self.config.max_tokens),
            "temperature": parameters.get("temperature", self.config.temperature),
            "top_p": parameters.get("top_p", 0.9),
        }
        
        if "anthropic" in model_id.lower():
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": model_params["max_tokens"],
                "temperature": model_params["temperature"],
                "top_p": model_params["top_p"],
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        else:
            body = {
                "prompt": prompt,
                **model_params
            }
        
        try:
            response = self.client.invoke_model_with_response_stream(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            stream = response.get('body')
            if stream:
                for event in stream:
                    chunk = event.get('chunk')
                    if chunk:
                        chunk_data = json.loads(chunk.get('bytes').decode())
                        
                        if "anthropic" in model_id.lower():
                            if chunk_data.get('type') == 'content_block_delta':
                                yield chunk_data['delta']['text']
                        else:
                            yield chunk_data.get('completion', chunk_data.get('text', ''))
        
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield self._get_mock_response(prompt)
    
    def _get_mock_response(self, prompt: str) -> str:
        """Generate mock response when Bedrock is unavailable."""
        return f"""This is a mock response for development purposes.

Your prompt was: {prompt[:100]}...

In production, this would be replaced with actual AWS Bedrock responses.
Configure your AWS credentials in the .env file to enable real AI responses."""

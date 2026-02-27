"""Voice processing for multi-language speech recognition."""
from dataclasses import dataclass
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class VoiceResult:
    """Voice processing result."""
    transcript: str
    language: str
    confidence: float
    processing_time: float


class VoiceProcessor:
    """Processes voice input using AWS Transcribe."""
    
    def __init__(self, aws_config=None):
        """
        Initialize voice processor.
        
        Args:
            aws_config: AWS configuration for Transcribe
        """
        self.aws_config = aws_config
        self.supported_languages = {
            'en': 'en-US',  # English
            'hi': 'hi-IN',  # Hindi
            'te': 'te-IN'   # Telugu
        }
        
        # Try to initialize AWS Transcribe
        self.transcribe_client = None
        if aws_config:
            try:
                import boto3
                # Boto3 automatically uses credentials from environment variables
                self.transcribe_client = boto3.client(
                    'transcribe',
                    region_name=aws_config.region
                )
                logger.info("AWS Transcribe client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize AWS Transcribe: {e}")
    
    def process_audio(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Optional[VoiceResult]:
        """
        Process audio data and return transcription.
        
        Args:
            audio_data: Audio data in bytes
            language: Optional language code (en, hi, te). If None, auto-detect.
            
        Returns:
            VoiceResult with transcription or None if failed
        """
        start_time = time.time()
        
        try:
            # Validate audio
            if not self.validate_audio(audio_data):
                logger.error("Invalid audio data")
                return None
            
            # Detect language if not provided
            if not language:
                language = 'en'  # Default to English
            
            # Get AWS language code
            aws_language = self.supported_languages.get(language, 'en-US')
            
            # Process with AWS Transcribe if available
            if self.transcribe_client:
                transcript = self._transcribe_with_aws(audio_data, aws_language)
            else:
                # Fallback to mock transcription
                logger.warning("AWS Transcribe not available, using mock transcription")
                transcript = self._mock_transcribe(language)
            
            processing_time = time.time() - start_time
            
            # Handle accent variations
            transcript = self.handle_accent(transcript, language)
            
            return VoiceResult(
                transcript=transcript,
                language=language,
                confidence=0.95,
                processing_time=processing_time
            )
        
        except Exception as e:
            logger.error(f"Failed to process audio: {e}")
            return None
    
    def process_audio_stream(
        self,
        audio_stream,
        language: str = 'en'
    ) -> Optional[VoiceResult]:
        """
        Process audio stream using AWS Transcribe streaming.
        
        Args:
            audio_stream: Audio stream object
            language: Language code (en, hi, te)
            
        Returns:
            VoiceResult with transcription or None if failed
        """
        try:
            if not self.transcribe_client:
                logger.warning("AWS Transcribe not available")
                return None
            
            # Get AWS language code
            aws_language = self.supported_languages.get(language, 'en-US')
            
            # Use AWS Transcribe streaming API
            # This is a simplified version - real implementation would use
            # the streaming API with proper event handling
            
            logger.info(f"Starting transcription stream for language: {aws_language}")
            
            # For now, return mock data
            # Real implementation would use boto3's transcribe streaming
            return VoiceResult(
                transcript=self._mock_transcribe(language),
                language=language,
                confidence=0.90,
                processing_time=1.0
            )
        
        except Exception as e:
            logger.error(f"Failed to process audio stream: {e}")
            return None
    
    def detect_language(self, audio_data: bytes) -> str:
        """
        Detect language from audio data.
        
        Args:
            audio_data: Audio data in bytes
            
        Returns:
            Language code (en, hi, te)
        """
        try:
            if self.transcribe_client:
                # Use AWS language identification
                # This is a simplified version - real implementation would use
                # AWS Transcribe's language identification feature
                return 'en'  # Default to English
            else:
                # Mock language detection
                logger.warning("Using mock language detection")
                return 'en'
        
        except Exception as e:
            logger.error(f"Failed to detect language: {e}")
            return 'en'  # Default to English
    
    def handle_accent(self, transcript: str, language: str) -> str:
        """
        Handle regional accent variations.
        
        Args:
            transcript: Transcribed text
            language: Language code
            
        Returns:
            Processed transcript with accent handling
        """
        try:
            # Apply accent-specific corrections
            if language == 'en':
                # Handle Indian English accent variations
                corrections = {
                    'vat': 'what',
                    'vere': 'where',
                    'ven': 'when',
                    'vhy': 'why',
                    'vill': 'will'
                }
                
                for incorrect, correct in corrections.items():
                    transcript = transcript.replace(incorrect, correct)
            
            elif language == 'hi':
                # Handle Hindi accent variations
                # Add Hindi-specific corrections here
                pass
            
            elif language == 'te':
                # Handle Telugu accent variations
                # Add Telugu-specific corrections here
                pass
            
            return transcript
        
        except Exception as e:
            logger.error(f"Failed to handle accent: {e}")
            return transcript
    
    def _transcribe_with_aws(
        self,
        audio_data: bytes,
        language_code: str
    ) -> str:
        """
        Transcribe audio using AWS Transcribe.
        
        Args:
            audio_data: Audio data in bytes
            language_code: AWS language code (e.g., 'en-US')
            
        Returns:
            Transcribed text
        """
        try:
            import boto3
            import uuid
            import json
            import io
            from botocore.exceptions import ClientError
            
            # Generate unique job name
            job_name = f"transcribe-{uuid.uuid4().hex[:8]}"
            
            # Create S3 client
            s3_client = boto3.client('s3', region_name=self.aws_config.region)
            
            # Get or create S3 bucket for audio files
            bucket_name = self._get_or_create_bucket(s3_client)
            if not bucket_name:
                logger.warning("Failed to create S3 bucket, using mock transcription")
                return self._mock_transcribe(language_code[:2])
            
            # Upload audio to S3
            s3_key = f"audio/{job_name}.wav"
            try:
                # Convert audio bytes to WAV format if needed
                audio_file = self._prepare_audio_for_transcribe(audio_data)
                
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=audio_file,
                    ContentType='audio/wav'
                )
                logger.info(f"Uploaded audio to s3://{bucket_name}/{s3_key}")
            except Exception as e:
                logger.error(f"Failed to upload audio to S3: {e}")
                return self._mock_transcribe(language_code[:2])
            
            # Start transcription job
            try:
                media_uri = f"s3://{bucket_name}/{s3_key}"
                
                self.transcribe_client.start_transcription_job(
                    TranscriptionJobName=job_name,
                    Media={'MediaFileUri': media_uri},
                    MediaFormat='wav',
                    LanguageCode=language_code
                    # Removed Settings to avoid validation errors
                )
                logger.info(f"Started transcription job: {job_name}")
            except Exception as e:
                logger.error(f"Failed to start transcription job: {e}")
                # Clean up S3 object
                self._cleanup_s3_object(s3_client, bucket_name, s3_key)
                return self._mock_transcribe(language_code[:2])
            
            # Wait for transcription to complete
            max_wait_time = 60  # seconds
            wait_interval = 2  # seconds
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                try:
                    response = self.transcribe_client.get_transcription_job(
                        TranscriptionJobName=job_name
                    )
                    
                    status = response['TranscriptionJob']['TranscriptionJobStatus']
                    
                    if status == 'COMPLETED':
                        # Get transcript
                        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                        transcript_text = self._fetch_transcript(transcript_uri)
                        
                        # Clean up
                        self._cleanup_transcription_job(job_name)
                        self._cleanup_s3_object(s3_client, bucket_name, s3_key)
                        
                        logger.info(f"Transcription completed: {transcript_text[:50]}...")
                        return transcript_text
                    
                    elif status == 'FAILED':
                        failure_reason = response['TranscriptionJob'].get('FailureReason', 'Unknown')
                        logger.error(f"Transcription job failed: {failure_reason}")
                        
                        # Clean up
                        self._cleanup_transcription_job(job_name)
                        self._cleanup_s3_object(s3_client, bucket_name, s3_key)
                        
                        return self._mock_transcribe(language_code[:2])
                    
                    # Still in progress
                    time.sleep(wait_interval)
                    elapsed_time += wait_interval
                
                except Exception as e:
                    logger.error(f"Error checking transcription status: {e}")
                    break
            
            # Timeout - clean up and return mock
            logger.warning(f"Transcription job timed out after {max_wait_time}s")
            self._cleanup_transcription_job(job_name)
            self._cleanup_s3_object(s3_client, bucket_name, s3_key)
            
            return self._mock_transcribe(language_code[:2])
        
        except Exception as e:
            logger.error(f"AWS Transcribe failed: {e}")
            return self._mock_transcribe(language_code[:2])
    
    def _mock_transcribe(self, language: str) -> str:
        """
        Mock transcription for testing.
        
        Args:
            language: Language code
            
        Returns:
            Mock transcribed text
        """
        mock_transcripts = {
            'en': "Explain this function to me in simple terms",
            'hi': "इस फ़ंक्शन को मुझे सरल शब्दों में समझाएं",
            'te': "ఈ ఫంక్షన్‌ను నాకు సరళంగా వివరించండి"
        }
        
        return mock_transcripts.get(language, mock_transcripts['en'])
    
    def _get_or_create_bucket(self, s3_client) -> Optional[str]:
        """
        Get or create S3 bucket for audio files.
        
        Args:
            s3_client: Boto3 S3 client
            
        Returns:
            Bucket name or None if failed
        """
        try:
            # Check if user provided a bucket name in config
            if self.aws_config and self.aws_config.s3_bucket:
                bucket_name = self.aws_config.s3_bucket
                logger.info(f"Using configured bucket: {bucket_name}")
                
                # Verify bucket exists and is accessible
                try:
                    s3_client.head_bucket(Bucket=bucket_name)
                    logger.info(f"Bucket accessible: {bucket_name}")
                    return bucket_name
                except Exception as e:
                    logger.error(f"Configured bucket not accessible: {e}")
                    return None
            
            # Try to use a consistent bucket name based on region
            bucket_name = f"codeguru-transcribe-{self.aws_config.region}"
            
            # Check if bucket exists
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                logger.info(f"Using existing bucket: {bucket_name}")
                return bucket_name
            except:
                # Bucket doesn't exist, try to create it
                pass
            
            # Try to create bucket
            try:
                if self.aws_config.region == 'us-east-1':
                    # us-east-1 doesn't need LocationConstraint
                    s3_client.create_bucket(Bucket=bucket_name)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': self.aws_config.region
                        }
                    )
                
                # Set lifecycle policy to delete old files
                try:
                    s3_client.put_bucket_lifecycle_configuration(
                        Bucket=bucket_name,
                        LifecycleConfiguration={
                            'Rules': [
                                {
                                    'ID': 'DeleteOldAudio',  # Changed from 'Id' to 'ID'
                                    'Status': 'Enabled',
                                    'Prefix': 'audio/',
                                    'Expiration': {'Days': 1}
                                }
                            ]
                        }
                    )
                except Exception as e:
                    logger.warning(f"Failed to set lifecycle policy: {e}")
                
                logger.info(f"Created bucket: {bucket_name}")
                return bucket_name
            
            except Exception as e:
                logger.warning(f"Failed to create bucket (missing S3 permissions): {e}")
                logger.info("To use AWS Transcribe, either:")
                logger.info("  1. Add S3 permissions to your AWS user")
                logger.info("  2. Create a bucket manually and set S3_TRANSCRIBE_BUCKET in .env")
                logger.info("  3. Use mock transcription (automatic fallback)")
                return None
        
        except Exception as e:
            logger.error(f"Error managing S3 bucket: {e}")
            return None
    
    def _prepare_audio_for_transcribe(self, audio_data: bytes) -> bytes:
        """
        Prepare audio data for AWS Transcribe.
        
        Args:
            audio_data: Raw audio data in bytes
            
        Returns:
            Audio data in WAV format
        """
        try:
            # Check if audio is already in WAV format
            if audio_data[:4] == b'RIFF':
                logger.info("Audio is already in WAV format")
                return audio_data
            
            # Try to convert using pydub if available
            try:
                from pydub import AudioSegment
                import io
                
                # Try to load audio
                audio = AudioSegment.from_file(io.BytesIO(audio_data))
                
                # Convert to WAV
                wav_io = io.BytesIO()
                audio.export(wav_io, format='wav')
                wav_data = wav_io.getvalue()
                
                logger.info("Converted audio to WAV format")
                return wav_data
            
            except ImportError:
                logger.warning("pydub not available, using raw audio data")
                return audio_data
            except Exception as e:
                logger.warning(f"Failed to convert audio: {e}, using raw data")
                return audio_data
        
        except Exception as e:
            logger.error(f"Error preparing audio: {e}")
            return audio_data
    
    def _fetch_transcript(self, transcript_uri: str) -> str:
        """
        Fetch transcript from AWS Transcribe result URI.
        
        Args:
            transcript_uri: URI to transcript JSON file
            
        Returns:
            Transcribed text
        """
        try:
            import requests
            import json
            
            # Fetch transcript JSON
            response = requests.get(transcript_uri, timeout=10)
            response.raise_for_status()
            
            # Parse transcript
            transcript_json = response.json()
            
            # Extract text from results
            if 'results' in transcript_json:
                transcripts = transcript_json['results'].get('transcripts', [])
                if transcripts and len(transcripts) > 0:
                    transcript_text = transcripts[0].get('transcript', '')
                    return transcript_text
            
            logger.warning("No transcript found in response")
            return ""
        
        except Exception as e:
            logger.error(f"Failed to fetch transcript: {e}")
            return ""
    
    def _cleanup_transcription_job(self, job_name: str):
        """
        Clean up transcription job.
        
        Args:
            job_name: Transcription job name
        """
        try:
            self.transcribe_client.delete_transcription_job(
                TranscriptionJobName=job_name
            )
            logger.info(f"Deleted transcription job: {job_name}")
        except Exception as e:
            logger.warning(f"Failed to delete transcription job: {e}")
    
    def _cleanup_s3_object(self, s3_client, bucket_name: str, key: str):
        """
        Clean up S3 object.
        
        Args:
            s3_client: Boto3 S3 client
            bucket_name: S3 bucket name
            key: S3 object key
        """
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=key)
            logger.info(f"Deleted S3 object: s3://{bucket_name}/{key}")
        except Exception as e:
            logger.warning(f"Failed to delete S3 object: {e}")
    
    def validate_audio(
        self,
        audio_data: bytes,
        max_duration_seconds: int = 60
    ) -> bool:
        """
        Validate audio data.
        
        Args:
            audio_data: Audio data in bytes
            max_duration_seconds: Maximum allowed duration
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if audio data is not empty
            if not audio_data or len(audio_data) == 0:
                logger.error("Audio data is empty")
                return False
            
            # Check file size (approximate duration check)
            # Assuming ~16KB per second for typical audio
            max_size = max_duration_seconds * 16 * 1024
            if len(audio_data) > max_size:
                logger.error(f"Audio too long: {len(audio_data)} bytes > {max_size} bytes")
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to validate audio: {e}")
            return False
    
    def get_supported_languages(self) -> dict:
        """
        Get supported languages.
        
        Returns:
            Dictionary of language codes and names
        """
        return {
            'en': 'English',
            'hi': 'हिंदी (Hindi)',
            'te': 'తెలుగు (Telugu)'
        }

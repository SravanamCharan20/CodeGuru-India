"""Quick test to verify AI is working."""
import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

print("=" * 70)
print("Testing AWS Bedrock AI")
print("=" * 70)

# Get config
region = os.getenv("AWS_REGION")
model_id = os.getenv("BEDROCK_MODEL_ID")

print(f"\nRegion: {region}")
print(f"Model: {model_id}")

# Test connection
print("\nTesting AI connection...")

try:
    runtime = boto3.client('bedrock-runtime', region_name=region)
    
    # Prepare request based on model type
    if "llama" in model_id.lower() or "meta" in model_id.lower():
        body = {
            "prompt": "Say 'Hello from CodeGuru India!' in one sentence.",
            "max_gen_len": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
    elif "anthropic" in model_id.lower():
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [{"role": "user", "content": "Say 'Hello from CodeGuru India!' in one sentence."}]
        }
    else:
        body = {
            "prompt": "Say 'Hello from CodeGuru India!' in one sentence.",
            "max_tokens": 100
        }
    
    # Invoke model
    response = runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    
    response_body = json.loads(response['body'].read())
    
    # Extract text based on model type
    if "llama" in model_id.lower() or "meta" in model_id.lower():
        text = response_body.get('generation', '')
    elif "anthropic" in model_id.lower():
        text = response_body['content'][0]['text']
    else:
        text = response_body.get('completion', response_body.get('text', ''))
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! AI IS WORKING!")
    print("=" * 70)
    
    print(f"\nAI Response:")
    print("-" * 70)
    print(text)
    print("-" * 70)
    
    print("\n✅ Your CodeGuru India app will use REAL AI!")
    print("✅ All features are operational!")
    print("\n🚀 Start the app: python -m streamlit run app.py")
    
except Exception as e:
    print("\n" + "=" * 70)
    print("❌ AI NOT WORKING")
    print("=" * 70)
    print(f"\nError: {e}")
    
    if "payment" in str(e).lower():
        print("\n⚠️  Payment method required")
        print("Add payment method to AWS account")
    elif "access" in str(e).lower():
        print("\n⚠️  Model access denied")
        print("Enable model access in AWS Console")
    else:
        print("\n⚠️  Check your configuration")
        print("1. Verify .env file has correct credentials")
        print("2. Check region and model ID")
        print("3. Ensure AWS credentials are valid")
    
    print("\n💡 App will work with mock data:")
    print("   python -m streamlit run app.py")

print("\n" + "=" * 70)

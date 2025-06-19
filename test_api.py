import requests
import json

# Correct JSON format - notice how special characters are properly escaped
test_payload = {
    "prompt": "How does the `__init__()` method in comet.py utilize `_get_rank()` from rank_zero.py to determine process hierarchy?",
    "model_1": "I'll analyze how CometLogger uses rank detection for distributed training.\n\nBased on my analysis, here's how CometLogger uses `_get_rank()` for distributed training:\n\n## How `_get_rank()` Works\n\nThe `_get_rank()` function determines the process rank by checking environment variables in a specific order:\n\n```python\ndef _get_rank() -> Optional[int]:\n    rank_keys = (\"RANK\", \"LOCAL_RANK\", \"SLURM_PROCID\", \"JSM_NAMESPACE_RANK\")\n    for key in rank_keys:\n        rank = os.environ.get(key)\n        if rank is not None:\n            return int(rank)\n    return None\n```",
    "model_2": "The function `_get_rank()` in `src/lightning/fabric/utilities/rank_zero.py` is responsible for determining the rank of the current process in a distributed setup.\n\nIt checks for environment variables in this order: `RANK`, `LOCAL_RANK`, `SLURM_PROCID`, and `JSM_NAMESPACE_RANK`.\n\nThe CometLogger uses this to ensure only rank 0 creates experiments.",
    "model_3": "The CometLogger class uses `_get_rank()` to manage process hierarchy and experiment creation in distributed environments.\n\nThe key logic is:\n```python\nif _get_rank() is not None and _get_rank() != 0:\n    return\n```\n\nThis ensures only the main process (rank 0) creates the experiment.",
    "use_knowledge": False
}

# Test payload with knowledge enabled
test_payload_with_knowledge = test_payload.copy()
test_payload_with_knowledge["use_knowledge"] = True

def test_knowledge_status():
    """Test the knowledge base status endpoint."""
    try:
        response = requests.get("http://localhost:8000/knowledge-status")
        if response.status_code == 200:
            print("✅ Knowledge status check passed")
            result = response.json()
            print(f"Status: {result['status']}")
            if 'pdf_files' in result:
                print(f"PDF files found: {result['pdf_files']}")
        else:
            print(f"❌ Knowledge status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Knowledge status error: {e}")

def test_load_knowledge():
    """Test loading the knowledge base."""
    try:
        response = requests.post("http://localhost:8000/load-knowledge", params={"recreate": False})
        if response.status_code == 200:
            print("✅ Knowledge base loaded successfully")
            result = response.json()
            print(f"Message: {result['message']}")
        else:
            print(f"❌ Knowledge loading failed: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Knowledge loading error: {e}")

def test_api():
    """Test the API without knowledge."""
    url = "http://localhost:8000/evaluate"
    
    try:
        # Test the API
        response = requests.post(url, json=test_payload)
        
        if response.status_code == 200:
            print("✅ Basic API test successful!")
            result = response.json()
            print(f"Status: {result['status']}")
            print(f"Analysis length: {len(result['analysis'])} characters")
            print(f"Metadata: {result['metadata']}")
            print("\n--- Analysis Preview ---")
            print(result['analysis'][:500] + "..." if len(result['analysis']) > 500 else result['analysis'])
        else:
            print(f"❌ Error {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_with_knowledge():
    """Test the API with knowledge base enabled."""
    url = "http://localhost:8000/evaluate"
    
    try:
        # Test the API with knowledge
        response = requests.post(url, json=test_payload_with_knowledge)
        
        if response.status_code == 200:
            print("✅ Knowledge-enhanced API test successful!")
            result = response.json()
            print(f"Status: {result['status']}")
            print(f"Analysis length: {len(result['analysis'])} characters")
            print(f"Knowledge used: {result['metadata']['knowledge_used']}")
            print(f"Session ID: {result['metadata'].get('session_id', 'N/A')}")
            print("\n--- Knowledge-Enhanced Analysis Preview ---")
            print(result['analysis'][:500] + "..." if len(result['analysis']) > 500 else result['analysis'])
        else:
            print(f"❌ Knowledge API Error {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health():
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(response.json())
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_root_info():
    """Test the root endpoint to see available features."""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint check passed")
            result = response.json()
            print(f"Available endpoints: {result['endpoints']}")
            print(f"Features: {result['features']}")
        else:
            print(f"❌ Root endpoint check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")

if __name__ == "__main__":
    print("🚀 Testing Enhanced Hustle Buddy API with Knowledge Base...")
    
    print("\n1. Root Info:")
    test_root_info()
    
    print("\n2. Health Check:")
    test_health()
    
    print("\n3. Knowledge Status:")
    test_knowledge_status()
    
    print("\n4. Load Knowledge Base:")
    test_load_knowledge()
    
    print("\n5. Basic API Test (without knowledge):")
    test_api()
    
    print("\n6. Knowledge-Enhanced API Test:")
    test_api_with_knowledge()
    
    print("\n7. Example of properly formatted JSON:")
    print("Without knowledge:")
    print(json.dumps(test_payload, indent=2))
    print("\nWith knowledge:")
    print(json.dumps(test_payload_with_knowledge, indent=2)) 
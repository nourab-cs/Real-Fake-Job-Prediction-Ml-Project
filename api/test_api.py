"""
Test script for the Fake Job Posting Detection API
"""
import requests
import json

# API endpoint
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("Testing Health Endpoint")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    

def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*50)
    print("Testing Model Info Endpoint")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_real_job():
    """Test with a likely real job posting"""
    print("\n" + "="*50)
    print("Testing REAL Job Posting")
    print("="*50)
    
    data = {
        "title": "Senior Software Engineer",
        "company_profile": "Google is a leading technology company known for search, cloud computing, and innovation.",
        "description": """We are looking for a Senior Software Engineer to join our team. 
        You will work on large-scale distributed systems and contribute to products used by millions.
        The ideal candidate has strong problem-solving skills and experience with modern tech stacks.""",
        "requirements": """
        - Bachelor's degree in Computer Science or related field
        - 5+ years of software development experience
        - Strong knowledge of Python, Java, or C++
        - Experience with cloud platforms (GCP, AWS)
        - Excellent communication and teamwork skills
        """,
        "benefits": "Competitive salary, health insurance, 401k matching, stock options, remote work flexibility",
        "employment_type": "Full-time",
        "required_experience": "Mid-Senior level",
        "required_education": "Bachelor's Degree",
        "industry": "Information Technology",
        "function": "Engineering",
        "telecommuting": 1,
        "has_company_logo": 1,
        "has_questions": 1
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_fake_job():
    """Test with a likely fake job posting"""
    print("\n" + "="*50)
    print("Testing FAKE Job Posting")
    print("="*50)
    
    data = {
        "title": "WORK FROM HOME - EARN $5000/WEEK!!!",
        "company_profile": "",
        "description": """AMAZING OPPORTUNITY!!! Make thousands of dollars per week from the comfort of your home! 
        No experience needed! No interviews! Just send us $99 for training materials and start earning TODAY!!!
        Limited spots available! ACT NOW!!!""",
        "requirements": "Just need a computer and internet connection! Anyone can do this!",
        "benefits": "UNLIMITED INCOME POTENTIAL!!! Be your own boss! Work whenever you want!!!",
        "employment_type": "Other",
        "required_experience": "Entry level",
        "required_education": "Unspecified",
        "industry": "Other",
        "function": "Other",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_minimal_input():
    """Test with minimal required fields"""
    print("\n" + "="*50)
    print("Testing Minimal Input")
    print("="*50)
    
    data = {
        "title": "Data Analyst",
        "description": "Looking for a data analyst to join our team and help with business intelligence."
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Fake Job Posting Detection API - Test Suite")
    print("="*50)
    print(f"Testing API at: {BASE_URL}")
    
    try:
        # Run all tests
        test_health()
        test_model_info()
        test_real_job()
        test_fake_job()
        test_minimal_input()
        
        print("\n" + "="*50)
        print("✅ All tests completed!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API.")
        print("Make sure the API is running:")
        print("  cd api")
        print("  uvicorn app:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

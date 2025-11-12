import requests
import json

def fetch_daily_quote():
    """
    Fetches quote from ZenQuotes API
    Returns: dict with 'text' and 'author' or None if failed
    """
    api_url = "https://zenquotes.io/api/today"
    
    print(f"Fetching quote from: {api_url}")
    print()
    
    try:
        # Make request with timeout
        response = requests.get(api_url, timeout=10)
        
        print(f"Response status code: {response.status_code}")
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"✗ API returned error status code: {response.status_code}")
            return None
        
        # Parse JSON response
        data = response.json()
        
        print(f"Raw response: {json.dumps(data, indent=2)}")
        print()
        
        # Validate response structure
        if not data or not isinstance(data, list) or len(data) == 0:
            print("✗ Malformed API response - expected a non-empty list")
            return None
        
        quote_data = data[0]
        
        # Extract quote and author
        quote = {
            'text': quote_data.get('q', ''),
            'author': quote_data.get('a', 'Unknown')
        }
        
        # Validate we got actual content
        if not quote['text']:
            print("✗ Empty quote received")
            return None
        
        print("✓ Successfully fetched quote!")
        return quote
        
    except requests.exceptions.Timeout:
        print("✗ API request timed out (took longer than 10 seconds)")
        return None
    
    except requests.exceptions.ConnectionError:
        print("✗ Failed to connect to API - check your internet connection")
        return None
    
    except json.JSONDecodeError:
        print("✗ API returned invalid JSON")
        print(f"Response text: {response.text}")
        return None
    
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return None


def test_edge_cases():
    """Test various edge cases"""
    print("=" * 60)
    print("Testing Edge Cases")
    print("=" * 60)
    print()
    
    # Test 1: Invalid URL (should handle connection error)
    print("Test 1: Testing with invalid URL...")
    try:
        response = requests.get("https://invalid-url-that-does-not-exist.com", timeout=5)
    except requests.exceptions.ConnectionError:
        print("✓ Correctly handled connection error")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    print()
    
    # Test 2: Timeout (using a URL known to be slow)
    print("Test 2: Testing timeout handling...")
    try:
        response = requests.get("https://httpstat.us/200?sleep=15000", timeout=2)
    except requests.exceptions.Timeout:
        print("✓ Correctly handled timeout")
    except Exception as e:
        print(f"Note: {e}")
    print()
    
    print("Edge case testing complete!")
    print()
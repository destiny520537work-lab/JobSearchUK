"""
Debug script to diagnose HTML parsing issues
"""

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json

def debug_search():
    """Debug the search API response"""

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    params = {
        "keywords": "Data Analyst",
        "location": "United Kingdom",
        "geoId": "101165590",
        "f_TPR": "r86400",
        "f_E": "1,2",
        "start": 0,
    }

    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{urlencode(params)}"

    print("=" * 70)
    print("🔍 LinkedIn Search API Debug")
    print("=" * 70)
    print(f"\n📌 URL: {url}\n")
    print(f"📌 User-Agent: {headers['User-Agent']}\n")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ Response Status: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} characters\n")

        if response.status_code == 200:
            print("=" * 70)
            print("📄 Response HTML (first 2000 characters):")
            print("=" * 70)
            print(response.text[:2000])
            print("\n...\n")

            # Try parsing
            soup = BeautifulSoup(response.text, "html.parser")

            # Check for different selectors
            print("\n" + "=" * 70)
            print("🔎 HTML Structure Analysis:")
            print("=" * 70)

            # Look for job cards - try multiple selectors
            selectors = [
                ("li", {}),
                ("div", {"class": "job-search-card"}),
                ("div", {"class": "base-search-card"}),
                ("article", {}),
                ("h3", {"class": "base-search-card__title"}),
            ]

            for tag, attrs in selectors:
                elements = soup.find_all(tag, attrs)
                print(f"\n✓ <{tag}> tags with {attrs}: {len(elements)} found")
                if len(elements) > 0 and len(elements) <= 3:
                    for i, elem in enumerate(elements[:3]):
                        print(f"  [{i}] {str(elem)[:100]}...")

            # Check for error messages
            if "error" in response.text.lower() or "no jobs" in response.text.lower():
                print("\n⚠️  Error or 'no jobs' message detected in response")

            # Save full HTML to file for inspection
            with open("response_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("\n💾 Full HTML saved to: response_debug.html")

        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def debug_detail_page():
    """Debug job detail page"""

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Use a real job ID (example)
    job_id = "3891899163"
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

    print("\n" + "=" * 70)
    print("🔍 LinkedIn Job Detail API Debug")
    print("=" * 70)
    print(f"\n📌 URL: {url}\n")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ Response Status: {response.status_code}")
        print(f"📏 Response Length: {len(response.text)} characters\n")

        if response.status_code == 200:
            print("=" * 70)
            print("📄 Response HTML (first 1500 characters):")
            print("=" * 70)
            print(response.text[:1500])

            # Save to file
            with open("response_detail_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("\n💾 Full HTML saved to: response_detail_debug.html")
        else:
            print(f"❌ Error: HTTP {response.status_code}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("\n🚀 Running debug diagnostics...\n")
    debug_search()
    # Uncomment to debug detail page:
    # debug_detail_page()

    print("\n" + "=" * 70)
    print("✅ Debug complete!")
    print("=" * 70)
    print("\n💡 Check response_debug.html in your browser to see the actual HTML structure")
    print("   This will help identify how LinkedIn's HTML has changed.\n")

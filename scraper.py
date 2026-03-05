"""
LinkedIn UK Job Scraper - Main Program

Scrapes job listings from LinkedIn Guest API for UK positions
"""

import sys
import time
import random
import argparse
from datetime import datetime
from urllib.parse import urlencode

import requests
from tqdm import tqdm
from fake_useragent import UserAgent

from config import (
    SEARCH_KEYWORDS,
    BASE_SEARCH_URL,
    BASE_DETAIL_URL,
    LOCATION,
    GEO_ID,
    TIME_FILTER,
    EXPERIENCE_LEVEL,
    PAGE_SIZE,
    MIN_DELAY,
    MAX_DELAY,
    MAX_RETRIES,
    RETRY_DELAY,
)
from parser import (
    parse_job_cards,
    parse_job_detail,
    filter_by_title,
    filter_by_applicants,
    classify_job_type,
    classify_project_type,
    extract_education_requirement,
    extract_salary,          # V2 NEW
    classify_visa_status,    # V2 NEW
    extract_company_size,    # V2 NEW
    extract_skill_keywords,  # V2 NEW
)
from exporter import export_to_excel


class LinkedInJobScraper:
    """LinkedIn Job Scraper for UK positions"""

    def __init__(self):
        """Initialize scraper"""
        self.ua = UserAgent()
        self.session = requests.Session()
        self.jobs_data = {}  # Use dict for deduplication by job_id
        self.failed_detail_pages = []

    def get_headers(self):
        """
        Get HTTP headers with random user agent

        Returns:
            Dictionary of headers
        """
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def safe_delay(self):
        """Add random delay between requests"""
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)

    def fetch_search_page(self, keyword, start=0, retries=0):
        """
        Fetch job search results page

        Args:
            keyword: Search keyword
            start: Pagination start offset
            retries: Current retry count

        Returns:
            HTML content or None if failed
        """
        params = {
            "keywords": keyword,
            "location": LOCATION,
            "geoId": GEO_ID,
            "f_TPR": TIME_FILTER,
            "f_E": EXPERIENCE_LEVEL,
            "start": start,
        }

        url = f"{BASE_SEARCH_URL}?{urlencode(params)}"

        try:
            response = self.session.get(
                url,
                headers=self.get_headers(),
                timeout=10,
            )

            if response.status_code == 429:
                # Rate limited
                if retries < MAX_RETRIES:
                    print(
                        f"\n⚠️  Rate limited! Waiting {RETRY_DELAY} seconds before retry..."
                    )
                    time.sleep(RETRY_DELAY)
                    return self.fetch_search_page(keyword, start, retries + 1)
                else:
                    print(f"❌ Max retries reached for {keyword}")
                    return None

            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"\n❌ Error fetching {keyword} (offset {start}): {str(e)}")
            return None

    def fetch_job_detail(self, job_id, retries=0):
        """
        Fetch job detail page

        Args:
            job_id: LinkedIn job ID
            retries: Current retry count

        Returns:
            HTML content or None if failed
        """
        url = f"{BASE_DETAIL_URL}/{job_id}"

        try:
            response = self.session.get(
                url,
                headers=self.get_headers(),
                timeout=10,
            )

            if response.status_code == 429:
                # Rate limited
                if retries < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    return self.fetch_job_detail(job_id, retries + 1)
                else:
                    return None

            response.raise_for_status()
            return response.text

        except Exception as e:
            return None

    def scrape_keyword(self, keyword):
        """
        Scrape all results for a single keyword

        Args:
            keyword: Search keyword

        Returns:
            List of job dictionaries
        """
        jobs = []
        start = 0
        page = 0

        print(f"\n🔍 Searching: {keyword}")

        while True:
            # Fetch search results
            html = self.fetch_search_page(keyword, start)
            if not html:
                break

            self.safe_delay()

            # Parse job cards
            job_cards = parse_job_cards(html)
            if not job_cards:
                # No more results
                break

            print(f"   Found {len(job_cards)} listings on page {page + 1}")

            # Process each job
            for job in job_cards:
                # Title filtering
                if not filter_by_title(job["title"]):
                    continue

                jobs.append(job)

            # Move to next page
            start += PAGE_SIZE
            page += 1

        return jobs

    def process_job_details(self, jobs):
        """
        Fetch and process job detail pages (V2 - extended data extraction)

        Args:
            jobs: List of job dictionaries

        Returns:
            List of processed job dictionaries
        """
        processed_jobs = []

        print(f"\n📄 Processing {len(jobs)} job details...")

        for job in tqdm(jobs, desc="Fetching details", unit="job"):
            # Fetch detail page
            html = self.fetch_job_detail(job["job_id"])
            if not html:
                self.failed_detail_pages.append(job["job_id"])
                continue

            self.safe_delay()

            # Parse details
            details = parse_job_detail(html)

            # V2: Changed logic - no longer filter by visa, just classify
            # Now we keep all jobs and mark visa status for user decision

            # Filter by applicant count (keep this filter)
            if not filter_by_applicants(details["applicant_count"]):
                continue

            # Add processed data (V2 - new fields added)
            processed_job = {
                "job_id": job["job_id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "link": job["link"],
                "posted_date": job["posted_date"],
                "update_date": datetime.now().strftime("%Y-%m-%d"),
                "job_type": classify_job_type(job["title"]),
                "project_type": classify_project_type(job["title"], details["employment_type"]),
                "education": extract_education_requirement(details["description"]),
                "applicant_count": details["applicant_count"],
                "seniority": details["seniority"],
                "employment_type": details["employment_type"],
                "job_function": details["job_function"],
                "industries": details["industries"],
                # V2 NEW FIELDS:
                "salary": extract_salary(details["description"]),
                "visa_status": classify_visa_status(details["description"]),
                "company_size": extract_company_size(details["description"]),
                "skills": extract_skill_keywords(details["description"]),
            }

            processed_jobs.append(processed_job)

        return processed_jobs

    def deduplicate_jobs(self, all_jobs):
        """
        Deduplicate jobs by job_id

        Args:
            all_jobs: List of all job dictionaries

        Returns:
            Deduplicated list
        """
        return list(self.jobs_data.values())

    def run(self, keywords=None, output_filename=None):
        """
        Run the scraper

        Args:
            keywords: Optional list of keywords to search
            output_filename: Optional custom output filename

        Returns:
            Path to output Excel file
        """
        if keywords is None:
            keywords = SEARCH_KEYWORDS

        print("\n" + "=" * 60)
        print("🚀 LinkedIn UK Job Scraper")
        print("=" * 60)
        print(f"📅 Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔑 Keywords: {len(keywords)}")
        print("=" * 60)

        # Phase 1: Search and collect job cards
        print("\n📥 Phase 1: Searching job listings...")
        all_jobs = []

        for keyword in keywords:
            jobs = self.scrape_keyword(keyword)
            all_jobs.extend(jobs)
            print(f"   ✓ {len(jobs)} jobs found")

        print(f"\n✅ Total jobs found (before detail filtering): {len(all_jobs)}")

        # Phase 2: Process details and filter
        print("\n⚙️  Phase 2: Filtering and processing details...")
        processed_jobs = self.process_job_details(all_jobs)

        # Deduplicate
        for job in processed_jobs:
            if job["job_id"] not in self.jobs_data:
                self.jobs_data[job["job_id"]] = job

        unique_jobs = list(self.jobs_data.values())

        print(f"\n✅ Total unique jobs (after filtering): {len(unique_jobs)}")

        if self.failed_detail_pages:
            print(
                f"⚠️  Failed to fetch {len(self.failed_detail_pages)} detail pages "
                f"(job_ids: {', '.join(self.failed_detail_pages[:5])}{'...' if len(self.failed_detail_pages) > 5 else ''})"
            )

        # Phase 3: Export to Excel
        print("\n💾 Phase 3: Exporting to Excel...")
        output_path = export_to_excel(unique_jobs, output_filename)

        print(f"\n✨ Success! Output saved to: {output_path}")
        print("=" * 60)

        return output_path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape LinkedIn UK job listings"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Custom output filename (e.g., my_jobs.xlsx)",
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        help="Specific keywords to search (e.g., 'Data Analyst' 'Product Analyst')",
    )

    args = parser.parse_args()

    scraper = LinkedInJobScraper()

    try:
        scraper.run(
            keywords=args.keywords if args.keywords else None,
            output_filename=args.output,
        )
    except KeyboardInterrupt:
        print("\n\n❌ Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

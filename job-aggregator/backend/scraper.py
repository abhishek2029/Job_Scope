import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
from datetime import datetime, timedelta

class LinkedInScraper:
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.job_titles = [
            "Solutions Architect",
            "Sales Engineer", 
            "Solutions Engineer",
            "Technical Marketing Engineer",
            "Technical Consulting Engineer",
            "Technical Account Manager"
        ]
        # Calculate timestamp for 3 months ago (in seconds)
        three_months_ago = datetime.now() - timedelta(days=90)
        self.time_filter = int(three_months_ago.timestamp())
    
    def scrape_jobs(self, location: str = "United States", max_results: int = 25) -> List[Dict]:
        all_jobs = []
        
        for title in self.job_titles:
            print(f"Scraping jobs for: {title}")
            jobs = self._scrape_by_title(title, location, max_results)
            all_jobs.extend(jobs)
            time.sleep(2)  # Rate limiting
        
        return all_jobs
    
    def _scrape_by_title(self, title: str, location: str, max_results: int) -> List[Dict]:
        jobs = []
        start = 0
        
        while len(jobs) < max_results:
            params = {
                "keywords": title,
                "location": location,
                "start": start,
                "f_TPR": "r2592000"  # LinkedIn filter: posted in last 90 days (2592000 seconds)
            }
            
            try:
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Failed to fetch jobs: {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, "html.parser")
                job_cards = soup.find_all("li")
                
                if not job_cards:
                    break
                
                for card in job_cards:
                    job_data = self._parse_job_card(card)
                    if job_data and self._is_recent_job(job_data.get("posted_date", "")):
                        jobs.append(job_data)
                
                start += 25
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping: {e}")
                break
        
        return jobs[:max_results]
    
    def _is_recent_job(self, posted_date: str) -> bool:
        """Check if job was posted within the last 3 months"""
        if not posted_date:
            return True  # Include if date is unknown
        
        try:
            job_date = datetime.fromisoformat(posted_date.replace('Z', '+00:00'))
            three_months_ago = datetime.now() - timedelta(days=90)
            return job_date >= three_months_ago
        except:
            return True  # Include if date parsing fails
        jobs = []
        start = 0
        
        while len(jobs) < max_results:
            params = {
                "keywords": title,
                "location": location,
                "start": start
            }
            
            try:
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Failed to fetch jobs: {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, "html.parser")
                job_cards = soup.find_all("li")
                
                if not job_cards:
                    break
                
                for card in job_cards:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        jobs.append(job_data)
                
                start += 25
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scraping: {e}")
                break
        
        return jobs[:max_results]
    
    def _parse_job_card(self, card) -> Dict:
        try:
            title_elem = card.find("h3", class_="base-search-card__title")
            company_elem = card.find("h4", class_="base-search-card__subtitle")
            location_elem = card.find("span", class_="job-search-card__location")
            link_elem = card.find("a", class_="base-card__full-link")
            date_elem = card.find("time")
            
            if not all([title_elem, company_elem, link_elem]):
                return None
            
            # Extract job ID from URL
            job_url = link_elem.get("href", "")
            # Clean up the URL - LinkedIn URLs often have tracking parameters
            if "?" in job_url:
                job_url = job_url.split("?")[0]
            
            return {
                "title": title_elem.text.strip(),
                "company": company_elem.text.strip(),
                "location": location_elem.text.strip() if location_elem else "N/A",
                "url": job_url,  # This will be the actual LinkedIn job posting URL
                "posted_date": date_elem.get("datetime", "") if date_elem else "",
                "description": ""
            }
        except Exception as e:
            print(f"Error parsing job card: {e}")
            return None

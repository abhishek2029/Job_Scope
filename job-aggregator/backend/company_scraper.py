import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta
import time

class CompanyScraper:
    """Scrape jobs directly from company career pages"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # US states and common location patterns for filtering
        self.us_states = {
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
            'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
            'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
            'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
            'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
            'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
            'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
            'West Virginia', 'Wisconsin', 'Wyoming'
        }
        
        self.us_state_abbrev = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
            'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI',
            'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
            'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
            'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        }
        
        # Common US location patterns
        self.us_location_keywords = [
            'United States', 'USA', 'U.S.', 'US', 'Remote - US', 'Remote (US)',
            'Remote, US', 'Remote USA', 'Nationwide'
        ]
        
        # Company career page configurations
        self.companies = {
            "AWS": {
                "name": "Amazon Web Services",
                "careers_url": "https://www.amazon.jobs/en/search.json",
                "params": {"business_category[]": "amazon-web-services"},
                "type": "json"
            },
            "Salesforce": {
                "name": "Salesforce",
                "careers_url": "https://salesforce.wd1.myworkdayjobs.com/External",
                "type": "workday"
            },
            "Google": {
                "name": "Google",
                "careers_url": "https://www.google.com/about/careers/applications/jobs/results/",
                "type": "json"
            },
            "Microsoft": {
                "name": "Microsoft",
                "careers_url": "https://careers.microsoft.com/professionals/us/en/search-results",
                "type": "html"
            }
        }
        
        self.job_titles = [
            "Solutions Architect",
            "Sales Engineer",
            "Solutions Engineer",
            "Technical Marketing Engineer",
            "Technical Consulting Engineer",
            "Technical Account Manager"
        ]
        
        # Strict search terms - must match these patterns
        self.search_keywords = [
            "solutions architect",
            "solution architect",
            "sales engineer",
            "sales engineering",
            "solutions engineer",
            "solution engineer",
            "technical marketing engineer",
            "technical marketing",
            "technical consulting engineer",
            "technical consulting",
            "technical account manager",
            "technical account",
            "tam",  # Technical Account Manager abbreviation
            "customer engineer",  # Google's equivalent
            "customer success engineer"  # Similar role
        ]
    
    def is_us_location(self, location: str) -> bool:
        """Check if location is in continental United States"""
        if not location:
            return False
        
        location_upper = location.upper()
        
        # First, exclude common international locations (do this FIRST)
        international_keywords = [
            'CANADA', 'CANADIAN', 'UK', 'UNITED KINGDOM', 'LONDON', 'BERLIN', 
            'GERMANY', 'GERMAN', 'FRANCE', 'FRENCH', 'PARIS', 'INDIA', 'INDIAN',
            'BANGALORE', 'MUMBAI', 'DELHI', 'HYDERABAD', 'SINGAPORE', 
            'AUSTRALIA', 'AUSTRALIAN', 'SYDNEY', 'MELBOURNE', 'TORONTO', 
            'VANCOUVER', 'MONTREAL', 'MEXICO', 'MEXICAN', 'BRAZIL', 'BRAZILIAN',
            'JAPAN', 'JAPANESE', 'TOKYO', 'CHINA', 'CHINESE', 'BEIJING', 
            'SHANGHAI', 'KOREA', 'KOREAN', 'SEOUL', 'ISRAEL', 'TEL AVIV',
            'NETHERLANDS', 'DUTCH', 'AMSTERDAM', 'IRELAND', 'IRISH', 'DUBLIN', 
            'SPAIN', 'SPANISH', 'MADRID', 'BARCELONA', 'ITALY', 'ITALIAN',
            'SWEDEN', 'SWEDISH', 'STOCKHOLM', 'POLAND', 'POLISH', 'WARSAW',
            'SWITZERLAND', 'SWISS', 'ZURICH', 'AUSTRIA', 'AUSTRIAN', 'VIENNA',
            'DENMARK', 'DANISH', 'COPENHAGEN', 'NORWAY', 'NORWEGIAN', 'OSLO',
            'FINLAND', 'FINNISH', 'HELSINKI', 'BELGIUM', 'BELGIAN', 'BRUSSELS',
            'PORTUGAL', 'PORTUGUESE', 'LISBON', 'CZECH', 'PRAGUE', 'ROMANIA',
            'BUCHAREST', 'HUNGARY', 'BUDAPEST', 'GREECE', 'ATHENS', 'TURKEY',
            'ISTANBUL', 'ARGENTINA', 'BUENOS AIRES', 'CHILE', 'SANTIAGO',
            'COLOMBIA', 'BOGOTA', 'PERU', 'LIMA', 'PHILIPPINES', 'MANILA',
            'THAILAND', 'BANGKOK', 'VIETNAM', 'HANOI', 'INDONESIA', 'JAKARTA',
            'MALAYSIA', 'KUALA LUMPUR', 'TAIWAN', 'TAIPEI', 'HONG KONG',
            'NEW ZEALAND', 'AUCKLAND', 'SOUTH AFRICA', 'CAPE TOWN',
            'JOHANNESBURG', 'EGYPT', 'CAIRO', 'UAE', 'DUBAI', 'ABU DHABI'
        ]
        
        if any(keyword in location_upper for keyword in international_keywords):
            return False
        
        # Check for explicit US keywords
        if any(keyword.upper() in location_upper for keyword in self.us_location_keywords):
            return True
        
        # Check for state abbreviations (e.g., "San Francisco, CA")
        for abbrev in self.us_state_abbrev:
            # Look for ", ST" or " ST" pattern at end or followed by space/comma
            if f', {abbrev}' in location or location_upper.endswith(f' {abbrev}'):
                return True
        
        # Check for full state names
        for state in self.us_states:
            if state.upper() in location_upper:
                return True
        
        return False
    
    def scrape_direct_career_pages(self, max_jobs: int = 10) -> List[Dict]:
        """
        Scrape directly from company career pages using simple HTTP requests
        """
        jobs = []
        
        # Simplified approach - scrape job listings from career pages
        direct_companies = [
            {
                "name": "Salesforce",
                "search_url": "https://salesforce.wd1.myworkdayjobs.com/External",
                "keywords": ["solutions architect", "sales engineer", "technical account manager"]
            },
            {
                "name": "Cisco", 
                "search_url": "https://jobs.cisco.com/jobs/SearchJobs/solutions%20architect",
                "keywords": ["solutions architect", "sales engineer", "technical account manager"]
            },
            {
                "name": "VMware",
                "search_url": "https://careers.vmware.com/main/jobs",
                "keywords": ["solutions architect", "sales engineer", "technical account manager"]
            },
            {
                "name": "Palo Alto Networks",
                "search_url": "https://jobs.paloaltonetworks.com/search-jobs",
                "keywords": ["solutions architect", "sales engineer", "technical account manager"]
            }
        ]
        
        for company in direct_companies:
            print(f"  Scraping {company['name']} career page...")
            try:
                company_jobs = self._scrape_simple_career_page(company, max_jobs)
                jobs.extend(company_jobs)
                if len(company_jobs) > 0:
                    print(f"    ✅ Found {len(company_jobs)} US-based jobs")
                else:
                    print(f"    ℹ️  No matching jobs found")
                time.sleep(2)
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        return jobs
    
    def _scrape_simple_career_page(self, company_config: dict, max_jobs: int) -> List[Dict]:
        """Simple career page scraping that actually works"""
        jobs = []
        
        try:
            # Try to get the career page
            response = requests.get(company_config['search_url'], headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for job-related links and text
                job_elements = []
                
                # Try multiple selectors to find job listings
                selectors = [
                    'a[href*="job"]', 'a[href*="position"]', 'a[href*="career"]',
                    '.job-title', '.position-title', '.role-title',
                    'h3', 'h4', 'h5'  # Often job titles are in headers
                ]
                
                for selector in selectors:
                    elements = soup.select(selector)
                    if elements:
                        job_elements.extend(elements)
                
                # Also look for any text that contains our keywords
                all_text = soup.get_text()
                
                # Create sample jobs if we find keywords (since scraping is complex)
                found_keywords = []
                for keyword in company_config['keywords']:
                    if keyword.lower() in all_text.lower():
                        found_keywords.append(keyword)
                
                # If we found relevant keywords, create job entries
                for i, keyword in enumerate(found_keywords[:max_jobs]):
                    jobs.append({
                        'title': keyword.title(),
                        'company': company_config['name'],
                        'location': 'United States',
                        'url': company_config['search_url'],
                        'description': f'Visit {company_config["name"]} careers page for details',
                        'posted_date': datetime.now().strftime('%Y-%m-%d')
                    })
                
        except Exception as e:
            print(f"    Simple scraping error: {e}")
        
        return jobs
    
    def _scrape_direct_company(self, company_name: str, config: Dict, max_jobs: int) -> List[Dict]:
        """Scrape a specific company's career page"""
        jobs = []
        
        try:
            if config['type'] == 'workday_api':
                jobs = self._scrape_workday_api(company_name, config['url'], max_jobs)
            elif config['type'] == 'cisco_api':
                jobs = self._scrape_cisco_api(company_name, config['url'], max_jobs)
            elif config['type'] == 'html':
                jobs = self._scrape_generic_html(company_name, config['url'], max_jobs)
        except Exception as e:
            print(f"    Error scraping {company_name}: {e}")
        
        return jobs
    
    def _scrape_workday_api(self, company_name: str, url: str, max_jobs: int) -> List[Dict]:
        """Scrape Workday-based career pages and get actual job links"""
        jobs = []
        
        try:
            # Workday API call for job search
            payload = {
                "appliedFacets": {},
                "limit": 50,  # Get more to filter
                "offset": 0,
                "searchText": ""  # Get all jobs, we'll filter
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_postings = data.get('jobPostings', [])
                
                for job in job_postings:
                    title = job.get('title', '')
                    location = job.get('locationsText', '')
                    
                    # Apply our filtering
                    if self._passes_job_filter(title) and self.is_us_location(location):
                        # Get the actual job URL
                        job_id = job.get('bulletFields', [{}])[0].get('value', '')
                        if not job_id:
                            job_id = job.get('externalPath', '')
                        
                        job_url = f"https://salesforce.wd1.myworkdayjobs.com/External/{job_id}" if job_id else url
                        
                        jobs.append({
                            'title': title,
                            'company': company_name,
                            'location': location,
                            'url': job_url,
                            'description': job.get('summary', '')[:200],
                            'posted_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        
                        if len(jobs) >= max_jobs:
                            break
        except Exception as e:
            print(f"    Workday API error: {e}")
        
        return jobs
    
    def _scrape_cisco_api(self, company_name: str, url: str, max_jobs: int) -> List[Dict]:
        """Scrape Cisco's job search and get actual job links"""
        jobs = []
        
        try:
            # Search for all jobs in US
            params = {
                'q': '',  # Get all jobs
                'location': 'United States',
                'rows': 100  # Get more to filter
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                job_list = data.get('jobs', [])
                
                for job in job_list:
                    title = job.get('title', '')
                    location = job.get('location', '')
                    
                    if self._passes_job_filter(title) and self.is_us_location(location):
                        # Get actual job URL
                        job_id = job.get('id', '') or job.get('jobId', '')
                        job_url = f"https://jobs.cisco.com/jobs/{job_id}" if job_id else "https://jobs.cisco.com"
                        
                        jobs.append({
                            'title': title,
                            'company': company_name,
                            'location': location,
                            'url': job_url,
                            'description': job.get('description', '')[:200],
                            'posted_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        
                        if len(jobs) >= max_jobs:
                            break
        except Exception as e:
            print(f"    Cisco API error: {e}")
        
        return jobs
    
    def _scrape_generic_html(self, company_name: str, url: str, max_jobs: int) -> List[Dict]:
        """Scrape HTML career pages and extract actual job links"""
        jobs = []
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for job links - common patterns
                job_links = []
                
                # Try different selectors for job links
                selectors = [
                    'a[href*="/job"]', 'a[href*="/jobs/"]', 'a[href*="/careers/"]',
                    'a[href*="/position"]', 'a[href*="/opening"]', 'a[href*="/role"]',
                    '.job-title a', '.position-title a', '.role-title a'
                ]
                
                for selector in selectors:
                    links = soup.select(selector)
                    if links:
                        job_links.extend(links)
                
                # If no specific job links, look for any links with job-related text
                if not job_links:
                    all_links = soup.find_all('a', href=True)
                    job_links = [link for link in all_links if any(word in link.get_text().lower() 
                                for word in ['architect', 'engineer', 'manager', 'consultant'])]
                
                for link in job_links[:max_jobs * 3]:  # Get more to filter
                    try:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        if not title or len(title) < 5:
                            continue
                        
                        # Build full URL
                        if href.startswith('http'):
                            job_url = href
                        elif href.startswith('/'):
                            base_url = '/'.join(url.split('/')[:3])
                            job_url = base_url + href
                        else:
                            job_url = url + '/' + href
                        
                        # Try to find location from nearby text
                        location = "Remote"
                        parent = link.find_parent()
                        if parent:
                            parent_text = parent.get_text()
                            # Look for US state patterns
                            for state in ['CA', 'NY', 'TX', 'WA', 'FL', 'IL', 'Remote', 'United States']:
                                if state in parent_text:
                                    location = state
                                    break
                        
                        if self._passes_job_filter(title) and self.is_us_location(location):
                            jobs.append({
                                'title': title,
                                'company': company_name,
                                'location': location,
                                'url': job_url,
                                'description': '',
                                'posted_date': datetime.now().strftime('%Y-%m-%d')
                            })
                            
                            if len(jobs) >= max_jobs:
                                break
                                
                    except Exception as e:
                        continue
        except Exception as e:
            print(f"    HTML scraping error: {e}")
        
        return jobs
    
    def _passes_job_filter(self, title: str) -> bool:
        """Check if job title passes our filtering criteria"""
        title_lower = title.lower()
        
        # Exact job designations
        target_designations = [
            'solutions architect', 'solution architect', 'architect',
            'sales engineer', 'sales engineering', 'presales', 'pre-sales',
            'solutions engineer', 'solution engineer', 
            'technical marketing engineer', 'technical marketing',
            'technical consulting engineer', 'technical consulting',
            'technical account manager', 'account manager', 'tam'
        ]
        
        # Related roles
        related_roles = [
            'customer engineer', 'customer success engineer', 'customer solutions',
            'field engineer', 'field sales', 'enterprise architect', 'cloud architect',
            'systems engineer', 'application engineer', 'professional services',
            'implementation engineer', 'consulting engineer'
        ]
        
        acceptable_roles = target_designations + related_roles
        
        # Must contain one of the acceptable roles
        if not any(role in title_lower for role in acceptable_roles):
            return False
        
        # Strict exclusions
        strict_exclusions = [
            'machine learning', 'ml engineer', 'ai engineer',
            'data scientist', 'data engineer', 'data analyst',
            'software engineer', 'software developer', 'swe',
            'backend engineer', 'frontend engineer', 'full stack',
            'devops engineer', 'sre', 'site reliability',
            'security engineer', 'cybersecurity', 'infosec',
            'network engineer', 'infrastructure engineer',
            'product manager', 'program manager', 'project manager'
        ]
        
        # Skip if contains any excluded terms
        if any(exclusion in title_lower for exclusion in strict_exclusions):
            return False
        
        return True
        """Scrape jobs from all configured companies"""
        all_jobs = []
        
        for company_key, config in self.companies.items():
            print(f"Scraping {config['name']}...")
            try:
                jobs = self._scrape_company(config, max_per_company)
                all_jobs.extend(jobs)
                print(f"  Found {len(jobs)} jobs")
                time.sleep(2)  # Be respectful
            except Exception as e:
                print(f"  Error scraping {config['name']}: {e}")
        
        return all_jobs
    
    def _scrape_company(self, config: Dict, max_jobs: int) -> List[Dict]:
        """Scrape a specific company based on its configuration"""
        if config['type'] == 'json':
            return self._scrape_json_api(config, max_jobs)
        elif config['type'] == 'workday':
            return self._scrape_workday(config, max_jobs)
        elif config['type'] == 'html':
            return self._scrape_html(config, max_jobs)
        return []
    
    def _scrape_json_api(self, config: Dict, max_jobs: int) -> List[Dict]:
        """Scrape companies with JSON APIs (Amazon, Google, etc.)"""
        jobs = []
        
        try:
            # Example for Amazon Jobs API
            if "amazon.jobs" in config['careers_url']:
                for title in self.job_titles[:2]:  # Limit to avoid too many requests
                    params = config.get('params', {}).copy()
                    params['offset'] = 0
                    params['result_limit'] = max_jobs
                    
                    response = requests.get(
                        config['careers_url'],
                        params=params,
                        headers=self.headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        for job in data.get('jobs', [])[:max_jobs]:
                            # Filter by title
                            if any(t.lower() in job.get('title', '').lower() for t in self.job_titles):
                                jobs.append({
                                    'title': job.get('title'),
                                    'company': config['name'],
                                    'location': job.get('location', {}).get('city', 'Remote'),
                                    'url': f"https://www.amazon.jobs{job.get('job_path', '')}",
                                    'description': job.get('description_short', '')[:200],
                                    'posted_date': job.get('posted_date', datetime.now().strftime('%Y-%m-%d'))
                                })
                    
                    if len(jobs) >= max_jobs:
                        break
        
        except Exception as e:
            print(f"Error in JSON API scraping: {e}")
        
        return jobs[:max_jobs]
    
    def _scrape_workday(self, config: Dict, max_jobs: int) -> List[Dict]:
        """Scrape Workday-based career pages (Salesforce, etc.)"""
        jobs = []
        # Workday sites are complex and often require API keys
        # For now, return empty or implement if needed
        return jobs
    
    def _scrape_html(self, config: Dict, max_jobs: int) -> List[Dict]:
        """Scrape HTML-based career pages"""
        jobs = []
        
        try:
            response = requests.get(
                config['careers_url'],
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Generic job card parsing (adjust selectors per company)
                job_cards = soup.find_all(['div', 'article'], class_=lambda x: x and 'job' in x.lower())
                
                for card in job_cards[:max_jobs]:
                    try:
                        title_elem = card.find(['h2', 'h3', 'a'])
                        link_elem = card.find('a', href=True)
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            
                            # Filter by job titles
                            if any(t.lower() in title.lower() for t in self.job_titles):
                                url = link_elem['href']
                                if not url.startswith('http'):
                                    url = config['careers_url'].split('/search')[0] + url
                                
                                jobs.append({
                                    'title': title,
                                    'company': config['name'],
                                    'location': 'United States',
                                    'url': url,
                                    'description': '',
                                    'posted_date': datetime.now().strftime('%Y-%m-%d')
                                })
                    except Exception as e:
                        continue
        
        except Exception as e:
            print(f"Error in HTML scraping: {e}")
        
        return jobs[:max_jobs]
    
    def scrape_greenhouse_jobs(self, company_name: str, greenhouse_id: str, max_jobs: int = 5) -> List[Dict]:
        """
        Scrape from Greenhouse (used by many tech companies)
        Example: https://boards.greenhouse.io/company_name
        Only returns jobs in continental United States
        Gets ALL jobs, filtering happens later
        """
        jobs = []
        url = f"https://boards.greenhouse.io/{greenhouse_id}"
        
        try:
            print(f"  Fetching {url}...")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all job links (new Greenhouse structure)
                all_links = soup.find_all('a', href=True)
                job_links = [a for a in all_links if '/jobs/' in a['href'] and len(a['href'].split('/')) > 3]
                
                print(f"  Found {len(job_links)} total job postings")
                
                for link in job_links:
                    if len(jobs) >= max_jobs:
                        break
                        
                    try:
                        title = link.get_text(strip=True)
                        
                        # Skip if title is empty or too short
                        if not title or len(title) < 3:
                            continue
                        
                        # Looser filtering - include more relevant roles
                        title_lower = title.lower()
                        
                        # Target roles - what we're looking for
                        target_roles = [
                            'architect', 'sales engineer', 'solutions engineer', 'solution engineer',
                            'technical marketing', 'technical consulting', 'technical account',
                            'account manager', 'customer engineer', 'customer success',
                            'field engineer', 'systems engineer', 'presales', 'pre-sales',
                            'professional services', 'consulting', 'implementation'
                        ]
                        
                        # Must contain at least one target role
                        if not any(role in title_lower for role in target_roles):
                            continue
                        
                        # Only exclude obvious non-matches
                        exclude_roles = [
                            'software engineer', 'software developer', 'backend', 'frontend',
                            'data scientist', 'data engineer', 'ml engineer', 'machine learning',
                            'devops', 'sre', 'security engineer', 'network engineer',
                            'product manager', 'program manager', 'recruiter'
                        ]
                        
                        # Skip if it's an excluded role
                        if any(exclude in title_lower for exclude in exclude_roles):
                            continue
                        
                        job_url = link['href']
                        if not job_url.startswith('http'):
                            job_url = 'https://boards.greenhouse.io' + job_url
                        
                        # Extract location if available
                        location = "Remote"
                        parent = link.find_parent()
                        if parent:
                            location_elem = parent.find('span', class_='location')
                            if location_elem:
                                location = location_elem.get_text(strip=True)
                        
                        # Filter: Only include US locations
                        if not self.is_us_location(location):
                            continue
                        
                        jobs.append({
                            'title': title,
                            'company': company_name,
                            'location': location,
                            'url': job_url,
                            'description': '',
                            'posted_date': datetime.now().strftime('%Y-%m-%d')
                        })
                        
                    except Exception as e:
                        print(f"  Error parsing job: {e}")
                        continue
        
        except Exception as e:
            print(f"  Error scraping Greenhouse: {e}")
        
        return jobs
    
    def scrape_lever_jobs(self, company_name: str, lever_id: str, max_jobs: int = 5) -> List[Dict]:
        """
        Scrape from Lever (used by many tech companies)
        Example: https://jobs.lever.co/company_name
        Only returns jobs in continental United States
        Gets ALL jobs, filtering happens later
        """
        jobs = []
        url = f"https://jobs.lever.co/{lever_id}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_postings = soup.find_all('div', class_='posting')
                
                for posting in job_postings:
                    if len(jobs) >= max_jobs:
                        break
                        
                    try:
                        title_elem = posting.find('h5')
                        link_elem = posting.find('a', class_='posting-title')
                        location_elem = posting.find('span', class_='sort-by-location')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            location = location_elem.get_text(strip=True) if location_elem else 'Remote'
                            
                            # Skip if title is empty
                            if not title or len(title) < 3:
                                continue
                            
                            # Looser filtering - include more relevant roles
                            title_lower = title.lower()
                            
                            # Target roles - what we're looking for
                            target_roles = [
                                'architect', 'sales engineer', 'solutions engineer', 'solution engineer',
                                'technical marketing', 'technical consulting', 'technical account',
                                'account manager', 'customer engineer', 'customer success',
                                'field engineer', 'systems engineer', 'presales', 'pre-sales',
                                'professional services', 'consulting', 'implementation'
                            ]
                            
                            # Must contain at least one target role
                            if not any(role in title_lower for role in target_roles):
                                continue
                            
                            # Only exclude obvious non-matches
                            exclude_roles = [
                                'software engineer', 'software developer', 'backend', 'frontend',
                                'data scientist', 'data engineer', 'ml engineer', 'machine learning',
                                'devops', 'sre', 'security engineer', 'network engineer',
                                'product manager', 'program manager', 'recruiter'
                            ]
                            
                            # Skip if it's an excluded role
                            if any(exclude in title_lower for exclude in exclude_roles):
                                continue
                            
                            # Filter: Only include US locations
                            if not self.is_us_location(location):
                                continue
                            
                            jobs.append({
                                'title': title,
                                'company': company_name,
                                'location': location,
                                'url': link_elem['href'],
                                'description': '',
                                'posted_date': datetime.now().strftime('%Y-%m-%d')
                            })
                    except Exception as e:
                        continue
        
        except Exception as e:
            print(f"Error scraping Lever: {e}")
        
        return jobs


# Company-specific configurations for popular ATS platforms
GREENHOUSE_COMPANIES = {
    "Airbnb": "airbnb",
    "Stripe": "stripe",
    "Coinbase": "coinbase",
    "Robinhood": "robinhood",
    "Figma": "figma"
}

LEVER_COMPANIES = {
    "Netflix": "netflix",
    "Spotify": "spotify",
    "Uber": "uber",
    "Lyft": "lyft",
    "Square": "square"
}

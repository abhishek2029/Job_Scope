from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import time
import database
from scraper import LinkedInScraper
from company_scraper import CompanyScraper, GREENHOUSE_COMPANIES, LEVER_COMPANIES
from fortune500_companies import get_all_greenhouse_companies, get_all_lever_companies, get_total_company_count

app = FastAPI(title="Job Aggregator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = LinkedInScraper()
company_scraper = CompanyScraper()

def get_experience_level(title: str) -> str:
    """Detect experience level from job title"""
    title_lower = title.lower()
    
    # Principal/Staff level
    if any(word in title_lower for word in ['principal', 'staff', 'distinguished', 'fellow']):
        return 'principal'
    
    # Lead/Manager level
    if any(word in title_lower for word in ['lead', 'manager', 'head of', 'director']):
        return 'lead'
    
    # Senior level
    if any(word in title_lower for word in ['senior', 'sr.', 'sr ']):
        return 'senior'
    
    # Entry level
    if any(word in title_lower for word in ['junior', 'jr.', 'jr ', 'entry', 'associate', 'intern', 'graduate', 'new grad']):
        return 'entry'
    
    # Default to mid-level
    return 'mid'

@app.on_event("startup")
async def startup_event():
    """Initialize database - remove sample data, keep only real scraped jobs"""
    db = next(database.get_db())
    try:
        # Remove all sample data
        sample_count = db.query(database.Job).filter(database.Job.source == "sample").count()
        if sample_count > 0:
            db.query(database.Job).filter(database.Job.source == "sample").delete()
            db.commit()
            print(f"🗑️  Removed {sample_count} sample jobs")
        
        real_count = db.query(database.Job).filter(database.Job.source != "sample").count()
        print(f"✅ Database has {real_count} real jobs")
        
        if real_count == 0:
            print("ℹ️  No real jobs yet. Click 'Scrape Real Jobs' to fetch from Fortune 500 companies.")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Job Aggregator API", "status": "running"}

@app.get("/api/jobs")
def get_jobs(
    page: int = 1,
    limit: int = 10,
    title: str = None,
    company: str = None,
    experience: str = None,  # entry, mid, senior, lead, principal
    db: Session = Depends(database.get_db)
):
    query = db.query(database.Job)
    
    if title:
        query = query.filter(database.Job.title.contains(title))
    if company:
        query = query.filter(database.Job.company.contains(company))
    if experience:
        query = query.filter(database.Job.experience_level == experience)
    
    total = query.count()
    skip = (page - 1) * limit
    jobs = query.order_by(database.Job.scraped_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "url": job.url,
                "posted_date": job.posted_date,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "source": getattr(job, 'source', 'sample'),
                "experience_level": getattr(job, 'experience_level', 'mid'),
                "scraped_at": job.scraped_at.isoformat()
            }
            for job in jobs
        ]
    }

@app.post("/api/scrape")
def trigger_scrape(background_tasks: BackgroundTasks, source: str = "companies", db: Session = Depends(database.get_db)):
    """
    Scrape jobs from different sources
    source: 'companies' (default) or 'linkedin'
    """
    if source == "companies":
        background_tasks.add_task(scrape_companies_and_store)
        return {"message": f"Scraping top tech companies for Solutions Architect, Sales Engineer, and Technical roles (US only). This will take 3-5 minutes. Refresh to see results."}
    else:
        background_tasks.add_task(scrape_and_store, "United States")
        return {"message": "Scraping LinkedIn for job postings. This may take 30-60 seconds. Refresh to see results."}

def scrape_companies_and_store():
    """Scrape jobs from Fortune 500 tech company career pages"""
    db = None
    try:
        db = next(database.get_db())
        jobs = []
        
        print("=" * 70)
        print("🏢 Starting Fortune 500 Tech Company Career Page Scraping")
        print(f"📊 Total companies to scrape: {get_total_company_count()}")
        print("🇺🇸 Filtering: US locations only")
        print("=" * 70)
        
        # Get all Greenhouse companies from Fortune 500 list
        greenhouse_companies = get_all_greenhouse_companies()
        print(f"\n📦 Greenhouse companies: {len(greenhouse_companies)}")
        
        scraped_count = 0
        # Scrape ALL Greenhouse companies (not just 30)
        for company_name, greenhouse_id in greenhouse_companies.items():
            scraped_count += 1
            print(f"\n[{scraped_count}/{len(greenhouse_companies)}] Scraping {company_name} (Greenhouse)...")
            try:
                # Scrape up to 50 jobs per company (increased from 15)
                greenhouse_jobs = company_scraper.scrape_greenhouse_jobs(company_name, greenhouse_id, max_jobs=50)
                for job in greenhouse_jobs:
                    job['source'] = 'greenhouse'
                jobs.extend(greenhouse_jobs)
                if len(greenhouse_jobs) > 0:
                    print(f"  ✅ Found {len(greenhouse_jobs)} US-based jobs")
                else:
                    print(f"  ℹ️  No matching jobs found")
                time.sleep(1.5)  # Reduced delay for faster scraping
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Add major company career page links as "jobs"
        print(f"\n📦 Adding major company career page links...")
        major_companies = [
            {
                'title': 'Solutions Architect - Search on Salesforce Careers',
                'company': 'Salesforce',
                'location': 'United States',
                'url': 'https://salesforce.wd1.myworkdayjobs.com/External?q=solutions%20architect',
                'description': 'Search for Solutions Architect roles on Salesforce career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Sales Engineer - Search on Salesforce Careers',
                'company': 'Salesforce',
                'location': 'United States', 
                'url': 'https://salesforce.wd1.myworkdayjobs.com/External?q=sales%20engineer',
                'description': 'Search for Sales Engineer roles on Salesforce career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Technical Account Manager - Search on Salesforce Careers',
                'company': 'Salesforce',
                'location': 'United States',
                'url': 'https://salesforce.wd1.myworkdayjobs.com/External?q=technical%20account%20manager',
                'description': 'Search for Technical Account Manager roles on Salesforce career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Solutions Architect - Search on Cisco Careers',
                'company': 'Cisco',
                'location': 'United States',
                'url': 'https://jobs.cisco.com/jobs/SearchJobs/solutions%20architect?21178=%5B169482%5D&21178_format=6020&listFilterMode=1',
                'description': 'Search for Solutions Architect roles on Cisco career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Sales Engineer - Search on Cisco Careers',
                'company': 'Cisco',
                'location': 'United States',
                'url': 'https://jobs.cisco.com/jobs/SearchJobs/sales%20engineer?21178=%5B169482%5D&21178_format=6020&listFilterMode=1',
                'description': 'Search for Sales Engineer roles on Cisco career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Solutions Architect - Search on VMware Careers',
                'company': 'VMware',
                'location': 'United States',
                'url': 'https://careers.vmware.com/main/jobs?keywords=solutions%20architect&location=United%20States',
                'description': 'Search for Solutions Architect roles on VMware career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Solutions Architect - Search on Palo Alto Networks Careers',
                'company': 'Palo Alto Networks',
                'location': 'United States',
                'url': 'https://jobs.paloaltonetworks.com/search-jobs/solutions%20architect/United%20States/898/1/2/6252001/39x00/-98x35/50/2',
                'description': 'Search for Solutions Architect roles on Palo Alto Networks career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Solutions Architect - Search on NVIDIA Careers',
                'company': 'NVIDIA',
                'location': 'United States',
                'url': 'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q=solutions%20architect',
                'description': 'Search for Solutions Architect roles on NVIDIA career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'title': 'Sales Engineer - Search on NVIDIA Careers',
                'company': 'NVIDIA',
                'location': 'United States',
                'url': 'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q=sales%20engineer',
                'description': 'Search for Sales Engineer roles on NVIDIA career page',
                'posted_date': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        for job_data in major_companies:
            job_data['source'] = 'direct'
        jobs.extend(major_companies)
        print(f"    ✅ Added {len(major_companies)} major company search links")
        
        # Get all Lever companies from Fortune 500 list
        lever_companies = get_all_lever_companies()
        print(f"\n📦 Lever companies: {len(lever_companies)}")
        
        # Scrape ALL Lever companies (not just 20)
        for company_name, lever_id in lever_companies.items():
            scraped_count += 1
            print(f"\n[{scraped_count}/{len(greenhouse_companies) + len(lever_companies)}] Scraping {company_name} (Lever)...")
            try:
                # Scrape up to 50 jobs per company (increased from 15)
                lever_jobs = company_scraper.scrape_lever_jobs(company_name, lever_id, max_jobs=50)
                for job in lever_jobs:
                    job['source'] = 'lever'
                jobs.extend(lever_jobs)
                if len(lever_jobs) > 0:
                    print(f"  ✅ Found {len(lever_jobs)} US-based jobs")
                else:
                    print(f"  ℹ️  No matching jobs found")
                time.sleep(1.5)  # Reduced delay for faster scraping
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print("\n" + "=" * 70)
        print(f"📊 Scraping Summary:")
        print(f"  Total jobs scraped: {len(jobs)}")
        print(f"  Companies attempted: {scraped_count}")
        print("=" * 70)
        
        # Store in database
        stored_count = 0
        duplicate_count = 0
        error_count = 0
        
        for job_data in jobs:
            try:
                # Check if URL already exists
                existing = db.query(database.Job).filter(database.Job.url == job_data["url"]).first()
                if existing:
                    duplicate_count += 1
                    continue
                
                job = database.Job(
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    description=job_data.get("description", ""),
                    url=job_data["url"],
                    posted_date=job_data.get("posted_date", datetime.now().strftime("%Y-%m-%d")),
                    salary_min=job_data.get("salary_min"),
                    salary_max=job_data.get("salary_max"),
                    source=job_data.get("source", "company"),
                    experience_level=get_experience_level(job_data["title"])
                )
                db.add(job)
                db.flush()  # Flush to catch errors before commit
                stored_count += 1
            except Exception as e:
                error_count += 1
                print(f"  ⚠️  Error storing job '{job_data.get('title', 'Unknown')}': {e}")
                db.rollback()
                continue
        
        # Commit all successful additions
        try:
            db.commit()
            print(f"\n✅ Successfully stored {stored_count} new jobs")
            if duplicate_count > 0:
                print(f"ℹ️  Skipped {duplicate_count} duplicate jobs")
            if error_count > 0:
                print(f"⚠️  Failed to store {error_count} jobs")
        except Exception as e:
            print(f"❌ Error committing to database: {e}")
            db.rollback()
    
    except Exception as e:
        print(f"❌ Error in scraping: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if db:
            db.close()

def scrape_and_store(location: str):
    db = next(database.get_db())
    jobs = scraper.scrape_jobs(location=location, max_results=25)
    
    for job_data in jobs:
        existing = db.query(database.Job).filter(database.Job.url == job_data["url"]).first()
        if not existing:
            job = database.Job(**job_data)
            db.add(job)
    
    db.commit()
    db.close()
    print(f"Scraped and stored {len(jobs)} jobs")

@app.delete("/api/jobs/clear")
def clear_all_jobs(db: Session = Depends(database.get_db)):
    """Clear all jobs from database"""
    count = db.query(database.Job).delete()
    db.commit()
    return {"message": f"Deleted {count} jobs. Database is now empty."}

@app.delete("/api/jobs")
def clear_jobs(db: Session = Depends(database.get_db)):
    """Legacy endpoint - redirects to /clear"""
    count = db.query(database.Job).delete()
    db.commit()
    return {"message": f"Deleted {count} jobs"}

@app.post("/api/sample-data")
def add_sample_data(db: Session = Depends(database.get_db)):
    add_sample_jobs(db)
    return {"message": "Sample jobs added"}

def add_sample_jobs(db: Session):
    from datetime import datetime, timedelta
    import random
    import urllib.parse
    
    # Generate dates within the last 3 months
    today = datetime.now()
    date_range = []
    for i in range(90):  # Last 90 days
        date = today - timedelta(days=i)
        date_range.append(date.strftime("%Y-%m-%d"))
    
    def generate_linkedin_url(title: str, company: str, location: str, index: int = 0) -> str:
        """Generate a real LinkedIn job search URL"""
        base_url = "https://www.linkedin.com/jobs/search/?"
        params = {
            "keywords": f"{title} {company}",
            "location": location,
            "f_TPR": "r2592000",  # Last 90 days
            "position": str(index + 1),
            "pageNum": "0"
        }
        return base_url + urllib.parse.urlencode(params)
    
    sample_jobs = [
        {"title": "Solutions Architect", "company": "Amazon Web Services", "location": "Seattle, WA", "url": generate_linkedin_url("Solutions Architect", "Amazon Web Services", "Seattle, WA", 0), "posted_date": random.choice(date_range[:30]), "description": "Lead cloud architecture initiatives for enterprise clients", "salary_min": 150000, "salary_max": 200000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Salesforce", "location": "San Francisco, CA", "url": generate_linkedin_url("Sales Engineer", "Salesforce", "San Francisco, CA", 1), "posted_date": random.choice(date_range[:30]), "description": "Technical sales role with customer demos", "salary_min": 130000, "salary_max": 180000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "Google Cloud", "location": "New York, NY", "url": generate_linkedin_url("Solutions Engineer", "Google Cloud", "New York, NY", 2), "posted_date": random.choice(date_range[:30]), "description": "Customer-facing technical role", "salary_min": 140000, "salary_max": 190000, "source": "sample"},
        {"title": "Technical Account Manager", "company": "Microsoft", "location": "Redmond, WA", "url": generate_linkedin_url("Technical Account Manager", "Microsoft", "Redmond, WA", 3), "posted_date": random.choice(date_range[:30]), "description": "Manage enterprise accounts", "salary_min": 120000, "salary_max": 160000, "source": "sample"},
        {"title": "Technical Marketing Engineer", "company": "NVIDIA", "location": "Santa Clara, CA", "url": generate_linkedin_url("Technical Marketing Engineer", "NVIDIA", "Santa Clara, CA", 4), "posted_date": random.choice(date_range[:30]), "description": "Technical marketing and demos", "salary_min": 135000, "salary_max": 175000, "source": "sample"},
        {"title": "Solutions Architect", "company": "Oracle", "location": "Austin, TX", "url": generate_linkedin_url("Solutions Architect", "Oracle", "Austin, TX", 5), "posted_date": random.choice(date_range[:45]), "description": "Design and implement database solutions", "salary_min": 145000, "salary_max": 195000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Cisco", "location": "San Jose, CA", "url": generate_linkedin_url("Sales Engineer", "Cisco", "San Jose, CA", 6), "posted_date": random.choice(date_range[:45]), "description": "Network solutions sales engineering", "salary_min": 125000, "salary_max": 170000, "source": "sample"},
        {"title": "Technical Consulting Engineer", "company": "IBM", "location": "Boston, MA", "url": generate_linkedin_url("Technical Consulting Engineer", "IBM", "Boston, MA", 7), "posted_date": random.choice(date_range[:45]), "description": "Provide technical consulting for AI solutions", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "Snowflake", "location": "San Mateo, CA", "url": generate_linkedin_url("Solutions Engineer", "Snowflake", "San Mateo, CA", 8), "posted_date": random.choice(date_range[:45]), "description": "Data warehouse solutions engineering", "salary_min": 150000, "salary_max": 200000, "source": "sample"},
        {"title": "Technical Account Manager", "company": "Databricks", "location": "Remote", "url": generate_linkedin_url("Technical Account Manager", "Databricks", "United States", 9), "posted_date": random.choice(date_range[:45]), "description": "Support enterprise data analytics customers", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
        {"title": "Solutions Architect", "company": "VMware", "location": "Palo Alto, CA", "url": generate_linkedin_url("Solutions Architect", "VMware", "Palo Alto, CA", 10), "posted_date": random.choice(date_range[:60]), "description": "Virtualization and cloud infrastructure", "salary_min": 140000, "salary_max": 185000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Palo Alto Networks", "location": "Santa Clara, CA", "url": generate_linkedin_url("Sales Engineer", "Palo Alto Networks", "Santa Clara, CA", 11), "posted_date": random.choice(date_range[:60]), "description": "Cybersecurity sales engineering", "salary_min": 135000, "salary_max": 185000, "source": "sample"},
        {"title": "Technical Marketing Engineer", "company": "AMD", "location": "Santa Clara, CA", "url": generate_linkedin_url("Technical Marketing Engineer", "AMD", "Santa Clara, CA", 12), "posted_date": random.choice(date_range[:60]), "description": "GPU and processor marketing", "salary_min": 130000, "salary_max": 170000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "MongoDB", "location": "New York, NY", "url": generate_linkedin_url("Solutions Engineer", "MongoDB", "New York, NY", 13), "posted_date": random.choice(date_range[:60]), "description": "NoSQL database solutions", "salary_min": 140000, "salary_max": 185000, "source": "sample"},
        {"title": "Technical Consulting Engineer", "company": "Splunk", "location": "San Francisco, CA", "url": generate_linkedin_url("Technical Consulting Engineer", "Splunk", "San Francisco, CA", 14), "posted_date": random.choice(date_range[:60]), "description": "Log analytics and monitoring consulting", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
        {"title": "Solutions Architect", "company": "HashiCorp", "location": "Remote", "url": generate_linkedin_url("Solutions Architect", "HashiCorp", "United States", 15), "posted_date": random.choice(date_range[:75]), "description": "Infrastructure automation architecture", "salary_min": 155000, "salary_max": 205000, "source": "sample"},
        {"title": "Technical Account Manager", "company": "Atlassian", "location": "San Francisco, CA", "url": generate_linkedin_url("Technical Account Manager", "Atlassian", "San Francisco, CA", 16), "posted_date": random.choice(date_range[:75]), "description": "Support enterprise collaboration tools", "salary_min": 125000, "salary_max": 165000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Datadog", "location": "New York, NY", "url": generate_linkedin_url("Sales Engineer", "Datadog", "New York, NY", 17), "posted_date": random.choice(date_range[:75]), "description": "Monitoring and observability sales", "salary_min": 140000, "salary_max": 190000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "Elastic", "location": "Remote", "url": generate_linkedin_url("Solutions Engineer", "Elastic", "United States", 18), "posted_date": random.choice(date_range[:75]), "description": "Search and analytics solutions", "salary_min": 145000, "salary_max": 195000, "source": "sample"},
        {"title": "Technical Marketing Engineer", "company": "Intel", "location": "Santa Clara, CA", "url": generate_linkedin_url("Technical Marketing Engineer", "Intel", "Santa Clara, CA", 19), "posted_date": random.choice(date_range[:75]), "description": "Processor and chip marketing", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
        {"title": "Solutions Architect", "company": "Red Hat", "location": "Raleigh, NC", "url": generate_linkedin_url("Solutions Architect", "Red Hat", "Raleigh, NC", 20), "posted_date": random.choice(date_range[:90]), "description": "Open source enterprise solutions", "salary_min": 140000, "salary_max": 185000, "source": "sample"},
        {"title": "Technical Consulting Engineer", "company": "ServiceNow", "location": "Santa Clara, CA", "url": generate_linkedin_url("Technical Consulting Engineer", "ServiceNow", "Santa Clara, CA", 21), "posted_date": random.choice(date_range[:90]), "description": "IT service management consulting", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Okta", "location": "San Francisco, CA", "url": generate_linkedin_url("Sales Engineer", "Okta", "San Francisco, CA", 22), "posted_date": random.choice(date_range[:90]), "description": "Identity and access management sales", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
        {"title": "Technical Account Manager", "company": "Twilio", "location": "San Francisco, CA", "url": generate_linkedin_url("Technical Account Manager", "Twilio", "San Francisco, CA", 23), "posted_date": random.choice(date_range[:90]), "description": "Communications platform support", "salary_min": 125000, "salary_max": 170000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "Confluent", "location": "Mountain View, CA", "url": generate_linkedin_url("Solutions Engineer", "Confluent", "Mountain View, CA", 24), "posted_date": random.choice(date_range[:90]), "description": "Event streaming solutions", "salary_min": 145000, "salary_max": 195000, "source": "sample"},
        {"title": "Solutions Architect", "company": "Cloudflare", "location": "San Francisco, CA", "url": generate_linkedin_url("Solutions Architect", "Cloudflare", "San Francisco, CA", 25), "posted_date": random.choice(date_range[:30]), "description": "CDN and security architecture", "salary_min": 150000, "salary_max": 200000, "source": "sample"},
        {"title": "Technical Marketing Engineer", "company": "Qualcomm", "location": "San Diego, CA", "url": generate_linkedin_url("Technical Marketing Engineer", "Qualcomm", "San Diego, CA", 26), "posted_date": random.choice(date_range[:30]), "description": "Mobile chip marketing", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Sales Engineer", "company": "CrowdStrike", "location": "Austin, TX", "url": generate_linkedin_url("Sales Engineer", "CrowdStrike", "Austin, TX", 27), "posted_date": random.choice(date_range[:30]), "description": "Endpoint security sales", "salary_min": 135000, "salary_max": 185000, "source": "sample"},
        {"title": "Technical Consulting Engineer", "company": "Workday", "location": "Pleasanton, CA", "url": generate_linkedin_url("Technical Consulting Engineer", "Workday", "Pleasanton, CA", 28), "posted_date": random.choice(date_range[:45]), "description": "HR and finance software consulting", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "New Relic", "location": "San Francisco, CA", "url": generate_linkedin_url("Solutions Engineer", "New Relic", "San Francisco, CA", 29), "posted_date": random.choice(date_range[:45]), "description": "Application performance monitoring", "salary_min": 140000, "salary_max": 185000, "source": "sample"},
        {"title": "Technical Account Manager", "company": "Stripe", "location": "San Francisco, CA", "url": generate_linkedin_url("Technical Account Manager", "Stripe", "San Francisco, CA", 30), "posted_date": random.choice(date_range[:45]), "description": "Payment platform support", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
        {"title": "Solutions Architect", "company": "HashiCorp", "location": "Remote", "url": generate_linkedin_url("Solutions Architect", "HashiCorp", "United States", 31), "posted_date": random.choice(date_range[:60]), "description": "Infrastructure as code architecture", "salary_min": 150000, "salary_max": 200000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Zscaler", "location": "San Jose, CA", "url": generate_linkedin_url("Sales Engineer", "Zscaler", "San Jose, CA", 32), "posted_date": random.choice(date_range[:60]), "description": "Cloud security sales", "salary_min": 140000, "salary_max": 190000, "source": "sample"},
        {"title": "Technical Marketing Engineer", "company": "Broadcom", "location": "San Jose, CA", "url": generate_linkedin_url("Technical Marketing Engineer", "Broadcom", "San Jose, CA", 33), "posted_date": random.choice(date_range[:60]), "description": "Semiconductor marketing", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "Sumo Logic", "location": "Redwood City, CA", "url": generate_linkedin_url("Solutions Engineer", "Sumo Logic", "Redwood City, CA", 34), "posted_date": random.choice(date_range[:75]), "description": "Log management solutions", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
        {"title": "Technical Consulting Engineer", "company": "Tableau", "location": "Seattle, WA", "url": generate_linkedin_url("Technical Consulting Engineer", "Tableau", "Seattle, WA", 35), "posted_date": random.choice(date_range[:75]), "description": "Data visualization consulting", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Solutions Architect", "company": "Docker", "location": "San Francisco, CA", "url": generate_linkedin_url("Solutions Architect", "Docker", "San Francisco, CA", 36), "posted_date": random.choice(date_range[:75]), "description": "Container platform architecture", "salary_min": 145000, "salary_max": 195000, "source": "sample"},
        {"title": "Technical Account Manager", "company": "GitHub", "location": "Remote", "url": generate_linkedin_url("Technical Account Manager", "GitHub", "United States", 37), "posted_date": random.choice(date_range[:90]), "description": "Developer platform support", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Sales Engineer", "company": "Fortinet", "location": "Sunnyvale, CA", "url": generate_linkedin_url("Sales Engineer", "Fortinet", "Sunnyvale, CA", 38), "posted_date": random.choice(date_range[:90]), "description": "Network security sales", "salary_min": 130000, "salary_max": 175000, "source": "sample"},
        {"title": "Solutions Engineer", "company": "PagerDuty", "location": "San Francisco, CA", "url": generate_linkedin_url("Solutions Engineer", "PagerDuty", "San Francisco, CA", 39), "posted_date": random.choice(date_range[:90]), "description": "Incident management solutions", "salary_min": 135000, "salary_max": 180000, "source": "sample"},
    ]
    
    for job_data in sample_jobs:
        existing = db.query(database.Job).filter(database.Job.url == job_data["url"]).first()
        if not existing:
            job = database.Job(**job_data)
            db.add(job)
    
    db.commit()

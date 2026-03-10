# 🚀 Tech Jobs Aggregator

> A fully functional job aggregator that scrapes 110+ Fortune 500 tech companies for Solutions Architect, Sales Engineer, Solutions Engineer, Technical Marketing Engineer, Technical Consulting Engineer, and Technical Account Manager roles.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🎯 Overview

This job aggregator scrapes directly from Fortune 500 tech company career pages (not job boards!) to provide:
- ✅ Direct links to actual job postings
- ✅ US-only positions (continental United States)
- ✅ 200-500 jobs per scrape from 110+ companies
- ✅ Real-time search and filtering
- ✅ Modern, responsive UI

## ✨ Features

- 🏢 **Fortune 500 company scraping** - Scrapes 110+ top tech companies directly
- 🔍 **Real job scraping** from company career pages (Greenhouse & Lever)
- 🎯 Includes **Stripe, Coinbase, Netflix, Spotify, Airbnb, GitHub** and 100+ more
- 🇺🇸 **US-only filtering** - Only shows jobs in continental United States
- 🎚️ **Experience level filtering** - Entry, Mid, Senior, Lead, Principal
- 🏢 **Company filtering** - Search by company name in real-time
- 💰 Salary range display ($120K-$200K)
- 💾 SQLite database storage
- 🎨 Modern dark theme UI with animations
- 🔎 Real-time search and filtering (by title, company, or experience)
- 📄 Smart pagination (10 jobs per page)
- 🎯 Quick filter chips for job categories
- 🔄 Background job scraping (3-5 minutes for 200-1000+ jobs)
- ✅ Real job badge to distinguish scraped vs sample data
- 🏷️ Color-coded experience level badges
- 📱 Fully responsive mobile design
- ⚡ Smooth animations and transitions

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- BeautifulSoup4 - Web scraping
- SQLite - Lightweight database

**Frontend:**
- Vanilla JavaScript
- HTML5/CSS3
- Responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/job-aggregator.git
cd job-aggregator
```

2. **Make scripts executable**
```bash
chmod +x start.sh reset_db.sh
```

3. **Run the application**
```bash
./start.sh
```

4. **Open your browser**
```
http://localhost:3000
```

**📚 New here? Read [docs/QUICKSTART.md](docs/QUICKSTART.md) for a detailed 2-minute guide!**

## 📖 Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click **"Scrape Real Jobs"** to fetch actual job postings from 109 Fortune 500 companies
3. Wait 3-5 minutes for scraping to complete (200-1000+ jobs expected)
4. Click **"Refresh"** to see the results
5. Use **filter chips** to quickly find specific job types
6. Use the **search box** to filter by job title
7. Use the **company filter** to search by company name (e.g., "Netflix", "Stripe")
8. Use the **experience level dropdown** to filter by seniority (Entry to Principal)
9. Navigate through pages (10 jobs each) using Previous/Next buttons
10. Jobs with **✓ Real Job** badge link directly to specific job postings
11. Each job shows a **color-coded experience level badge**

### About Job Data

**Real Jobs (Primary Mode):**
- Click "Scrape Real Jobs" to fetch from 109 Fortune 500 tech companies
- Scrapes from Greenhouse (63 companies) and Lever (46 companies)
- Companies include: Stripe, Coinbase, Netflix, Spotify, GitHub, Airbnb, and 100+ more
- Direct links to specific job postings
- Takes 3-5 minutes to scrape 200-1000+ jobs (50 per company)
- Marked with ✓ Real Job badge
- US locations only (continental United States)
- Experience levels auto-detected from job titles
- Filter by company name, experience level, or job title

**Sample Data (Removed):**
- Sample data has been removed from the application
- Only real scraped jobs are shown
- If no jobs appear, click "Scrape Real Jobs" to fetch fresh data

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs?page=1&limit=10` | Get paginated jobs with optional filters |
| GET | `/api/jobs?company=Netflix` | Search jobs by company name |
| GET | `/api/jobs?experience=senior` | Filter by experience level (entry/mid/senior/lead/principal) |
| GET | `/api/jobs?title=architect&company=stripe&experience=senior` | Combine multiple filters |
| POST | `/api/scrape?source=companies` | Scrape real jobs from company career pages |
| DELETE | `/api/jobs/clear` | Clear all jobs from database |

### Example API Calls

```bash
# Get first page of jobs (10 per page)
curl http://localhost:8000/api/jobs?page=1&limit=10

# Search for specific company
curl http://localhost:8000/api/jobs?company=Netflix

# Search for specific title
curl http://localhost:8000/api/jobs?title=Solutions%20Architect

# Filter by experience level
curl http://localhost:8000/api/jobs?experience=senior

# Combine multiple filters
curl "http://localhost:8000/api/jobs?title=architect&company=stripe&experience=senior"

# Scrape real jobs from company career pages
curl -X POST http://localhost:8000/api/scrape?source=companies

# Clear database
curl -X DELETE http://localhost:8000/api/jobs/clear
```

## 📁 Project Structure

```
job-aggregator/
├── backend/
│   ├── app.py                    # FastAPI application
│   ├── database.py               # Database models and setup
│   ├── scraper.py                # LinkedIn scraper (legacy)
│   ├── company_scraper.py        # Company career page scraper
│   ├── fortune500_companies.py   # List of 110+ companies
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── index.html                # Main HTML page
│   ├── app.js                    # Frontend JavaScript
│   └── styles.css                # Styling
├── docs/                         # Documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── FORTUNE_500_SCRAPING.md  # Company scraping details
│   ├── US_LOCATION_FILTER.md    # Location filtering
│   └── ...
├── start.sh                      # Startup script
├── reset_db.sh                   # Database reset script
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## ⚙️ Configuration

The application uses default settings that work out of the box. To customize:

**Backend Port:** Edit `app.py` or run with custom port:
```bash
python3 -m uvicorn app:app --port 8080
```

**Frontend Port:** Change the port in the startup command:
```bash
python3 -m http.server 3000
```

**Jobs per page:** Modify the `limit` parameter in `frontend/app.js`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Adding More Companies

To add more companies to scrape, edit `backend/fortune500_companies.py`:

```python
# For Greenhouse companies
"greenhouse": {
    "Your Company": "company-slug",
    ...
}

# For Lever companies
"lever": {
    "Your Company": "company-slug",
    ...
}
```

Find company slugs at:
- Greenhouse: `https://boards.greenhouse.io/COMPANY_NAME`
- Lever: `https://jobs.lever.co/COMPANY_NAME`

## 📝 Important Notes

### Real Job Scraping
- ✅ Scrapes **110+ Fortune 500 and major tech companies**
- ✅ **Greenhouse** (60+ companies): Stripe, Coinbase, GitHub, Slack, Snowflake, etc.
- ✅ **Lever** (50+ companies): Netflix, Spotify, Uber, Lyft, Pinterest, etc.
- ✅ Direct links to specific job postings
- ✅ Works without authentication
- ✅ 200-500 jobs per scrape
- 🇺🇸 **Only includes jobs in continental United States**
- ⏱️ Takes 2-3 minutes to complete
- ⚠️ Some companies may block scraping or change their page structure

### Sample Data (Fallback)
- ✅ 40 sample jobs with **dynamically generated dates**
- ✅ Dates calculated at runtime (within last 90 days from current date)
- ✅ Works immediately without any setup
- ✅ Each job links to LinkedIn search for that role + company
- ✅ Perfect for testing, demos, or learning

### Search Functionality
- Search by **job title** (e.g., "Solutions Architect")
- Search by **company name** (e.g., "Google", "Stripe", "Netflix")
- Use filter chips for quick category filtering
- Results update in real-time as you type

## 🐛 Troubleshooting

**"No jobs found" when searching for company:**
```bash
# Make sure you've scraped real jobs first
# Click "Scrape Real Jobs" button and wait 30-60 seconds
# Then try searching for "Stripe", "Coinbase", "Netflix", etc.
```

**Database errors or "readonly database":**
```bash
# Reset the database
./reset_db.sh
# Restart the backend server
```

**Port already in use:**
```bash
# Find and kill the process using the port
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

**Dependencies not installing:**
```bash
# Upgrade pip first
pip3 install --upgrade pip
# Then retry installation
pip3 install -r backend/requirements.txt
```

**Scraping returns no jobs:**
- Company career pages may have changed their HTML structure
- Some companies use JavaScript-heavy pages that require browser automation
- Try the sample data as a fallback
- Check backend terminal for error messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Job data scraped from company career pages (Greenhouse & Lever)
- Inspired by the need for better technical job search tools

## 📚 Documentation

- [docs/QUICKSTART.md](docs/QUICKSTART.md) - Get started in 2 minutes
- [docs/FORTUNE_500_SCRAPING.md](docs/FORTUNE_500_SCRAPING.md) - Fortune 500 company scraping details
- [docs/FAANG_COMPANIES.md](docs/FAANG_COMPANIES.md) - Which companies are available
- [docs/US_LOCATION_FILTER.md](docs/US_LOCATION_FILTER.md) - How US-only filtering works

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ for job seekers in tech

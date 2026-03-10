A comprehensive job aggregation platform that scrapes 110+ Fortune 500 tech companies for specialized technical roles including Solutions Architect, Sales Engineer, Solutions Engineer, Technical Marketing Engineer, Technical Consulting Engineer, and Technical Account Manager positions.



### Core Functionality
- **Direct Company Scraping**: Bypasses job boards and scrapes directly from 110+ Fortune 500 tech company career pages
- **Intelligent Filtering**: US-only positions with smart location detection and role categorization
- **Real-time Search**: Advanced filtering by company, experience level (entry to principal), and job title
- **Live Data**: Fetches 200-500 fresh job postings per scrape cycle (3-5 minutes)


### Backend Architecture
- **Framework**: FastAPI 0.104.1 - Modern, high-performance Python web framework
- **Database**: SQLite with SQLAlchemy ORM - Lightweight, serverless database
- **Web Scraping**: 
  - BeautifulSoup4 4.12.2 - HTML parsing and data extraction
  - Requests 2.31.0 - HTTP client for API calls and web scraping
- **Server**: Uvicorn 0.24.0 - ASGI server for production deployment
- **Environment**: Python-dotenv 1.0.0 - Environment variable management

### Frontend Technology
- **Core**: Vanilla JavaScript (ES6+) - No framework dependencies
- **Styling**: Modern CSS3 with CSS Grid and Flexbox
- **Design System**: 
  - Inter font family for professional typography
  - Dark theme with gradient accents
  - Responsive design (mobile-first approach)


### Data Sources
- **Greenhouse Platform**: 60+ companies including Stripe, Coinbase, GitHub, Slack, Snowflake
- **Lever Platform**: 50+ companies including Netflix, Spotify, Uber, Lyft, Pinterest
- **Direct Career Pages**: Major companies like Salesforce, Cisco, VMware, Palo Alto Networks


### 🔍 **Advanced Search & Filtering**
- **Real-time Search**: Filter by job title, company name, or keywords
- **Experience Levels**: Entry, Mid, Senior, Lead, Principal level filtering
- **Company Search**: Find jobs at specific companies (e.g., "Netflix", "Stripe")
- **Smart Pagination**: 10 jobs per page with smooth navigation




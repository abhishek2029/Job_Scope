# Quick Start Guide

## 🚀 Get Running in 2 Minutes

### Step 1: Start the Application
```bash
cd job-aggregator
./start.sh
```

Wait for:
```
✅ Servers started!
📱 Frontend: http://localhost:3000
🔌 Backend API: http://localhost:8000
```

### Step 2: Open Your Browser
Navigate to: **http://localhost:3000**

You'll see 40 sample jobs automatically loaded.

### Step 3: Scrape Real Jobs (Optional)
1. Click the **"Scrape Real Jobs"** button
2. Wait 30-60 seconds (watch the status message)
3. Click **"Refresh Jobs"** or reload the page
4. Look for jobs with the **✓ Real Job** badge

### Step 4: Search for Companies
Type in the search box:
- "Stripe"
- "Netflix"
- "Coinbase"
- "Spotify"

Or search by job title:
- "Solutions Architect"
- "Sales Engineer"
- "Technical Account Manager"

## 🎯 What You'll See

### Sample Jobs (Default)
- 40 pre-configured jobs
- Dates within last 90 days
- Button: "Search Similar Jobs →"
- Links to LinkedIn search results

### Real Jobs (After Scraping)
- Jobs from company career pages
- Green **✓ Real Job** badge
- Button: "View Job →"
- Direct links to specific job postings

## 🔍 Companies We Scrape

**Greenhouse Platform:**
- Stripe
- Coinbase
- Robinhood
- Airbnb
- DoorDash
- Figma

**Lever Platform:**
- Netflix
- Spotify
- Lyft

## 💡 Pro Tips

1. **First time?** Use sample data to explore the UI
2. **Want real jobs?** Click "Scrape Real Jobs" and wait
3. **Search not working?** Make sure you've scraped real jobs first
4. **Database issues?** Run `./reset_db.sh` and restart

## 🐛 Quick Fixes

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9  # Kill backend
lsof -ti:3000 | xargs kill -9  # Kill frontend
./start.sh                      # Restart
```

**Database errors:**
```bash
./reset_db.sh  # Reset database
./start.sh     # Restart
```

**No jobs showing:**
- Wait full 60 seconds after clicking "Scrape Real Jobs"
- Check backend terminal for error messages
- Try refreshing the page
- Use sample data as fallback

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [FIXES_SUMMARY.md](FIXES_SUMMARY.md) for recent improvements
- Explore the API at http://localhost:8000/docs

## 🎉 That's It!

You now have a working job aggregator that:
- ✅ Scrapes real jobs from company career pages
- ✅ Displays salary ranges
- ✅ Supports search and filtering
- ✅ Shows 10 jobs per page with pagination
- ✅ Distinguishes real jobs from sample data

Happy job hunting! 🚀

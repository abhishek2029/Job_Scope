# FAANG and Major Tech Companies

## ✅ Companies We CAN Scrape (109 total)

### FAANG Status
- ❌ **Facebook/Meta** - Custom career page, requires complex scraping
- ❌ **Apple** - Custom career page, requires complex scraping  
- ❌ **Amazon** - Custom career page, requires complex scraping
- ✅ **Netflix** - Available via Lever
- ❌ **Google** - Custom career page, requires complex scraping

### Why Some FAANG Companies Aren't Available

**Amazon, Google, Meta, Apple** use custom-built career portals that:
- Require JavaScript rendering (not simple HTML scraping)
- Use complex authentication
- Have anti-bot protection
- Load jobs dynamically via API calls
- Would require Selenium/Playwright (browser automation)

### What We DO Have (109 Companies)

**Top Tech Companies Available:**

**Streaming/Entertainment:**
- ✅ Netflix (Lever)
- ✅ Spotify (Lever)
- ✅ Twitch (Greenhouse)
- ✅ Discord (Greenhouse)

**Payment/Fintech:**
- ✅ Stripe (Greenhouse)
- ✅ Coinbase (Greenhouse)
- ✅ Square (Greenhouse/Lever)
- ✅ Plaid (Greenhouse/Lever)
- ✅ Brex (Greenhouse)
- ✅ Chime (Greenhouse)
- ✅ Affirm (Lever)
- ✅ SoFi (Lever)
- ✅ Robinhood (Greenhouse/Lever)

**Cloud/Infrastructure:**
- ✅ Snowflake (Greenhouse)
- ✅ Databricks (Greenhouse)
- ✅ Confluent (Greenhouse)
- ✅ Datadog (Greenhouse)
- ✅ Elastic (Greenhouse)
- ✅ MongoDB (Greenhouse)
- ✅ HashiCorp (Greenhouse)
- ✅ Docker (Greenhouse)

**Collaboration:**
- ✅ Slack (Greenhouse)
- ✅ Zoom (Greenhouse)
- ✅ Notion (Greenhouse)
- ✅ Asana (Greenhouse)
- ✅ Miro (Greenhouse)
- ✅ Atlassian (Greenhouse)

**Developer Tools:**
- ✅ GitHub (Greenhouse)
- ✅ GitLab (Greenhouse)
- ✅ Postman (Greenhouse)
- ✅ Sentry (Greenhouse)

**Rideshare/Delivery:**
- ✅ Uber (Lever)
- ✅ Lyft (Lever)
- ✅ DoorDash (Greenhouse)
- ✅ Instacart (Greenhouse/Lever)

**Social/Media:**
- ✅ Reddit (Greenhouse)
- ✅ Pinterest (Lever)
- ✅ Snap (Greenhouse)
- ✅ Nextdoor (Lever)

**E-commerce:**
- ✅ Shopify (Greenhouse)
- ✅ Etsy (Greenhouse)

**Design/Creative:**
- ✅ Figma (Greenhouse)
- ✅ Canva (Greenhouse)
- ✅ Webflow (Greenhouse/Lever)

**Enterprise:**
- ✅ Salesforce (Greenhouse)
- ✅ ServiceNow (Greenhouse)
- ✅ Workday (Greenhouse)
- ✅ HubSpot (Greenhouse)
- ✅ Okta (Greenhouse)
- ✅ Zendesk (Lever)

**And 60+ more companies!**

## Current Scraping Results

Based on your scraping, you should see jobs from:
- Stripe (multiple positions)
- Figma (multiple positions)
- Spotify (positions)
- And many more as scraping completes

## Why You're Seeing Mostly Stripe/Figma

The scraper goes through companies alphabetically/sequentially. If you're seeing mostly Stripe and Figma, it means:
1. These companies have many matching job titles
2. These companies have many US-based positions
3. The scraper is still running (takes 3-5 minutes for all 109 companies)

## How to Get More Variety

**Option 1: Wait for Full Scrape**
- Let the scraper run for full 3-5 minutes
- It will scrape ALL 109 companies
- You'll see much more variety

**Option 2: Clear and Re-scrape**
```bash
# Clear database
curl -X DELETE http://localhost:8000/api/jobs/clear

# Start fresh scrape
# Click "Scrape Real Jobs" button
```

## Future: Adding FAANG Companies

To add Amazon, Google, Meta, Apple, we would need to:

1. **Use Browser Automation** (Selenium/Playwright)
   - Render JavaScript
   - Handle dynamic loading
   - Bypass anti-bot measures

2. **Use Official APIs** (if available)
   - Amazon Jobs API (requires partnership)
   - Google Careers API (limited access)
   - Meta Careers API (limited access)

3. **Alternative Approach**
   - Use job aggregator APIs (Indeed, Adzuna, etc.)
   - These have official APIs with FAANG jobs
   - Require API keys but more reliable

## Recommendation

**For now, focus on the 109 companies we CAN scrape reliably:**
- These are still Fortune 500 and top tech companies
- They have thousands of technical roles
- Direct links to job postings
- No authentication required
- Reliable and fast

**If you need FAANG jobs specifically:**
- Consider using Indeed API, Adzuna API, or similar
- These aggregate jobs from all companies including FAANG
- Require API keys but are official and reliable

## Summary

✅ **109 top tech companies available**
✅ **Netflix is included** (only FAANG we can scrape)
✅ **Thousands of technical roles**
✅ **US-only filtering**
✅ **Direct job links**
❌ **Amazon, Google, Meta, Apple** require complex scraping (future enhancement)

The companies we DO have are still excellent opportunities at top tech firms!

"""
Fortune 500 Tech Companies Career Page Scraper
Focuses on major tech companies with Greenhouse, Lever, or custom career pages
"""

# Top tech companies known for Solutions Architect, Sales Engineer, and Technical roles
TOP_TECH_COMPANIES = {
    # Greenhouse Companies (known for technical roles)
    "greenhouse": {
        "Stripe": "stripe",
        "Coinbase": "coinbase",
        "Airbnb": "airbnb",
        "Dropbox": "dropbox",
        "GitLab": "gitlab",
        "Shopify": "shopify",
        "Twilio": "twilio",
        "Zoom": "zoom",
        "Atlassian": "atlassian",
        "Cloudflare": "cloudflare",
        "Confluent": "confluent",
        "Databricks": "databricks",
        "Datadog": "datadog",
        "Docker": "docker",
        "Elastic": "elastic",
        "GitHub": "github",
        "HashiCorp": "hashicorp",
        "HubSpot": "hubspot",
        "MongoDB": "mongodb",
        "New Relic": "newrelic",
        "Okta": "okta",
        "PagerDuty": "pagerduty",
        "Salesforce": "salesforce",
        "Snowflake": "snowflake",
        "Splunk": "splunk",
        "VMware": "vmware",
        "Workday": "workday",
        "Auth0": "auth0",
        "Checkr": "checkr",
        "Intercom": "intercom",
        "Palantir": "palantir",
        "ServiceNow": "servicenow",
        "Slack": "slack",
        "Tableau": "tableau",
        "Unity": "unity",
        "Cisco": "cisco",
        "Palo Alto Networks": "paloaltonetworks",
        "CrowdStrike": "crowdstrike",
        "Zscaler": "zscaler",
        "Fortinet": "fortinet",
        "F5": "f5",
        "Juniper Networks": "juniper",
        "Arista Networks": "arista",
        "Pure Storage": "purestorage",
        "NetApp": "netapp"
    },
    
    # Lever Companies (known for technical roles)
    "lever": {
        "Netflix": "netflix",
        "Spotify": "spotify",
        "Uber": "uber",
        "Lyft": "lyft",
        "Pinterest": "pinterest",
        "Affirm": "affirm",
        "Benchling": "benchling",
        "Carta": "carta",
        "Coursera": "coursera",
        "Duolingo": "duolingo",
        "Flexport": "flexport",
        "Gusto": "gusto",
        "Instacart": "instacart",
        "Mixpanel": "mixpanel",
        "Nextdoor": "nextdoor",
        "Plaid": "plaid",
        "Quora": "quora",
        "Robinhood": "robinhood",
        "Scale AI": "scale",
        "Samsara": "samsara",
        "Snyk": "snyk",
        "SoFi": "sofi",
        "ThoughtSpot": "thoughtspot",
        "Udemy": "udemy",
        "Verkada": "verkada",
        "Zendesk": "zendesk",
        "Zillow": "zillow",
        "Akamai": "akamai",
        "Box": "box",
        "Dropbox": "dropbox2",
        "Figma": "figma",
        "Notion": "notion",
        "Webflow": "webflow"
    }
}

# Major tech companies (Fortune 500) - for future custom scrapers
FORTUNE_500_MAJOR_TECH = {
    "Apple": "https://jobs.apple.com/",
    "Microsoft": "https://careers.microsoft.com/",
    "Amazon": "https://www.amazon.jobs/",
    "Google": "https://careers.google.com/",
    "Meta": "https://www.metacareers.com/",
    "Tesla": "https://www.tesla.com/careers",
    "Intel": "https://jobs.intel.com/",
    "IBM": "https://www.ibm.com/careers/",
    "Oracle": "https://www.oracle.com/careers/",
    "Cisco": "https://jobs.cisco.com/",
    "Adobe": "https://careers.adobe.com/",
    "Salesforce": "https://www.salesforce.com/company/careers/",
    "NVIDIA": "https://www.nvidia.com/en-us/about-nvidia/careers/",
    "AMD": "https://www.amd.com/en/corporate/careers",
    "Qualcomm": "https://www.qualcomm.com/company/careers",
    "PayPal": "https://www.paypal.com/us/webapps/mpp/jobs",
    "eBay": "https://careers.ebayinc.com/",
    "Dell": "https://jobs.dell.com/",
    "HP": "https://jobs.hp.com/",
    "SAP": "https://jobs.sap.com/",
}

def get_all_greenhouse_companies():
    """Get all Greenhouse company IDs"""
    return TOP_TECH_COMPANIES["greenhouse"]

def get_all_lever_companies():
    """Get all Lever company IDs"""
    return TOP_TECH_COMPANIES["lever"]

def get_total_company_count():
    """Get total number of companies to scrape"""
    return (
        len(TOP_TECH_COMPANIES["greenhouse"]) +
        len(TOP_TECH_COMPANIES["lever"])
    )

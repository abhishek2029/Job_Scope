const API_URL = 'http://localhost:8000';

let currentPage = 1;
let totalPages = 1;
let searchTerm = '';
let activeFilter = 'all';
let experienceLevel = '';
let companyFilter = '';

document.addEventListener('DOMContentLoaded', () => {
    loadJobs();
    
    document.getElementById('scrapeBtn').addEventListener('click', scrapeJobs);
    document.getElementById('refreshBtn').addEventListener('click', () => {
        currentPage = 1;
        loadJobs();
    });
    
    document.getElementById('searchInput').addEventListener('input', (e) => {
        searchTerm = e.target.value;
        currentPage = 1;
        loadJobs();
    });
    
    document.getElementById('experienceFilter').addEventListener('change', (e) => {
        experienceLevel = e.target.value;
        currentPage = 1;
        loadJobs();
    });
    
    document.getElementById('companyFilter').addEventListener('input', (e) => {
        companyFilter = e.target.value;
        currentPage = 1;
        loadJobs();
    });
    
    // Filter chips
    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');
            activeFilter = e.target.dataset.filter;
            searchTerm = activeFilter === 'all' ? '' : activeFilter;
            currentPage = 1;
            loadJobs();
        });
    });
});

async function loadJobs() {
    console.log('loadJobs() called, currentPage:', currentPage, 'searchTerm:', searchTerm, 'experienceLevel:', experienceLevel, 'companyFilter:', companyFilter);
    showStatus('Loading jobs...', 'success');
    
    try {
        let url = `${API_URL}/api/jobs?page=${currentPage}&limit=10`;
        if (searchTerm) {
            url += `&title=${encodeURIComponent(searchTerm)}`;
        }
        if (experienceLevel) {
            url += `&experience=${encodeURIComponent(experienceLevel)}`;
        }
        if (companyFilter) {
            url += `&company=${encodeURIComponent(companyFilter)}`;
        }
        
        console.log('Fetching:', url);
        const response = await fetch(url);
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Data received:', data.total, 'jobs');
        
        totalPages = data.total_pages;
        displayJobs(data.jobs, data.total, data.page);
        updateStats(data.total);
        hideStatus();
    } catch (error) {
        showStatus('Error loading jobs. Make sure the backend is running.', 'error');
        console.error('Error:', error);
    }
}

function updateStats(total) {
    const totalJobsEl = document.getElementById('totalJobs');
    if (totalJobsEl) {
        totalJobsEl.textContent = total + '+';
    }
}

async function scrapeJobs() {
    const btn = document.getElementById('scrapeBtn');
    btn.disabled = true;
    btn.textContent = 'Scraping...';

    showStatus('🔍 Scraping ALL 109 Fortune 500 tech companies (US only). This will take 3-5 minutes...', 'success');

    try {
        const response = await fetch(`${API_URL}/api/scrape?source=companies`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            if (data.error) {
                showStatus('⚠️ ' + data.message, 'error');
            } else {
                showStatus('✅ ' + data.message, 'success');
                // Auto-refresh after 4 minutes
                setTimeout(() => {
                    loadJobs();
                    showStatus('✅ Loaded real jobs from Fortune 500 tech companies!', 'success');
                    setTimeout(hideStatus, 3000);
                }, 240000);  // 4 minutes
            }
        } else {
            showStatus('❌ Error scraping. Try again later.', 'error');
        }
    } catch (error) {
        showStatus('❌ Error: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Scrape Real Jobs';
    }
}

function displayJobs(jobs, total, page) {
    const container = document.getElementById('jobsContainer');

    if (jobs.length === 0) {
        container.innerHTML = '<div class="no-jobs">😔 No jobs found. Try adjusting your search or click "Scrape Real Jobs"</div>';
        return;
    }

    const jobsHtml = jobs.map(job => {
        const salaryRange = job.salary_min && job.salary_max
            ? `<div class="job-salary">💰 ${(job.salary_min/1000).toFixed(0)}K - ${(job.salary_max/1000).toFixed(0)}K</div>`
            : '';

        // Determine button text based on source
        const isRealJob = job.source && (job.source === 'greenhouse' || job.source === 'lever' || job.source === 'linkedin');
        const buttonText = isRealJob ? 'View Job →' : 'Search Similar Jobs →';
        
        // Experience level badge
        const experienceLevelMap = {
            'entry': 'Entry',
            'mid': 'Mid',
            'senior': 'Senior',
            'lead': 'Lead',
            'principal': 'Principal'
        };
        const experienceBadge = job.experience_level 
            ? `<span class="experience-badge experience-${job.experience_level}">${experienceLevelMap[job.experience_level] || job.experience_level}</span>`
            : '';

        return `
            <div class="job-card">
                <div class="job-title">${escapeHtml(job.title)}</div>
                <div class="job-company">🏢 ${escapeHtml(job.company)}</div>
                <div class="job-location">📍 ${escapeHtml(job.location)}</div>
                ${salaryRange}
                <div class="job-description">${escapeHtml(job.description)}</div>
                <div class="job-meta">
                    <span>📅 Posted: ${job.posted_date || 'Recently'}</span>
                    ${isRealJob ? '<span class="real-job-badge">✓ Real Job</span>' : ''}
                    ${experienceBadge}
                </div>
                <a href="${job.url}" target="_blank" class="job-link">
                    ${buttonText}
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M6 12l4-4-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </a>
            </div>
        `;
    }).join('');

    const paginationHtml = totalPages > 1 ? `
        <div class="pagination">
            <button onclick="changePage(${page - 1})" ${page === 1 ? 'disabled' : ''}>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M10 12L6 8l4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Previous
            </button>
            <div class="page-info">Page ${page} of ${totalPages}</div>
            <button onclick="changePage(${page + 1})" ${page === totalPages ? 'disabled' : ''}>
                Next
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M6 12l4-4-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>
    ` : `<div class="page-info" style="grid-column: 1 / -1; text-align: center; padding: 20px 0;">${total} jobs found</div>`;

    container.innerHTML = jobsHtml + paginationHtml;
}

function changePage(page) {
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    loadJobs();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}



function showStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status show ${type}`;
}

function hideStatus() {
    const status = document.getElementById('status');
    status.classList.remove('show');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

# Terms of Service & Legal Compliance

## Overview

This document outlines the legal considerations, Terms of Service (ToS) restrictions, and responsible practices for using `applyr` to scrape job postings from various job boards. **Web scraping may violate website Terms of Service**. Users are responsible for ensuring their usage complies with applicable laws and website policies.

## ⚠️ Important Legal Disclaimer

**applyr is designed for personal, non-commercial use only.** The tool implements respectful scraping practices including:
- Rate limiting (2-second default delay between requests)
- Minimal server load (personal job tracking, not bulk harvesting)
- Standard browser headers (not attempting to hide activity)
- Error handling (respects 403/blocking responses)

**You use this tool at your own risk.** The developers of applyr are not responsible for any violations of Terms of Service or legal consequences resulting from your use of this software.

## Supported Job Boards & Their Policies

### SEEK (seek.com.au)

**Official Policy:**
- SEEK's Terms of Service restrict automated access without permission
- Commercial scraping is explicitly prohibited
- Official API access available for ATS/partner integrations

**applyr Implementation:**
- Personal use scope (individual job applications)
- Respectful rate limiting (2+ second delays)
- Standard browser-like headers
- Content filtering to extract only job descriptions

**Recommendations:**
- Use for personal job search activities only
- Do not bulk scrape or republish SEEK content
- Respect SEEK's robots.txt directives
- For commercial use, contact SEEK about API access

**Official Resources:**
- Terms of Service: https://www.seek.com.au/terms
- Contact: https://www.seek.com.au/about/

---

### Employment Hero (jobs.employmenthero.com)

**Official Policy:**
- Employment Hero hosts job listings for their client companies
- Terms of Service likely restrict automated scraping
- No public API documented for job retrieval

**applyr Implementation:**
- Personal use for job applications
- Respectful headers and rate limiting
- Minimal server impact

**Recommendations:**
- Use for tracking jobs you intend to apply for
- Do not bulk scrape or redistribute content
- Respect individual company postings
- For integration needs, contact Employment Hero

**Official Resources:**
- Website: https://www.employmenthero.com/

---

### Indeed (indeed.com / au.indeed.com)

✅ **SUPPORTED VIA MANUAL IMPORT** ✅

**Official Policy:**
- Indeed's Terms of Service **explicitly prohibit** automated web scraping without written permission
- Violating ToS may breach Computer Fraud and Abuse Act (CFAA) in the U.S.
- Official APIs available for authorized partners (ATS, publishers) only

**applyr's Compliant Approach: Manual Import**

applyr supports Indeed via **manual text file import** instead of automated scraping:

**How It Works:**
1. User visits Indeed job page in browser (normal use)
2. User manually copies page content (Cmd+A, Cmd+C / Ctrl+A, Ctrl+C)
3. User saves content to `data/raw/jobs/{job_id}.txt`
4. User runs `applyr add-job {job_id}` or `applyr add-job "{url}"`
5. System reads text file and extracts job data (no web requests to Indeed)

**Why This Is Compliant:**
- ✅ **No automated scraping**: User manually views and copies content
- ✅ **No circumvention**: No attempts to bypass Indeed's anti-bot measures
- ✅ **Personal use**: User copies content they're viewing for their own job tracking
- ✅ **No HTTP requests**: System only processes user-provided text files
- ✅ **Standard browser use**: User interacts with Indeed normally

**Why Automated Scraping Is Not Used:**

1. **Active Blocking (403 Errors)**
   - Indeed actively detects and blocks automated scraping attempts
   - Returns 403 Forbidden responses to non-browser clients
   - Sophisticated fingerprinting technology prevents automated access
   - More aggressive anti-bot measures than other job boards

2. **Official API Limitations**
   - **No job search/retrieval API**: APIs only support posting jobs TO Indeed
   - **Partner-only access**: Requires business partnership agreements
   - **Not for individuals**: Designed for ATS/recruitment platforms at enterprise scale
   - **Commercial pricing**: Undisclosed costs, not available to personal users

3. **Available APIs (All Partner-Only)**
   - **Job Sync API**: Post jobs TO Indeed (employers/ATS)
   - **Disposition Sync API**: Sync candidate status updates
   - **Indeed Apply**: Application process integration
   - All require business partnership, OAuth 2.0, and commercial agreements

**Usage Instructions:**

```bash
# 1. Visit https://au.indeed.com/viewjob?jk=cc76be5d850127ec
# 2. Select all (Cmd+A or Ctrl+A) and copy (Cmd+C or Ctrl+C)
# 3. Save to data/raw/jobs/cc76be5d850127ec.txt
# 4. Run command:
applyr add-job cc76be5d850127ec
# or
applyr add-job "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"
```

See `data/raw/jobs/README.md` for detailed instructions.

**Trade-offs:**
- ✅ **Pros**: ToS compliant, no blocking, integrates with applyr
- ⚠️ **Cons**: Requires manual copy/paste step (not fully automated)

**Official Resources:**
- Terms of Service: https://www.indeed.com/legal
- API Documentation: https://docs.indeed.com/
- Partnership Inquiries: https://www.indeed.com/hire

---

## Legal Considerations

### Web Scraping Legality

Web scraping exists in a legal gray area:

**Generally Legal:**
- Accessing publicly available information
- Personal, non-commercial use
- Respecting robots.txt
- Not circumventing technical barriers

**Potentially Illegal:**
- Violating explicit Terms of Service
- Commercial scraping without permission
- Bypassing access controls or authentication
- Causing excessive server load or harm
- Republishing copyrighted content

**Relevant Laws:**
- **Computer Fraud and Abuse Act (CFAA)** - U.S. law prohibiting unauthorized computer access
- **Copyright Law** - Job postings may be copyrighted content
- **Contract Law** - ToS violations may constitute breach of contract
- **Data Protection Laws** - GDPR, CCPA may apply to personal data handling

### Best Practices for Legal Compliance

1. **Use for Personal Purposes Only**
   - Track jobs you're actively applying to
   - Do not create commercial databases
   - Do not republish or sell scraped content

2. **Respect Rate Limiting**
   - Use default delays (2+ seconds between requests)
   - Do not modify rate limits to scrape faster
   - Stop if you receive 403/blocking responses

3. **Honor robots.txt**
   - Check each site's robots.txt file
   - Respect disallowed paths
   - Follow crawl-delay directives

4. **Consider Official APIs**
   - Use official APIs when available
   - Contact sites about partnership opportunities
   - Respect API rate limits and quotas

5. **Minimize Server Impact**
   - Scrape only what you need (individual jobs)
   - Cache results to avoid repeated requests
   - Use off-peak hours when possible

## applyr's Built-in Protections

### Rate Limiting
- **Default delay**: 2.0 seconds between requests
- **Configurable**: Users can increase (but not decrease) delays
- **Enforced**: Automatic sleep between all requests
- **Logged**: All requests are logged for transparency

### ToS Warnings
- **First-use warnings**: Displayed on first scrape per source
- **Documentation**: This comprehensive ToS guide
- **Logging**: All scraping activity logged with warnings
- **Error handling**: Graceful handling of 403/blocking

### Respectful Headers
- **Browser-like**: Standard User-Agent strings
- **Transparent**: Does not hide scraping activity
- **Standard protocols**: Uses normal HTTP requests
- **No circumvention**: Does not bypass security measures

### Personal Use Scope
- **Individual jobs**: Designed for one-by-one tracking
- **Application focus**: Tied to application workflow
- **No bulk features**: No mass harvesting capabilities
- **Database tracking**: Links to personal application records

## User Responsibilities

As a user of applyr, you are responsible for:

1. **Reading and Understanding ToS**
   - Review Terms of Service for each job board you scrape
   - Understand legal risks in your jurisdiction
   - Comply with all applicable laws

2. **Using Responsibly**
   - Personal job search use only
   - Do not bulk scrape or create job databases
   - Do not republish or sell scraped content
   - Respect anti-bot measures

3. **Accepting Consequences**
   - You assume all legal risk
   - Developers are not liable for ToS violations
   - You may face account bans or legal action
   - Consult legal counsel if uncertain

4. **Staying Informed**
   - Monitor changes to website ToS
   - Check for official API availability
   - Update applyr regularly for compliance improvements

## Official API Alternatives

If you need more robust, legal access to job data, consider these official alternatives:

### SEEK
- **Partner Program**: For ATS and technology partners
- **Contact**: Reach out to SEEK about API access
- **Use Case**: Commercial job board integrations

### Indeed
- **Publisher API**: For job listing websites (revenue sharing)
- **Job Sync API**: For ATS partners to post jobs
- **Application**: https://docs.indeed.com/
- **Requirements**: Business entity, compliance review

### General Alternatives
- **Adzuna API**: Public job search API with free tier
- **The Muse API**: Job board with official API
- **Reed API**: UK jobs with free API access
- **JobsDB**: Asian markets with partner programs

## When NOT to Use applyr

Do not use applyr if:

- You need to scrape hundreds or thousands of jobs
- You want to create a public job database
- You plan to republish job listings
- You're building a commercial product
- You've received cease-and-desist notices
- You're in a jurisdiction with strict CFAA enforcement
- The website explicitly blocks your requests

**Instead**: Contact the job board about official API access or partnership opportunities.

## Getting Help

### Legal Questions
- Consult a lawyer familiar with web scraping law
- Review Terms of Service for specific sites
- Check local laws in your jurisdiction

### Technical Questions
- Open an issue on GitHub
- Check documentation in docs/
- Review code in applyr/ for implementation details

### Reporting Issues
- If applyr is causing server issues, stop immediately
- Report ToS violations or concerns via GitHub issues
- Suggest improvements to responsible scraping practices

## Updates to This Document

This document will be updated as:
- Job board policies change
- Legal precedents are established
- New official APIs become available
- Community feedback is received

Last Updated: October 2025

---

## Summary

**Use applyr responsibly:**
- ✅ Personal job application tracking
- ✅ Individual job postings you intend to apply for
- ✅ Respectful rate limiting and delays
- ✅ Awareness of legal risks
- ❌ Bulk scraping or database creation
- ❌ Commercial use or republishing
- ❌ Circumventing anti-bot measures
- ❌ Ignoring ToS violations

**Remember**: You are responsible for your use of this tool. When in doubt, use official APIs or manual methods instead.

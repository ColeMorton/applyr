# Job Ranking Command (Simplified)

**ROLE:** You are an expert career advisor and software engineer specializing in job market analysis. Your task is to analyze personal files, rank job opportunities, and update a CSV database with rankings.

## STEP 0: PERSONAL PROFILE ANALYSIS

**Read and analyze personal documentation directly** to obtain comprehensive understanding:

**Personal File Intelligence Sources:**
1. **Ultimate Source of Truth**: `data/raw/personal/resume.html` - Complete professional profile and ATS-optimized format
2. **Technical Capabilities**: `data/raw/personal/skills.md` - LinkedIn-endorsed technical skills and experience timeline
3. **Career History**: `data/raw/personal/work_experience.md` - Detailed career achievements and progression
4. **Current Context**: `data/raw/personal/recent_history.md` - Recent transitions, motivations, and relocations
5. **Honest Assessment**: `data/raw/personal/reality_check.md` - Self-assessment, concerns, and authentic challenges

**Personal Intelligence Extraction:**
- Extract current technology stack (React, TypeScript, Node.js, etc.)
- Identify domain expertise and experience level (11+ years)
- Understand career goals (mid/senior roles, collaborative culture, growth opportunity)
- Recognize genuine concerns and interview preparation areas
- Map lifestyle preferences and location context (Brisbane, Australia relocation)
- Understand compensation expectations balanced with market re-entry positioning

**Use this personal context** to inform all job alignment scoring and risk assessment throughout the ranking process.

## STEP 0.5: RANK RESET & VALIDATION

1. **Clear All Existing Ranks**: Set ALL rank values to empty/null in `data/raw/advertisements.csv`
   - Use `df['rank'] = pd.NA` or `df['rank'] = ''` to clear all ranks
   - **CRITICAL**: This applies to ALL rows regardless of status
2. **Verify Rank Clearing**: Confirm that every single row has an empty rank value
   - Count non-empty ranks (should be 0)
   - Report how many ranks were cleared
3. **Validate Status Distribution**: Count jobs by status to ensure proper filtering scope
4. **Prepare Clean Dataset**: Ensure only discovered jobs will receive new rankings
5. **Data Integrity Check**: Verify that no jobs with non-"discovered" status retain rank values

## STEP 1: JOB DISCOVERY & FILTERING

1. Read `data/raw/advertisements.csv`
2. **Strictly filter** for all jobs where `status = "discovered"` (NO OTHER STATUSES)
3. **Validate filtering**: Ensure no jobs with status "applied", "rejected", "closed", or "second_round" are included
4. For each discovered job, read the corresponding markdown file from `data/outputs/job_descriptions/`
5. Create a comprehensive list of all discovered opportunities

## STEP 2: RANKING METHODOLOGY

Use this **4-Factor Weighted Scoring Framework**:

### Technical Alignment (50% weight)
- **Perfect Match (90-100%)**: React/TypeScript/Node.js stack, modern practices
- **Strong Match (70-89%)**: Frontend primarily, Full-stack
- **Moderate Match (50-69%)**: Adjacent technologies, learnable gap
- **Poor Match (0-49%)**: Major technology mismatch

### Career Goals Alignment (20% weight)
- **Ideal (90-100%)**: Mid/Senior role, collaborative culture, growth opportunity
- **Good (70-89%)**: Appropriate level, good team environment
- **Acceptable (50-69%)**: Some compromise on level or culture
- **Poor (0-49%)**: Junior positioning or poor cultural fit

### Compensation & Benefits (15% weight)
- **Excellent (90-100%)**: $120K+ or premium hourly, great benefits
- **Good (70-89%)**: Market rate with decent benefits
- **Fair (50-69%)**: Below market but acceptable
- **Poor (0-49%)**: Significantly underpaid

### Risk Assessment (15% weight) - INVERSE SCORING
- **Low Risk (90-100%)**: Stable company, portfolio-focused interviews
- **Medium Risk (70-89%)**: Some coding tests but collaborative
- **High Risk (50-69%)**: Intensive technical interviews
- **Very High Risk (0-49%)**: Heavy whiteboard/algorithm focus

## STEP 3: RANKING EXECUTION

For each discovered job:
1. **Analyze** job description against personal profile insights from Step 0
2. **Score** using 4-factor framework with detailed justification based on personal context
3. **Calculate** weighted total score (0-100%)
4. **Assign** preliminary rank based on score

## STEP 4: CSV UPDATE WITH STRICT FILTERING

1. **Initialize Rank Column**: Add `rank` column to `advertisements.csv` if it doesn't exist
2. **Clear All Ranks**: Set ALL rank values to empty/null (implementing Step 0.5 requirement)
3. **Filter Strictly**: Extract ONLY jobs where `status="discovered"` for ranking
4. **Validate Exclusions**: Confirm jobs with status "applied", "rejected", "closed", "second_round", "phone_call", "interested" are excluded from ranking
   - **CHECKPOINT**: Print count of excluded jobs by status
   - **CHECKPOINT**: Assert no excluded status jobs are in the ranking dataset
5. **Apply Integer Rankings**: Assign ranks 1, 2, 3... ONLY to discovered jobs:
   - Rank 1 = Highest scoring job (integer, not 1.0)
   - Rank 2 = Second highest (integer, not 2.0), etc.
   - **CRITICAL**: Use `range(1, n+1)` to ensure integer type
   - **CRITICAL**: No other status types receive ranks
6. **Data Integrity Verification**: Multi-point validation
   - **CHECKPOINT**: Count non-discovered jobs with rank values (must be 0)
   - **CHECKPOINT**: Verify all rank values are integers, not floats
   - **CHECKPOINT**: Verify rank sequence is consecutive (1, 2, 3... no gaps)
7. **Preserve** all existing data and formatting
8. **Final Validation**: Confirm no data corruption occurred during update

## STEP 5: TOP JOBS DETAILED DISPLAY

After successfully updating the CSV with rankings, provide a **focused analysis of the highest-value opportunities**:

1. **Top 10 Ranked Jobs Table**: Display a comprehensive table with the following columns:
   ```
   | Rank | Company | Job Title | Total Score | Tech Match | Career Fit | Comp | Risk | Key Strengths |
   ```
   - Show ranks 1-10 (or fewer if less than 10 discovered jobs exist)
   - Include all scoring components for transparency
   - Add a "Key Strengths" column highlighting 2-3 primary advantages

2. **Executive Summary**: Provide a brief overview paragraph:
   - Total number of discovered jobs ranked
   - Score range (highest to lowest)
   - Primary patterns in top-ranked opportunities (e.g., "Top 5 are all senior React roles")

3. **Top 3 Deep Dive**: For ranks 1-3, provide detailed analysis:
   - **Job Title & Company**: Full details with job_id reference
   - **Overall Score**: Weighted total with breakdown
   - **Technical Alignment**: Specific technology matches and gaps
   - **Career Goals Fit**: Why this role aligns with career trajectory
   - **Compensation Assessment**: Salary expectations and benefits analysis
   - **Risk Profile**: Interview process expectations and preparation needs
   - **Strategic Recommendation**: Specific advice for application and interview approach

4. **Application Priority Strategy**: Recommend optimal application sequence
   - Which jobs to apply to immediately (top 3-5)
   - Which to monitor for updates
   - Any timing considerations (e.g., application deadlines)

**Output Format Example:**
```markdown
## Top 10 Discovered Jobs - Ranked by Overall Fit

| Rank | Company | Job Title | Score | Tech | Career | Comp | Risk | Key Strengths |
|------|---------|-----------|-------|------|--------|------|------|---------------|
| 1 | Codafication | Software Engineer | 94 | 95 | 92 | 90 | 95 | Perfect React/TS stack, Senior level, Portfolio-focused |
| 2 | iSelect | Senior Software Engineer | 88 | 90 | 85 | 85 | 90 | CMS expertise valued, Growth opportunity |
...

**Executive Summary**: Ranked 18 discovered jobs with scores ranging from 94 to 52. Top 5 positions are all senior-level roles featuring React/TypeScript stacks with collaborative interview processes.

### Rank 1: Software Engineer - Codafication (Job ID: 87545275)

**Overall Score: 94/100**
- Technical Alignment: 95/100 (50% weight) = 47.5
- Career Goals: 92/100 (20% weight) = 18.4
...

[Detailed analysis continues]
```

## EXPECTED OUTPUT

Provide the following comprehensive analysis and validation report:

1. **Rank Reset Confirmation**: Report how many existing ranks were cleared from all jobs
2. **Status Validation Report**: Count of jobs by status and confirmation that only "discovered" jobs were ranked
3. **Top 10 Ranked Jobs Table** (as specified in Step 5): Comprehensive table with all scoring components
4. **Executive Summary** (as specified in Step 5): Overview of ranking results and patterns
5. **Top 3 Deep Dive Analysis** (as specified in Step 5): Detailed breakdown with strategic recommendations
6. **Application Priority Strategy** (as specified in Step 5): Optimal application sequence and timing
7. **CSV update confirmation** showing the rank column has been added/updated correctly with INTEGER values
8. **Data Integrity Verification**: Explicit confirmation that:
   - NO jobs with status "applied", "rejected", "closed", "phone_call", "interested", or "second_round" have rank values
   - ALL rank values are integers (1, 2, 3), NOT floats (1.0, 2.0, 3.0)
   - Rank sequence is consecutive with no gaps

**Required Validation Checks:**
- Total count of jobs ranked (should equal count of "discovered" jobs)
- Confirmation that all non-"discovered" jobs have empty rank values
- Verification that rank sequence is consecutive (1, 2, 3... with no gaps)
- Error reporting if any data integrity issues are found

## EXECUTION REQUIREMENTS

- **Autonomous operation**: Complete all steps without user intervention
- **Direct file reading**: Read all personal profile files directly in Step 0
- **Data preservation**: Don't modify any data except adding/updating rank column
- **Comprehensive analysis**: Read ALL personal files and ALL job descriptions
- **Consistent scoring**: Apply framework uniformly across all opportunities
- **Professional output**: Career advisor quality analysis and recommendations

**BEGIN EXECUTION NOW.**

---

## CSV Manipulation Specifications

**Current CSV Structure:**
```
job_id,company_name,job_title,source,status,priority,date_discovered,date_applied,date_closed,notes,salary_min,salary_max,location,url
```

**Required Modifications:**
1. **Add `rank` column** after existing columns (position 15)
2. **Update only** jobs with `status="discovered"`
3. **Rank values**: 1, 2, 3, etc. (1 = highest scoring opportunity)
4. **Preserve** all existing data, formatting, and column order
5. **Leave rank empty** for jobs with other statuses (applied, rejected, etc.)

**Implementation Steps:**
```python
# Pseudo-code for CSV manipulation with strict filtering
import pandas as pd

1. Read advertisements.csv into DataFrame
   df = pd.read_csv('data/raw/advertisements.csv')

2. **CLEAR ALL RANKS**: Set df['rank'] = pd.NA for ALL rows
   df['rank'] = pd.NA  # Clear ALL existing ranks

3. **VERIFY CLEARING**: Confirm all ranks are empty
   assert df['rank'].notna().sum() == 0, "Rank clearing failed"

4. **STRICT FILTERING**: discovered_jobs = df[df['status'] == 'discovered'].copy()

5. **VALIDATE EXCLUSIONS**: Ensure no jobs with other statuses are included
   excluded_statuses = ['applied', 'rejected', 'closed', 'second_round', 'phone_call', 'interested']
   assert not any(discovered_jobs['status'].isin(excluded_statuses)), "Non-discovered jobs found"

6. Calculate scores for each discovered job and sort by score (descending)
   discovered_jobs['score'] = [calculate_score(job) for job in discovered_jobs]
   discovered_jobs = discovered_jobs.sort_values('score', ascending=False).reset_index(drop=True)

7. **ASSIGN INTEGER RANKS**: Ranks MUST be integers (1, 2, 3...), NOT decimals (1.0, 2.0, 3.0)
   discovered_jobs['rank'] = range(1, len(discovered_jobs) + 1)  # Pure integers

8. **SELECTIVE UPDATE**: Update rank values ONLY for discovered jobs in original DataFrame
   df.loc[df['status'] == 'discovered', 'rank'] = discovered_jobs.set_index(df[df['status'] == 'discovered'].index)['rank']

9. **FINAL VERIFICATION**:
   - Confirm all non-discovered jobs have empty rank values
   - Confirm all rank values are integers (not floats like 1.0, 2.0)
   - Confirm rank sequence is consecutive (1, 2, 3... no gaps)
   non_discovered_with_ranks = df[(df['status'] != 'discovered') & (df['rank'].notna())]
   assert len(non_discovered_with_ranks) == 0, f"Found {len(non_discovered_with_ranks)} non-discovered jobs with ranks"

10. Write back to advertisements.csv with integer rank preservation
    df.to_csv('data/raw/advertisements.csv', index=False, na_rep='')
```

**Critical Requirements:**
- **Rank Clearing**: ALL existing ranks must be cleared before new ranking
- **Integer Ranks Only**: Ranks MUST be integers (1, 2, 3), NOT floats (1.0, 2.0, 3.0)
- **Status Validation**: ONLY jobs with status="discovered" receive ranks
- **Data Integrity**: All other statuses must have empty rank values
- **No Exceptions**: Zero tolerance for ranking jobs with non-"discovered" status
- **CSV Writing**: Use `na_rep=''` in `to_csv()` to write empty strings for missing ranks, not "NA" or "NaN"

This command provides high-quality analysis with consistent scoring methodology and professional strategic insights. The command will autonomously update your `advertisements.csv` with rankings that prioritize your highest-probability opportunities for Australian tech market success.

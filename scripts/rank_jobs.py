#!/usr/bin/env python3
"""
Job Ranking Script - Autonomous job analysis and ranking
Analyzes job opportunities against personal profile and updates CSV with rankings
"""

from pathlib import Path

import pandas as pd

# Personal profile summary
PROFILE = {
    "tech_stack": {
        "primary": ["React", "TypeScript", "JavaScript", "Node.js", "Python"],
        "frontend": ["Vue.js", "Angular", "Astro", "TailwindCSS", "styled-components"],
        "backend": [".NET", "C#", "Express.js", "GraphQL"],
        "data": ["Pandas", "NumPy", "PostgreSQL", "SQL Server"],
        "modern_tools": ["Claude Code", "Cursor", "GitHub", "Docker", "AWS"],
    },
    "experience_years": 11,
    "domain_expertise": ["fintech", "finance", "healthcare", "enterprise"],
    "career_goals": ["senior role", "collaborative team", "modern stack", "growth opportunity"],
    "concerns": ["coding tests", "whiteboard interviews", "algorithm challenges"],
    "location": "Brisbane, Australia",
    "status": "Recently relocated, seeking team environment after 4 years self-employment",
}


def load_job_description(job_id: str) -> str:
    """Load job description markdown file"""
    job_dir = Path("data/outputs/job_descriptions")

    # Find matching file
    pattern = f"{job_id}_*.md"
    matches = list(job_dir.glob(pattern))

    if matches:
        return matches[0].read_text()
    return ""


def score_technical_alignment(job_desc: str) -> tuple[float, str]:
    """Score technical stack alignment (40% weight)"""
    job_lower = job_desc.lower()

    # Check for perfect match indicators
    react_score = 30 if "react" in job_lower else 0
    ts_score = 25 if "typescript" in job_lower else 0
    node_score = 20 if "node" in job_lower or "nodejs" in job_lower else 0
    modern_fe_score = 15 if any(tech in job_lower for tech in ["vue", "angular", "astro"]) else 0
    python_score = 10 if "python" in job_lower else 0

    total = react_score + ts_score + node_score + modern_fe_score + python_score

    # Legacy or poor match penalties
    if "wordpress" in job_lower or "php" in job_lower:
        total *= 0.5

    if "java" in job_lower and "javascript" not in job_lower:
        total *= 0.7

    # Score mapping
    if total >= 80:
        score, reason = 95, "Perfect stack: React/TypeScript/Node.js"
    elif total >= 60:
        score, reason = 85, "Strong modern stack alignment"
    elif total >= 40:
        score, reason = 70, "Moderate stack overlap"
    elif total >= 20:
        score, reason = 55, "Some stack overlap, learnable gap"
    else:
        score, reason = 35, "Major technology mismatch"

    return score, reason


def score_career_alignment(job_desc: str, job_title: str) -> tuple[float, str]:
    """Score career goals alignment (25% weight)"""
    job_lower = job_desc.lower()
    title_lower = job_title.lower()

    # Level assessment
    is_senior = "senior" in title_lower or "lead" in title_lower or "principal" in title_lower
    is_mid = "mid" in title_lower or "developer" in title_lower or "engineer" in title_lower
    is_junior = "junior" in title_lower or "graduate" in title_lower or "grad" in title_lower

    # Culture indicators
    collaborative = any(word in job_lower for word in ["collaborate", "team", "agile", "pair programming"])
    growth = any(word in job_lower for word in ["growth", "learning", "mentorship", "career development"])
    any(word in job_lower for word in ["innovation", "modern", "cutting-edge"])

    # Scoring
    if is_senior and collaborative and growth:
        score, reason = 95, "Senior role with collaborative culture and growth"
    elif is_senior and collaborative:
        score, reason = 85, "Senior role with good team environment"
    elif is_mid and collaborative:
        score, reason = 75, "Mid-level with collaborative environment"
    elif is_junior:
        score, reason = 40, "Junior positioning (underleveled)"
    else:
        score, reason = 60, "Acceptable level, standard culture"

    return score, reason


def score_compensation(job_desc: str, salary_min: float, salary_max: float) -> tuple[float, str]:
    """Score compensation and benefits (20% weight)"""
    job_lower = job_desc.lower()

    # Salary scoring (if available)
    if pd.notna(salary_min) and salary_min > 0:
        if salary_min >= 800:  # Daily rate
            score, reason = 95, f"Premium daily rate: ${salary_min}/day"
        elif salary_min >= 120000:
            score, reason = 90, f"Excellent annual: ${salary_min}+"
        elif salary_min >= 100000:
            score, reason = 75, f"Market rate: ${salary_min}+"
        elif salary_min >= 80000:
            score, reason = 60, f"Below market: ${salary_min}+"
        else:
            score, reason = 45, f"Significantly underpaid: ${salary_min}+"
    else:
        # Infer from job description
        has_benefits = any(word in job_lower for word in ["benefits", "equity", "bonus", "competitive salary"])

        if has_benefits:
            score, reason = 70, "Competitive package mentioned"
        else:
            score, reason = 60, "Compensation not specified"

    return score, reason


def score_risk_assessment(job_desc: str, company_name: str) -> tuple[float, str]:
    """Score risk factors - INVERSE (15% weight)"""
    job_lower = job_desc.lower()

    # Red flags
    coding_test = any(
        word in job_lower for word in ["coding test", "technical test", "algorithm", "whiteboard", "leetcode"]
    )
    remote_overseas = "remote" in job_lower and any(loc in job_lower for loc in ["south africa", "offshore", "global"])
    contract = "contract" in job_lower or "6 month" in job_lower
    startup = any(word in job_lower for word in ["startup", "seed", "series a"])

    # Positive indicators
    portfolio_focus = any(word in job_lower for word in ["portfolio", "github", "previous work"])
    established = any(word in company_name.lower() for word in ["group", "limited", "holdings", "pty ltd"])

    # Scoring (higher = lower risk)
    if coding_test:
        score, reason = 40, "High risk: Coding tests/algorithms mentioned"
    elif remote_overseas:
        score, reason = 50, "Medium-high risk: Remote offshore role"
    elif contract:
        score, reason = 70, "Medium risk: Contract position"
    elif startup and not established:
        score, reason = 75, "Medium risk: Early-stage startup"
    elif portfolio_focus:
        score, reason = 95, "Low risk: Portfolio-focused interviews"
    elif established:
        score, reason = 85, "Low risk: Established company"
    else:
        score, reason = 70, "Medium risk: Standard interview process"

    return score, reason


def calculate_weighted_score(tech: float, career: float, comp: float, risk: float) -> float:
    """Calculate final weighted score"""
    return (tech * 0.40) + (career * 0.25) + (comp * 0.20) + (risk * 0.15)


def analyze_job(job_id: str, company: str, title: str, salary_min: float, salary_max: float) -> dict:
    """Comprehensive job analysis"""
    job_desc = load_job_description(job_id)

    if not job_desc:
        return {
            "job_id": job_id,
            "company": company,
            "title": title,
            "tech_score": 0,
            "tech_reason": "Job description not found",
            "career_score": 0,
            "career_reason": "N/A",
            "comp_score": 0,
            "comp_reason": "N/A",
            "risk_score": 0,
            "risk_reason": "N/A",
            "total_score": 0,
            "rank": 999,
        }

    tech_score, tech_reason = score_technical_alignment(job_desc)
    career_score, career_reason = score_career_alignment(job_desc, title)
    comp_score, comp_reason = score_compensation(job_desc, salary_min, salary_max)
    risk_score, risk_reason = score_risk_assessment(job_desc, company)

    total_score = calculate_weighted_score(tech_score, career_score, comp_score, risk_score)

    return {
        "job_id": job_id,
        "company": company,
        "title": title,
        "tech_score": tech_score,
        "tech_reason": tech_reason,
        "career_score": career_score,
        "career_reason": career_reason,
        "comp_score": comp_score,
        "comp_reason": comp_reason,
        "risk_score": risk_score,
        "risk_reason": risk_reason,
        "total_score": round(total_score, 1),
    }


def main():
    """Main execution"""
    print("=" * 80)
    print("JOB RANKING ANALYSIS - AUTONOMOUS EXECUTION")
    print("=" * 80)

    # Load CSV
    csv_path = Path("data/raw/advertisements.csv")
    df = pd.read_csv(csv_path)

    # Filter discovered jobs
    discovered = df[df["status"] == "discovered"].copy()
    print(f"\n✓ Found {len(discovered)} discovered jobs")

    # Analyze all jobs
    print(f"\n🔍 Analyzing {len(discovered)} job opportunities...")
    results = []

    for _idx, row in discovered.iterrows():
        job_id = str(row["job_id"])
        company = row["company_name"]
        title = row["job_title"]
        salary_min = row.get("salary_min", 0)
        salary_max = row.get("salary_max", 0)

        analysis = analyze_job(job_id, company, title, salary_min, salary_max)
        results.append(analysis)
        print(f"  • {company}: {analysis['total_score']:.1f}%")

    # Sort by score and assign ranks
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("total_score", ascending=False).reset_index(drop=True)
    results_df["rank"] = range(1, len(results_df) + 1)

    # Update original dataframe
    print("\n📊 Updating CSV with rankings...")

    # Add rank column if it doesn't exist
    if "rank" not in df.columns:
        df["rank"] = ""

    # Update ranks for discovered jobs
    for _, result in results_df.iterrows():
        mask = df["job_id"] == result["job_id"]
        df.loc[mask, "rank"] = result["rank"]

    # Save updated CSV
    df.to_csv(csv_path, index=False)
    print("✓ CSV updated with rankings")

    # Generate summary report
    print(f"\n{'=' * 80}")
    print("TOP 10 RANKED OPPORTUNITIES")
    print(f"{'=' * 80}\n")

    for _idx, row in results_df.head(10).iterrows():
        print(f"RANK {row['rank']}: {row['company']} - {row['title']}")
        print(f"  Total Score: {row['total_score']:.1f}%")
        print(f"  • Tech ({row['tech_score']:.0f}%): {row['tech_reason']}")
        print(f"  • Career ({row['career_score']:.0f}%): {row['career_reason']}")
        print(f"  • Comp ({row['comp_score']:.0f}%): {row['comp_reason']}")
        print(f"  • Risk ({row['risk_score']:.0f}%): {row['risk_reason']}")
        print()

    # Save detailed analysis
    analysis_path = Path("data/outputs/job_rankings_analysis.json")
    results_df.to_json(analysis_path, orient="records", indent=2)
    print(f"✓ Detailed analysis saved to: {analysis_path}")

    # Strategic insights
    print(f"\n{'=' * 80}")
    print("STRATEGIC INSIGHTS")
    print(f"{'=' * 80}\n")

    top_3 = results_df.head(3)

    print("🎯 TOP 3 PRIORITY APPLICATIONS:\n")
    for _idx, row in top_3.iterrows():
        print(f"{row['rank']}. {row['company']} - {row['title']} ({row['total_score']:.1f}%)")

    print("\n💡 RECOMMENDATIONS:")
    print("  • Focus application efforts on top 10 ranked opportunities")
    print("  • Prioritize roles with React/TypeScript/Node.js stack")
    print("  • Emphasize 11+ years experience and modern AI-augmented workflows")
    print("  • Prepare portfolio examples over algorithmic coding tests")
    print("  • Highlight recent Brisbane relocation and local commitment")

    avg_score = results_df["total_score"].mean()
    print(f"\n📈 MARKET FIT: Average score {avg_score:.1f}% indicates ", end="")
    if avg_score >= 70:
        print("strong alignment with discovered opportunities")
    elif avg_score >= 60:
        print("moderate alignment - focus on top-tier matches")
    else:
        print("weak alignment - consider expanding search criteria")

    print(f"\n{'=' * 80}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()

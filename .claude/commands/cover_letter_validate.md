# Cover Letter Validation Specialist

**Role**: Cover Letter Validation Specialist & Quality Assurance Analyst
**Parameter Required**: `job_id` (8-digit number from advertisements.csv)
**Pre-execution Required**:
- **MANDATORY**: Read and comprehensively understand `data/outputs/cover_letters/TEMPLATE.md` (template is single source of truth for validation criteria)
- Read `data/raw/advertisements.csv` to locate job by job_id
- Load job description from `data/outputs/job_descriptions/{job_id}_{company}_{role}.md`
- Load existing cover letter from `data/outputs/cover_letters/{company_slug}.md`
- **Check for Previous Validation**: Look for existing `data/outputs/validation_reports/{company_slug}_validation.json` for historical quality tracking
- Consult the **cole agent** for comprehensive personal data verification

**Output**: JSON validation report with confidence ratings (0.0-10.0 scale)

## Validation Intelligence Protocol

### Phase 1: Template Conformance & Data Source Verification

#### 1.0 Template Structure Conformance Validation
**CRITICAL FIRST VALIDATION**: All validation must be template-based
- **Template Structure Adherence**: Verify cover letter follows TEMPLATE.md structure exactly
- **Required Section Presence**: Confirm all mandatory template sections are present
- **Template Variable Population**: Validate all template variables are properly populated
- **Conditional Section Logic**: Verify appropriate conditional sections are included based on role/company analysis
- **Template Quality Standards**: Assess conformance to template's quality checklist requirements

**Template Conformance Scoring:**
- 10.0: Perfect template adherence with all variables properly populated
- 8.0-9.9: Minor deviations but core template structure maintained
- 6.0-7.9: Some template requirements missed but recognizable structure
- 4.0-5.9: Significant template deviations requiring correction
- 0.0-3.9: Major template non-conformance or missing critical sections

#### 1.1 Bullet Points Library Compliance Validation
**CRITICAL VALIDATION**: All bullet points must use standardized library content
- **Technical Stack Bullets**: Verify all {TECH_BULLET_*} variables use exact text from cover_letter.md Technical Stack Bullet Points Library
- **Domain Experience Bullets**: Confirm all {DOMAIN_BULLET_*} variables match Domain Experience Bullet Points Library exactly
- **Brisbane Establishment Bullets**: Validate all {BRISBANE_BULLET_*} variables use Brisbane Establishment Bullet Points Library text
- **No Custom Variations**: Flag any modifications, paraphrasing, or custom versions of library bullets
- **Selection Appropriateness**: Assess whether chosen bullets are relevant to specific job requirements
- **Library Currency**: Verify bullets reference most current version of library in cover_letter.md

**Bullet Points Library Compliance Scoring:**
- 10.0: Perfect library adherence with all bullets matching exactly and appropriately selected
- 8.0-9.9: Minor selection issues but exact text compliance maintained
- 6.0-7.9: Some inappropriate selections but library text preserved
- 4.0-5.9: Custom modifications detected requiring correction to library standards
- 2.0-3.9: Significant deviations from library with multiple custom variations
- 0.0-1.9: Complete disregard for library standards or major factual modifications

#### 1.2 Template Quality Standards Assessment
- **Optimal Length Check**: Verify 45-60 lines as specified in template
- **Structure Quality**: Assess clear headers, scannable format, bold emphasis per template
- **Personalization Quality**: Evaluate mission connection, cultural alignment, growth stage awareness per template standards
- **Company Type Alignment**: Verify appropriate template company-type guidance was applied
- **Conditional Section Appropriateness**: Validate correct conditional sections for role level and company type

#### 1.3 Primary Data Source Validation
- **advertisements.csv Verification**: Confirm job_id exists with complete metadata
- **Job Description File Integrity**: Validate file exists at expected location with proper naming
- **Cover Letter File Verification**: Confirm cover letter exists for target company
- **Cross-Reference Consistency**: Verify job_id mapping across all data sources
- **File Timestamp Analysis**: Check creation/modification dates for recency

**Confidence Scoring Criteria:**
- 10.0: All files exist, properly named, complete metadata
- 8.0-9.9: Minor naming inconsistencies or missing optional fields
- 6.0-7.9: Some files missing but core data intact
- 4.0-5.9: Significant data gaps requiring attention
- 0.0-3.9: Critical files missing or corrupted data

#### 1.4 Data Completeness Assessment
- **Job Requirements Extraction**: Parse technical stack, experience level, industry domain
- **Company Information Validation**: Verify company name, location, role details
- **Cover Letter Content Analysis**: Extract all factual claims for verification
- **Contact Information Validation**: Verify email, phone, portfolio links accuracy

#### 1.5 Company Analysis Discovery & Verification
- **Company Analysis Search**: Locate matching company analysis files in `data/outputs/company_analysis/*.md`
- **File Discovery Protocol**: Search for files matching company name with variations (Ltd, Pty Ltd, Technologies, etc.)
- **Analysis Recency Validation**: Check analysis file timestamp for currency (prefer recent analysis)
- **Content Integrity Check**: Verify company analysis file structure and completeness
- **Cross-Reference Validation**: Ensure company analysis matches job posting company information
- **Integration Assessment**: Evaluate if cover letter leverages available company intelligence

**Company Analysis Discovery Methodology:**
- **Primary Search**: Exact company name matching from job description
- **Secondary Search**: Fuzzy matching with business suffix normalization
- **Tertiary Search**: Keyword-based company identifier matching
- **Currency Evaluation**: Prefer most recent analysis if multiple files exist
- **No Analysis Documentation**: Record when no company analysis available for reference

**Analysis Integration Validation:**
- **Utilization Assessment**: Determine if available company analysis was properly leveraged
- **Missed Opportunity Identification**: Flag when analysis exists but wasn't used effectively
- **Integration Quality**: Evaluate accuracy and appropriateness of company insights integration

### Phase 2: Cole Agent Ground Truth Consultation

#### 2.1 Personal Intelligence Verification
**Use the cole agent** to establish ground truth baseline:
- **Employment Timeline Verification**: Cross-reference all employment dates and durations
- **Technical Experience Validation**: Verify all technology stack claims against documented experience
- **Project Claims Assessment**: Validate specific project mentions (Sensylate, Panorama Berlin, etc.)
- **Education & Certification Verification**: Confirm all educational claims
- **Location & Availability Verification**: Validate Brisbane residence and work rights
- **Career Transition Accuracy**: Verify gap period positioning and current status

#### 2.2 Evidence Citation Analysis Protocol
**Mandatory Evidence Verification for Every Major Claim:**
- **Evidence Citation Completeness**: Verify each major statement includes specific cole agent evidence reference
- **Quote Accuracy**: Confirm cover letter claims match exact cole agent response excerpts
- **Timeline Mathematical Verification**: Calculate all experience durations and verify accuracy (e.g., CharmHealth: Jan 2012 - Apr 2013 = 1.25 years)
- **Project Detail Precision**: Verify singular/plural accuracy against documented facts (one system vs multiple systems)
- **Unsupported Claim Detection**: Flag any philosophical, emotional, or inferential statements without factual backing

#### 2.3 Mathematical Accuracy Assessment
**Timeline and Quantity Verification:**
- **Experience Duration Calculations**: Mathematically verify all timeframes (Healthcare experience: specific calculation from employment dates)
- **Quantity Precision**: Verify exact numbers against cole agent evidence (team scaling: exactly "3→20" if documented)
- **Range Accuracy**: Ensure ranges reflect actual calculations, not marketing estimates
- **Aggregation Verification**: Validate combined experience claims with mathematical proof

#### 2.4 Experience-Claim Mapping Matrix
Create detailed mapping between cover letter claims and verifiable experience:
- **Direct Experience Match**: Claims backed by documented work history with exact evidence citations
- **Adjacent Experience Positioning**: How tangential experience is positioned with supporting evidence
- **Learning Claims Validation**: Verify stated learning abilities with specific examples from cole agent
- **Achievement Quantification**: Validate specific metrics with exact evidence (team scaling 3→20, etc.)

**Enhanced Confidence Scoring Methodology:**
- 10.0: Claim directly supported by documented experience with specific evidence citation and mathematical verification
- 8.0-9.9: Strong supporting evidence with minor extrapolation but accurate calculations
- 6.0-7.9: Reasonable inference from related experience with some evidence support
- 4.0-5.9: Weak supporting evidence, significant assumption, or minor mathematical inaccuracies
- 2.0-3.9: Mathematical inaccuracies, unsupported claims, or embellished language
- 0.0-1.9: False claims, major mathematical errors, or completely unsupported statements

### Phase 3: Template-Based Technical Stack Alignment Analysis

#### 3.1 Template Technical Alignment Validation
- **Template Variable Accuracy**: Verify {TECH_STACK_REQUIREMENTS} accurately lists job requirements
- **Bullet Point Selection**: Validate {TECH_BULLET_1}, {TECH_BULLET_2}, {TECH_BULLET_3}, {TECH_BULLET_4} are selected from Reusable Bullet Points Library
- **Domain Bullet Validation**: Confirm {DOMAIN_BULLET_1}, {DOMAIN_BULLET_2}, {DOMAIN_BULLET_3} match library standards
- **Brisbane Bullet Verification**: Ensure {BRISBANE_BULLET_1}, {BRISBANE_BULLET_2} use standardized location messaging
- **Learning Statement Validation**: Assess appropriateness of {LEARNING_STATEMENT} and {SKILL_TO_DEVELOP} if present
- **Library Compliance Check**: Verify all bullet points match exactly with no custom modifications

#### 3.2 Positioning Accuracy Evaluation
- **Seniority Level Alignment**: Experience level vs role requirements
- **Leadership Claims Verification**: Validate team scaling and mentorship examples
- **Industry Domain Relevance**: Assess sector experience relevance (FinTech, SaaS, etc.)
- **Remote Work Capability**: Verify remote work experience and capabilities

**Technical Confidence Calculation:**
```
Technical_Confidence = (
    (Direct_Match_Percentage * 0.4) +
    (Adjacent_Skills_Score * 0.3) +
    (Learning_Capability_Score * 0.2) +
    (Architecture_Experience_Score * 0.1)
)
```

### Phase 4: Company Analysis Integration Validation

#### 4.1 Company Intelligence Integration Assessment
**When company analysis available:**
- **Strategic Context Integration**: Evaluate use of company business model insights
- **Leadership Alignment**: Assess targeting based on leadership style and culture
- **Competitive Positioning**: Verify leveraging of company market position for differentiation
- **Cultural Intelligence Application**: Evaluate integration of company culture insights
- **Strategic Opportunity Alignment**: Assess connection of capabilities to company growth areas

**Company Analysis Integration Scoring:**
- 10.0: Exceptional integration with strategic company insights enhancing positioning
- 8.0-9.9: Strong integration with most available company intelligence utilized
- 6.0-7.9: Moderate integration with some missed opportunities
- 4.0-5.9: Limited integration despite available analysis
- 2.0-3.9: Poor integration with significant missed opportunities
- 0.0-1.9: No integration despite available company analysis

#### 4.2 Company Intelligence Accuracy Verification
- **Business Context Accuracy**: Verify company insights referenced are factually correct
- **Leadership Profile Accuracy**: Ensure leadership targeting aligns with actual company leadership
- **Strategic Direction Accuracy**: Validate references to company strategy and growth plans
- **Cultural Analysis Accuracy**: Confirm cultural insights are appropriately applied
- **Market Position Accuracy**: Verify competitive positioning references are current

#### 4.3 Integration Opportunity Assessment
**Analysis Utilization Evaluation:**
- **Available vs Used**: Compare available company intelligence with actual integration
- **Strategic Value Assessment**: Evaluate quality of integration relative to positioning enhancement
- **Missed Opportunity Identification**: Flag valuable insights not leveraged in cover letter
- **Integration Quality**: Assess natural vs forced integration of company analysis

### Phase 5: Content Quality & Professional Standards

#### 5.1 Language Precision Assessment
- **Evidence-Based Language**: Verify all statements are fact-based, not interpretive or philosophical
- **Marketing Language Detection**: Flag and score embellishment words ("exactly", "profound", "deeply", "perfect")
- **Technical Precision Scoring**: Assess use of precise technical language over marketing speak
- **Unsupported Claim Language**: Identify claims about "understanding", "responsibility", or feelings without factual backing
- **Fact-First Sentence Structure**: Evaluate whether statements lead with verifiable facts

#### 5.2 Professional Writing Assessment
- **Grammar & Syntax Analysis**: Comprehensive language quality evaluation
- **Tone Appropriateness**: Professional confidence without arrogance, precision without embellishment
- **Structure & Flow Evaluation**: Logical progression and readability with evidence-based content
- **Length & Conciseness**: Appropriate detail level for target audience with factual precision

#### 5.3 Brand Consistency Verification
- **Contact Information Accuracy**: Verify all contact details match current records
- **Portfolio Links Validation**: Check portfolio URL accessibility and relevance
- **Personal Brand Alignment**: Consistency with colemorton.com and LinkedIn
- **Professional Positioning**: Alignment with resume and other materials

#### 5.4 Cultural Fit Positioning
- **Company Values Alignment**: How well personal values connect with company culture (enhanced with analysis)
- **Communication Style Match**: Appropriate tone for company size and industry
- **Growth Mindset Demonstration**: Evidence of learning and adaptation capability

### Phase 6: Template-Based Strategic Positioning Verification

#### 6.1 Template Value Proposition Validation
- **Company Goal Alignment**: Validate company mission connection aligns appropriately with business analysis insights
- **Strategic Positioning**: Assess how technical capabilities are positioned relative to job requirements
**Verify each unique value proposition against documented evidence:**
- **Greenfield Transformation Experience**: Sensylate and project development verification
- **Design-Technical Bridge Capability**: Personal brand and design work validation
- **Remote-First Success**: Independent work period and collaboration verification
- **Brisbane Commitment**: Location and family tie verification

#### 6.2 Template-Based Competitive Advantage Assessment
- **Unique Differentiator Verification**: Validate claimed competitive advantages
- **Market Positioning Accuracy**: How positioning aligns with actual capabilities
- **Risk Mitigation Strategy**: How potential concerns are addressed

#### 6.3 Template-Enhanced Factual Accuracy Cross-Verification
- **Template Contact Information**: Verify footer contact details match template format exactly
- **Template Professional Links**: Validate all template footer links are accessible and current
- **Zero Tolerance for Embellishment**: Flag any unverifiable claims
- **Date Consistency Check**: All dates align with resume timeline
- **Achievement Verification**: Quantified achievements backed by evidence
- **Reference Point Validation**: All mentioned companies, projects, technologies verified

## Confidence Rating Methodology

### Overall Scoring Framework
- **10.0**: Exceptional - All claims fully verifiable with strong evidence
- **9.0-9.9**: Excellent - Minor uncertainties but strong overall verification
- **8.0-8.9**: Very Good - Good evidence base with some assumptions
- **7.0-7.9**: Good - Adequate verification with moderate confidence
- **6.0-6.9**: Acceptable - Some concerns but generally credible
- **5.0-5.9**: Marginal - Significant verification issues requiring attention
- **4.0-4.9**: Poor - Major credibility concerns and gaps
- **3.0-3.9**: Very Poor - Substantial false claims or misleading information
- **2.0-2.9**: Critical Issues - Potential legal or ethical concerns
- **0.0-1.9**: Unacceptable - Fraudulent or severely misleading content

### Category-Specific Weighting
```
Overall_Confidence = (
    (Template_Conformance * 0.20) +
    (Bullet_Points_Library_Compliance * 0.15) +
    (Factual_Accuracy * 0.25) +
    (Technical_Alignment * 0.20) +
    (Content_Quality * 0.15) +
    (Strategic_Positioning * 0.05)
)
```

**Template Conformance Weight Explanation:**
- **20% Weight**: Template adherence is critical for consistent quality and structure
- **Foundation Validation**: Template conformance enables all other quality assessments

**Bullet Points Library Compliance Weight Explanation:**
- **15% Weight**: Ensures consistency and evidence-based accuracy across all cover letters
- **Quality Standardization**: Library compliance eliminates variation and maintains professional standards
- **Evidence Preservation**: Pre-verified bullets maintain factual accuracy standards


## JSON Validation Report Structure

```json
{
  "validation_summary": {
    "overall_confidence": 8.7,
    "job_id": "86418322",
    "company": "PRA",
    "role": "Senior Frontend Developer",
    "cover_letter_file": "pra.md",
    "validation_timestamp": "2025-09-24T10:30:00Z",
    "validator_version": "2.0_template_driven",
    "total_claims_validated": 23,
    "template_version": "2025-09-25"
  },
  "template_conformance": {
    "overall_score": 9.2,
    "structure_adherence": {
      "score": 9.5,
      "required_sections_present": true,
      "template_variables_populated": 18,
      "template_variables_missing": 2,
      "section_order_correct": true
    },
    "bullet_points_library_compliance": {
      "score": 9.3,
      "tech_bullets_library_match": true,
      "domain_bullets_library_match": true,
      "brisbane_bullets_library_match": true,
      "custom_variations_detected": 0,
      "inappropriate_selections": 0,
      "library_currency_verified": true
    },
    "conditional_sections": {
      "score": 8.8,
      "role_level_appropriate": true,
      "company_type_alignment": "startup",
      "conditional_sections_included": ["Entrepreneurial Mindset", "Technical Stack Alignment"],
      "conditional_sections_skipped": ["Enterprise Experience"]
    },
    "quality_standards": {
      "score": 9.0,
      "optimal_length": "48 lines (within 45-60 range)",
      "clear_headers": true,
      "scannable_format": true,
      "bold_emphasis_appropriate": true,
      "professional_contact_complete": true
    },
    "personalization_quality": {
      "score": 8.9,
      "mission_connection": 9.1,
      "cultural_alignment": 8.8,
      "growth_stage_awareness": 9.0,
      "industry_expertise_relevance": 8.7,
      "location_advantage_emphasized": true
    }
  },
  "data_verification": {
    "job_data_integrity": {
      "score": 10.0,
      "job_file_exists": true,
      "csv_record_complete": true,
      "naming_convention_correct": true
    },
    "personal_data_consistency": {
      "score": 9.2,
      "cole_agent_consultation": true,
      "employment_timeline_verified": true,
      "technical_claims_validated": 22,
      "technical_claims_flagged": 1
    },
    "company_analysis_discovery": {
      "score": 8.5,
      "analysis_file_found": true,
      "analysis_file_path": "data/outputs/company_analysis/PRA_20250920.md",
      "analysis_currency": "recent",
      "analysis_completeness": 9.1,
      "company_name_match": "exact"
    },
    "cross_reference_accuracy": {
      "score": 8.8,
      "resume_alignment": 9.1,
      "portfolio_consistency": 8.5,
      "linkedin_match": 8.9,
      "company_analysis_consistency": 8.7
    }
  },
  "factual_accuracy": {
    "overall_score": 9.1,
    "evidence_citation_analysis": {
      "score": 8.8,
      "claims_with_evidence": 15,
      "unsupported_claims": 2,
      "evidence_quote_accuracy": 9.2,
      "philosophical_claims_flagged": 1
    },
    "mathematical_accuracy": {
      "score": 7.5,
      "timeline_calculations_verified": 3,
      "timeline_calculation_errors": 1,
      "quantity_precision_score": 8.2,
      "range_accuracy_score": 6.8
    },
    "language_precision": {
      "score": 8.1,
      "marketing_language_detected": 3,
      "embellishment_words_flagged": 2,
      "fact_first_structure_score": 8.5,
      "technical_precision_score": 8.8
    },
    "employment_timeline": {
      "score": 9.5,
      "claims_verified": 8,
      "claims_flagged": 0,
      "date_consistency": true,
      "duration_calculations_accurate": true
    },
    "technical_experience": {
      "score": 8.7,
      "react_experience": 9.2,
      "typescript_experience": 8.5,
      "nextjs_positioning": 7.8,
      "architecture_claims": 9.0
    },
    "project_detail_accuracy": {
      "score": 7.2,
      "singular_plural_accuracy": 6.5,
      "project_description_precision": 7.8,
      "system_count_accuracy": 5.0
    },
    "education_claims": {
      "score": 10.0,
      "degree_verified": true,
      "certifications_accurate": true
    },
    "location_statements": {
      "score": 10.0,
      "brisbane_residence": true,
      "work_rights_verified": true,
      "availability_accurate": true
    }
  },
  "technical_alignment": {
    "overall_score": 8.4,
    "required_skills_match": {
      "percentage": 85.2,
      "react_expert": 9.2,
      "typescript_expert": 8.5,
      "nextjs_experience": 6.8,
      "component_architecture": 9.1,
      "modern_css": 8.3
    },
    "positioning_accuracy": {
      "score": 8.9,
      "seniority_alignment": 8.7,
      "leadership_claims": 9.2,
      "gap_acknowledgment": 9.0
    },
    "learning_capability": {
      "score": 9.1,
      "evidence_provided": true,
      "realistic_timeline": true
    }
  },
  "content_quality": {
    "overall_score": 9.0,
    "professional_tone": {
      "score": 9.3,
      "confidence_level": "appropriate",
      "enthusiasm_balance": "excellent"
    },
    "grammar_accuracy": {
      "score": 9.8,
      "errors_found": 1,
      "readability_score": 9.5
    },
    "structure_flow": {
      "score": 8.6,
      "logical_progression": true,
      "section_balance": "good",
      "conclusion_strength": 8.8
    },
    "contact_information": {
      "score": 10.0,
      "email_verified": true,
      "portfolio_accessible": true,
      "linkedin_current": true
    }
  },
  "strategic_positioning": {
    "overall_score": 8.8,
    "value_propositions": {
      "greenfield_specialist": {
        "score": 9.2,
        "evidence": ["Sensylate platform", "Panorama Berlin app"],
        "credibility": "strong"
      },
      "design_technical_bridge": {
        "score": 8.5,
        "evidence": ["Personal brand execution", "Storybook experience"],
        "credibility": "good"
      },
      "remote_first_success": {
        "score": 9.0,
        "evidence": ["3+ years independent work", "Global collaboration"],
        "credibility": "strong"
      },
      "brisbane_commitment": {
        "score": 10.0,
        "evidence": ["Current residence", "Family ties"],
        "credibility": "verified"
      }
    },
    "competitive_advantage": {
      "score": 8.6,
      "unique_differentiators": 4,
      "market_positioning": "strong",
      "authenticity": 9.1
    }
  },
  "company_analysis_integration": {
    "overall_score": 8.3,
    "analysis_utilization": {
      "score": 8.1,
      "strategic_context_integration": 8.4,
      "leadership_alignment": 8.0,
      "cultural_intelligence_application": 8.2,
      "competitive_positioning_leverage": 8.3
    },
    "integration_quality": {
      "score": 8.5,
      "natural_integration": true,
      "forced_references": false,
      "strategic_value_added": 8.7
    },
    "missed_opportunities": {
      "count": 2,
      "severity": "minor",
      "opportunities": [
        "Could leverage company's recent technology expansion",
        "Missed opportunity to reference leadership innovation focus"
      ]
    },
    "accuracy_verification": {
      "score": 9.1,
      "business_context_accuracy": 9.2,
      "leadership_profile_accuracy": 9.0,
      "strategic_direction_accuracy": 9.1
    }
  },
  "risk_flags": [
    {
      "category": "technical_alignment",
      "severity": "low",
      "issue": "Next.js experience positioned as transferable from Astro/React",
      "recommendation": "Consider taking Next.js tutorial before interview"
    }
  ],
  "recommendations": [
    {
      "priority": "medium",
      "category": "technical_preparation",
      "action": "Review Next.js fundamentals to strengthen SSR framework claims",
      "confidence_impact": "+0.3"
    },
    {
      "priority": "low",
      "category": "content_optimization",
      "action": "Consider quantifying design system impact with specific metrics",
      "confidence_impact": "+0.2"
    }
  ],
  "validation_notes": [
    "Strong factual foundation with verifiable experience claims",
    "Technical alignment excellent for React/TypeScript requirements",
    "Strategic positioning authentic and well-supported",
    "Minor knowledge gap in Next.js appropriately acknowledged"
  ]
}
```

## Risk Detection Framework

### Critical Risk Indicators
- **Bullet Points Library Non-Compliance**: Custom variations, modifications, or complete disregard for standardized library bullets
- **Template Variable Population Errors**: Incorrect use of new bullet point variables or reverting to old variable system
- **Factual Inaccuracies**: Unverifiable employment dates, false company associations, mathematical timeline errors
- **Evidence Citation Failures**: Major claims without supporting cole agent evidence references
- **Mathematical Inaccuracies**: Timeline calculations, quantity claims, or experience duration errors
- **Language Precision Issues**: Marketing embellishment, unsupported philosophical claims, emphasis words without basis
- **Project Detail Errors**: Singular/plural inaccuracies, project description misstatements
- **Technical Overstatement**: Claiming expertise without supporting evidence
- **Timeline Inconsistencies**: Gaps or overlaps in employment history
- **Contact Information Errors**: Outdated or incorrect contact details
- **Cultural Misalignment**: Inappropriate tone for company culture

### Severity Classification
- **Critical (0.0-3.9)**: Potential legal or ethical issues requiring immediate correction
- **High (4.0-5.9)**: Significant credibility concerns affecting application success
- **Medium (6.0-7.9)**: Notable issues requiring attention before submission
- **Low (8.0-8.9)**: Minor optimization opportunities
- **Minimal (9.0-10.0)**: Negligible concerns or enhancement suggestions

## Usage Examples

```bash
# Validate cover letter for specific job
/cover_letter_validate 86418322  # PRA Senior Frontend Developer

# Would analyze:
# - Job: data/outputs/job_descriptions/86418322_PRA_Senior_Frontend_Developer.md
# - Cover Letter: data/outputs/cover_letters/pra.md
# - Personal Data: Via cole agent consultation
# - Output: Comprehensive JSON validation report with confidence ratings
```

## Integration with applyr Ecosystem

### Quality Assurance Workflow
- **Pre-Submission Validation**: Comprehensive verification before application
- **Continuous Improvement**: Iterative refinement based on validation feedback
- **Portfolio Consistency**: Ensure alignment across all application materials
- **Risk Mitigation**: Proactive identification and resolution of potential issues

### Data Flow Integration
- **Input Sources**: Job descriptions, cover letters, personal intelligence, cole agent
- **Processing Logic**: Evidence-based verification with confidence scoring
- **Output Coordination**: JSON reports for systematic quality improvement
- **Feedback Loop**: Validation insights inform cover letter optimization

This validation specialist provides template-driven institutional-grade quality assurance, ensuring TEMPLATE.md conformance, factual precision, and strategic positioning effectiveness before application submission.

**CRITICAL VALIDATION PRINCIPLE**: All validation criteria are derived from TEMPLATE.md as the single source of truth and the Reusable Bullet Points Library in cover_letter.md. Template conformance and bullet points library compliance are the foundation for all quality assessments and confidence scoring.
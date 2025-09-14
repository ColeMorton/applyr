# Company Intelligence Discover

**DASV Phase 1: Company Intelligence Data Collection and Context Gathering**

Comprehensive company intelligence collection and business research gathering for institutional-quality company analysis using systematic discovery protocols and researcher sub-agent orchestration.

## Purpose

The Company Analysis Discovery phase defines the requirements for systematic collection and initial structuring of all data required for comprehensive company intelligence analysis. This specification focuses on **what** company data is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/{SCRIPTS_BASE}/schemas/company_analysis_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute company intelligence discovery. Ensure output conforms to `/{SCRIPTS_BASE}/schemas/company_analysis_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: company_analyst
**Action**: discover
**Output Location**: `./{DATA_OUTPUTS}/company_analysis/discovery/`
**Next Phase**: company_analyst_analyze
**Template Reference**: `./{TEMPLATES_BASE}/analysis/company_analysis_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `company_name`: Company name or organization (required, normalized format)
- `depth`: Research depth - `summary` | `standard` | `comprehensive` | `deep-dive` (optional, default: comprehensive)
- `timeframe`: Research period - `1y` | `3y` | `5y` | `full_history` (optional, default: 3y)
- `confidence_threshold`: Minimum confidence for data quality - `0.6` | `0.7` | `0.8` (optional, default: 0.7)
- `validation_enhancement`: Enable validation-based enhancement - `true` | `false` (optional, default: true)

## Data Requirements

### Core Data Categories

**Company Foundation Intelligence Requirements**:
- Complete company history, founding story, and evolution timeline
- Mission, vision, and core values with cultural assessment
- Business model analysis and revenue stream identification
- Corporate structure, subsidiaries, and organizational hierarchy
- Leadership team profiles and management background analysis

**Business Operations Intelligence Requirements**:
- Product and service portfolio with market positioning
- Target customer segments and market analysis
- Technology stack, platforms, and operational infrastructure
- Geographic presence and market reach assessment
- Partnership ecosystem and strategic alliances

**Market Positioning Intelligence Requirements**:
- Industry classification and sector positioning
- Competitive landscape and competitive advantages
- Market share analysis and industry trends
- Brand reputation and public perception assessment
- Innovation initiatives and R&D investments

**Corporate Intelligence Requirements**:
- Recent news, press releases, and media coverage
- Strategic initiatives and major announcements
- Merger and acquisition activity and strategic moves
- Regulatory compliance and legal status assessment
- ESG initiatives and corporate social responsibility programs

### Quality Standards
- **Multi-Source Validation**: Cross-validation across multiple company data sources with confidence scoring
- **Comprehensive Coverage**: Overall data quality ≥ 0.90 for thorough company intelligence
- **Data Completeness**: ≥ 85% field population for comprehensive company analysis
- **Source Reliability**: ≥ 80% health score across company research services

## Output Structure and Schema

**File Naming**: `{COMPANY_NAME}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./{DATA_OUTPUTS}/company_analysis/discovery/`
**Schema Definition**: `/{SCRIPTS_BASE}/schemas/company_analysis_discovery_schema.json`

### Required Output Components
- **Company Profile**: Business description, history, mission, leadership information
- **Business Model**: Revenue streams, target markets, value proposition
- **Market Context**: Industry trends, competitive landscape, market positioning
- **Corporate Intelligence**: Recent developments, strategic initiatives, partnerships
- **Competitive Analysis**: Direct competitors with differentiation factors
- **Quality Metrics**: Confidence scores, data completeness, source reliability

### Schema Compliance Standards
- Multi-source company data validation targeting high confidence scores
- Complete discovery insights with research priorities identified
- Comprehensive company intelligence quality standards compliance

## Expected Outcomes

### Discovery Quality Targets
- **Overall Data Quality**: ≥ 97% confidence through multi-source validation
- **Data Completeness**: ≥ 92% across all required company intelligence categories
- **Company Profile Confidence**: ≥ 95% with complete business model integration
- **Source Health**: ≥ 80% operational status across company research services

### Key Deliverables
- Comprehensive company profile with business intelligence
- Multi-source validated company metrics and positioning data
- Industry context with company-specific market implications
- Competitive analysis with strategic positioning rationale
- Discovery insights identifying research priorities and intelligence gaps
- Quality assessment with confidence scoring and source reliability metrics

**Integration with DASV Framework**: This command provides the foundational company data required for the subsequent analyze phase, ensuring high-quality input for systematic company intelligence analysis.

**Author**: Cole Morton

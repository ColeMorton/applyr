# Company Intelligence Validate

**DASV Phase 4: Comprehensive DASV Workflow Validation**

Execute comprehensive validation and quality assurance for the complete company analysis DASV workflow using systematic verification methodologies via production-grade company research services and institutional quality standards targeting >9.5/10 confidence levels.

## Purpose

You are the Company Analysis Validation Specialist, functioning similarly to the content_evaluator command but specialized for comprehensive DASV workflow validation using production-grade company research services. You systematically validate ALL outputs from a complete DASV cycle (Discovery → Analysis → Synthesis) for a specific company and date, ensuring institutional-quality reliability scores >9.5/10 with a minimum threshold of 9.0/10 through multi-source company intelligence validation.

## Microservice Integration

**Framework**: DASV Phase 4
**Role**: company_analyst
**Action**: validate
**Input Parameter**: synthesis output filename (containing company name and date)
**Output Location**: `./{DATA_OUTPUTS}/company_analysis/validation/`
**Next Phase**: None (final validation phase)
**Company Research Services**: Production-grade company intelligence services for multi-source validation
**HYBRID TEMPLATE SYSTEM**:
- **Validation Standards**: `./{TEMPLATES_BASE}/analysis/company_analysis_template.md` (authoritative specification)
- **Company Research Implementation**: Enhanced company intelligence templates with validation framework
- **Compliance Verification**: Against authoritative markdown specification standards

## Parameters

### Mode 1: Single Company Validation
**Trigger**: Filename argument matching `{COMPANY_NAME}_{YYYYMMDD}.md`
- `synthesis_filename`: Path to synthesis output file (required) - format: {COMPANY_NAME}_{YYYYMMDD}.md
- `confidence_threshold`: Minimum confidence requirement - `9.0` | `9.5` | `9.8` (optional, default: 9.0)
- `validation_depth`: Validation rigor - `standard` | `comprehensive` | `institutional` (optional, default: institutional)
- `real_time_validation`: Use current company intelligence for validation - `true` | `false` (optional, default: true)

### Mode 2: DASV Phase Cross-Analysis
**Trigger**: Phase argument matching `discovery|analysis|synthesis|validation`
- `dasv_phase`: DASV phase for cross-analysis (required) - `discovery` | `analysis` | `synthesis` | `validation`
- `file_count`: Number of latest files to analyze (optional, default: 7)
- `confidence_threshold`: Minimum confidence requirement - `9.0` | `9.5` | `9.8` (optional, default: 9.0)
- `validation_depth`: Validation rigor - `standard` | `comprehensive` | `institutional` (optional, default: institutional)

**Note**: `synthesis_filename` and `dasv_phase` are mutually exclusive - use one or the other, not both.

## Parameter Detection and Execution Flow

### Argument Parsing Logic
```bash
# Command Invocation Examples:
/company_analysis:validate Apple_Inc_20250725.md          # Single Company Mode
/company_analysis:validate analysis                        # DASV Cross-Analysis Mode
/company_analysis:validate discovery --file_count=5       # DASV Cross-Analysis Mode (custom count)
```

**Detection Algorithm**:
1. If argument matches pattern `{COMPANY_NAME}_{YYYYMMDD}.md` → Single Company Validation Mode
2. If argument matches `discovery|analysis|synthesis|validation` → DASV Phase Cross-Analysis Mode
3. If no arguments provided → Error: Missing required parameter
4. If invalid argument → Error: Invalid parameter format

### Execution Routing
- **Single Company Mode**: Extract company name and date from filename, validate complete DASV workflow
- **DASV Cross-Analysis Mode**: Analyze latest files in specified phase directory for consistency

### Parameter Validation Rules
- **Mutually Exclusive**: Cannot specify both synthesis_filename and dasv_phase
- **Required**: Must specify either synthesis_filename OR dasv_phase
- **Format Validation**: synthesis_filename must match exact pattern {COMPANY_NAME}_{YYYYMMDD}.md
- **Phase Validation**: dasv_phase must be one of the four valid DASV phases

### Error Handling for Invalid Parameters
- **Invalid Filename Format**: Must match {COMPANY_NAME}_{YYYYMMDD}.md pattern exactly
- **Non-existent Phase**: Phase must be discovery, analysis, synthesis, or validation
- **Missing Required Parameters**: Must provide either filename or phase argument
- **Conflicting Parameters**: Cannot combine single company and cross-analysis modes

## DASV Phase Cross-Analysis Methodology

**Purpose**: Validate consistency, quality, and company-specificity across the latest files within a specific DASV phase to ensure systematic analysis quality and eliminate hardcoded template artifacts.

### Cross-Analysis Framework

**File Discovery and Selection**:
- Automatically locate latest 7 files (configurable) in specified phase directory
- Sort by modification timestamp for most recent analysis outputs
- Phase-specific directory mapping:
  - `discovery`: `./{DATA_OUTPUTS}/company_analysis/discovery/`
  - `analysis`: `./{DATA_OUTPUTS}/company_analysis/analysis/`
  - `synthesis`: `./{DATA_OUTPUTS}/company_analysis/` (root level)
  - `validation`: `./{DATA_OUTPUTS}/company_analysis/validation/`

### Core Validation Dimensions

#### 1. Structural Consistency Analysis
**Objective**: Ensure uniform structure and format compliance across phase outputs
```
STRUCTURAL VALIDATION PROTOCOL:
- JSON Schema Consistency: Validate all files follow identical structure
- Required Field Verification: Confirm all mandatory fields are present
- Data Type Consistency: Ensure consistent field types across files
- Metadata Format Compliance: Verify consistent metadata structure
- Confidence Score Format: Validate decimal format (0.0-1.0) consistency
- Company Research Integration: Confirm consistent research service utilization patterns
- Overall Structural Score: 9.0+/10.0 for institutional quality
```

#### 2. Hardcoded/Magic Value Detection
**Objective**: Identify and flag non-company-specific repeated values that indicate template artifacts
```
MAGIC VALUE DETECTION FRAMEWORK:
- Repeated String Patterns: Detect identical non-company strings across files
- Numerical Value Analysis: Flag suspicious repeated numbers not related to company data
- Template Artifact Identification: Identify placeholder text or example values
- Generic Description Detection: Find non-specific company descriptions
- Default Value Flagging: Identify unchanged template defaults
- Threshold: <5% repeated non-company-specific content for institutional quality
```

#### 3. Company Specificity Validation
**Objective**: Ensure all data and analysis content is appropriately specific to each company
```
COMPANY SPECIFICITY ASSESSMENT:
- Company Name Accuracy: Verify correct company names match business entities
- Industry Classification: Confirm sector/industry assignments are company-specific
- Business Intelligence Uniqueness: Validate company data varies appropriately by organization
- Business Model Descriptions: Ensure company-specific business model analysis
- Competitive Analysis Specificity: Verify company-appropriate competitive positioning
- Company Data Correlation: Confirm business metrics and market position align with company
- Specificity Score: 9.5+/10.0 for institutional company-specific analysis
```

#### 4. Company Research Integration Consistency
**Objective**: Validate consistent and appropriate use of company research services across phase files
```
COMPANY RESEARCH INTEGRATION VALIDATION:
- Research Service Utilization Patterns: Verify consistent company research service usage
- Data Source Attribution: Confirm proper company research service citations
- Quality Score Consistency: Validate company intelligence confidence scoring alignment
- Source Health Documentation: Ensure company research operational status tracking
- Multi-Source Validation: Confirm cross-validation across company intelligence sources
- Research Integration Score: 9.0+/10.0 for production-grade integration
```

### Cross-Analysis Output Structure

**File Naming**: `{PHASE}_cross_analysis_{YYYYMMDD}_validation.json`
**Location**: `./{DATA_OUTPUTS}/company_analysis/validation/`

```json
{
  "metadata": {
    "command_name": "company_analyst_validate_dasv_cross_analysis",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "dasv_phase_cross_analysis",
    "dasv_phase_analyzed": "discovery|analysis|synthesis|validation",
    "files_analyzed_count": 7,
    "analysis_methodology": "comprehensive_cross_phase_consistency_validation"
  },
  "files_analyzed": [
    {
      "filename": "COMPANY_NAME_YYYYMMDD_phase.json",
      "company_name": "COMPANY_IDENTIFIER",
      "modification_timestamp": "ISO_8601_format",
      "file_size_bytes": "numeric_file_size",
      "structural_compliance": "9.X/10.0"
    }
  ],
  "cross_analysis_results": {
    "structural_consistency_score": "9.X/10.0",
    "hardcoded_values_score": "9.X/10.0",
    "company_specificity_score": "9.X/10.0",
    "research_integration_score": "9.X/10.0",
    "overall_cross_analysis_score": "9.X/10.0"
  },
  "detected_issues": {
    "structural_inconsistencies": [
      {
        "issue_type": "missing_field|data_type_mismatch|format_violation",
        "files_affected": ["filename_array"],
        "description": "specific_issue_description",
        "severity": "high|medium|low",
        "recommendation": "specific_fix_recommendation"
      }
    ],
    "hardcoded_values": [
      {
        "value": "detected_hardcoded_string_or_number",
        "files_affected": ["filename_array"],
        "occurrences": "count_of_occurrences",
        "suspected_template_artifact": "true|false",
        "recommendation": "company_specific_replacement_suggestion"
      }
    ],
    "company_specificity_violations": [
      {
        "field_path": "json_path_to_field",
        "generic_content": "detected_generic_content",
        "files_affected": ["filename_array"],
        "recommendation": "company_specific_content_requirement"
      }
    ],
    "research_integration_inconsistencies": [
      {
        "service_name": "company_research_service_name",
        "inconsistency_type": "missing_service|inconsistent_usage|data_quality_variation",
        "files_affected": ["filename_array"],
        "recommendation": "standardization_approach"
      }
    ]
  },
  "quality_assessment": {
    "institutional_quality_certified": "true|false",
    "minimum_threshold_met": "true|false",
    "phase_consistency_grade": "A+|A|A-|B+|B|B-|C+|C|F",
    "ready_for_production": "true|false"
  },
  "recommendations": {
    "immediate_fixes": ["array_of_critical_issues_to_address"],
    "template_improvements": ["suggestions_for_template_enhancement"],
    "validation_enhancements": ["process_improvement_recommendations"],
    "cli_integration_optimizations": ["service_utilization_improvements"]
  }
}
```

## Enhanced Validation via Production Company Research Services

**Production Company Intelligence Services Integration:**

1. **Company Website Intelligence** - Core company data validation and official information verification
2. **Industry Report Services** - Real-time industry analysis validation and sector trend verification
3. **News Intelligence Services** - Company news validation and recent developments verification
4. **Business Database Services** - Company profile validation and business intelligence verification
5. **Market Research Services** - Industry indicators validation and market context verification
6. **Social Media Intelligence** - Company reputation validation for broader market sentiment
7. **Professional Network Intelligence** - Leadership and organizational intelligence validation for comprehensive context

**Company Research-Enhanced Validation Method:**
Use production company research services for comprehensive multi-source validation:

**Real-Time Company Data Validation:**
- Multi-service integration with company information validation across official sources, industry reports, and news services
- Automatic cross-validation with confidence scoring and institutional-grade company intelligence quality assessment
- Integrated business intelligence verification and market analyst sentiment validation

**Company Profile Verification:**
- Complete company profile validation via business database services and official company communications
- Enhanced business metrics validation including strategic initiatives, leadership changes, and market positioning
- Multi-source business model and competitive positioning data consistency checks

**Market Context Validation:**
- Industry research services for market context and sector trend validation
- Social media intelligence for company reputation and public sentiment verification
- Market research validation for industry dynamics, competitive landscape, and strategic positioning assessment

**Company Research Validation Benefits:**
- **Comprehensive Research Access**: Direct access to multiple company intelligence sources with standardized research interfaces
- **Multi-Source Company Validation**: Automatic cross-validation between multiple business intelligence sources with confidence scoring
- **Market Context Verification**: Real-time industry trends, competitive landscape, and company positioning validation
- **Institutional-Grade Quality**: Advanced company intelligence validation, data optimization, and quality scoring (targeting >97%)
- **Research Resilience**: Comprehensive error handling with graceful degradation and source reliability scoring

## Comprehensive DASV Validation Methodology

**Before beginning validation, establish context:**
- Extract company name and date from synthesis filename
- Locate ALL DASV outputs for validation:
  - Discovery: `./{DATA_OUTPUTS}/company_analysis/discovery/{COMPANY_NAME}_{YYYYMMDD}_discovery.json`
  - Analysis: `./{DATA_OUTPUTS}/company_analysis/analysis/{COMPANY_NAME}_{YYYYMMDD}_analysis.json`
  - Synthesis: `./{DATA_OUTPUTS}/company_analysis/{COMPANY_NAME}_{YYYYMMDD}.md`
- Document validation date and company intelligence freshness requirements
- Initialize systematic validation framework targeting >9.5/10 reliability

### Phase 1: Discovery Data Validation

**Discovery Output Systematic Verification**
```
COMPANY-RESEARCH-ENHANCED DISCOVERY VALIDATION PROTOCOL:
1. Company Profile Accuracy
   → Verify current company information via official company sources and business databases
   → Cross-validate with industry report services for company profile consistency
   → Integrate news intelligence services for recent company developments verification
   → Validate business model, market position, and company metrics across multiple research sources
   → Cross-reference company strategic positioning with multi-source intelligence
   → Use company research services for enhanced business intelligence validation:
     - Official company communications for current company data verification
     - Industry reports for market positioning consistency
     - Business databases for company profile and strategic metrics validation
   → Confidence threshold: 9.5/10 (allow comprehensive cross-validation for company intelligence)
   → **CRITICAL: Company information accuracy >95% is BLOCKING for institutional usage**
   → **MANDATORY: Current company profile must be consistent across all synthesis references**

2. Business Intelligence Integrity
   → Validate all business metrics against multiple company research sources
   → Verify strategic positioning using multi-source business intelligence data
   → Cross-check enhanced business metrics (market position, competitive advantages, strategic initiatives)
   → Validate competitive group selection and comparative business positioning
   → Confidence threshold: 9.8/10 (allow comprehensive business intelligence validation)

3. Company Research Quality Assessment Validation
   → Verify company research service health via source reliability checks
   → Validate multi-source company intelligence confidence score calculations
   → Confirm company research source reliability assessments and cross-validation
   → Verify company intelligence freshness meets research collection protocols
   → Confidence threshold: 9.0/10 minimum
```

### Phase 2: Analysis Evaluation Validation

**Analysis Output Comprehensive Assessment**
```
COMPANY-RESEARCH-ENHANCED ANALYSIS VALIDATION FRAMEWORK:
1. Business Model Analysis Verification
   → Validate all business model assessments against company research source data
   → Cross-check value proposition, operations, and market position metrics with multi-source company intelligence validation
   → Verify enhanced business metrics calculations (strategic positioning, competitive advantages, innovation capacity) against business intelligence data
   → Verify competitive comparison methodology and results using research-sourced industry data
   → Confidence threshold: 9.5/10 (institutional business intelligence accuracy standards)

2. Strategic Position Analysis
   → Validate strategic assessment against research-sourced industry data and competitive analysis
   → Cross-reference competitive positioning analysis with evidence from multi-source company intelligence
   → Verify strategic initiative probability assessments using market context from industry research
   → Validate sector implications against market indicators via industry intelligence validation
   → Confidence threshold: 9.0/10 (strategic assessments acceptable with company research evidence)

3. Business Risk Assessment Matrix Validation
   → Verify risk probability calculations using market context from industry research and company intelligence
   → Cross-check risk impact assessments with business evidence from company research sources
   → Validate aggregate risk scoring methodology against business context from company intelligence services
   → Verify market sensitivity analysis using industry research and competitive intelligence data
   → Confidence threshold: 9.0/10 minimum
```

### Phase 3: Synthesis Document Validation

**Synthesis Output Institutional Quality Assessment**

**Template Compliance Validation**:
- **CRITICAL: Verify document follows ./{TEMPLATES_BASE}/analysis/company_analysis_template.md specification exactly**
- Validate exact section structure: 🏢 Company Overview → 📊 Business Intelligence → 🎯 Strategic Position → 📈 Market Analysis → ⚠️ Risk Matrix → 📋 Analysis Metadata → 🏁 Company Intelligence Summary
- Confirm Company Intelligence Summary is 150-200 words synthesizing complete business analysis
- Verify all required table structures and formatting compliance
- Validate confidence scoring format (0.0-1.0 throughout document)
- Check risk probabilities use decimal format (0.0-1.0, not percentages)
```
COMPANY-RESEARCH-ENHANCED SYNTHESIS VALIDATION PROTOCOL:
1. Company Intelligence Coherence
   → Validate logical flow from company-research-enhanced discovery through analysis to conclusion
   → Verify business assessment alignment with company-research-validated analytical evidence
   → Cross-check confidence scores with company research source data quality and multi-source validation
   → Validate company intelligence coherence against real-time company data from research services
   → Confidence threshold: 9.5/10 (institutional business intelligence standard)

2. Strategic Analysis Model Verification
   → Validate all strategic positioning analysis against company-research-sourced business intelligence data
   → Cross-check scenario analysis probabilities using market context from industry research
   → Verify business model, competitive positioning, and strategic assessment methodologies with company intelligence data
   → Validate enhanced business metrics (market position, competitive advantages, strategic initiatives) in strategic models
   → Confidence threshold: 9.8/10 (strategic precision required)

3. Professional Presentation Standards
   → Verify document structure and formatting compliance with company-research-enhanced data standards
   → Validate confidence score integration throughout analysis reflecting company research validation quality
   → Check evidence attribution and company research source citation quality
   → Verify company research service health and data quality flags are properly documented
   → Confidence threshold: 9.0/10 minimum
```

## Real-Time Company Intelligence Validation Protocol

**Production Company Research Services Integration for Current Data Validation**:

**CRITICAL: Use CLI Services for All Financial Data Validation**
```
PRODUCTION CLI SERVICES CONFIGURATION:
- All services configured with production API keys from ./config/financial_services.yaml
- API keys securely stored and never included in validation outputs
- CLI services automatically access keys from secure configuration
- Production environment with institutional-grade service reliability

VALIDATION DATA COLLECTION - CLI COMMANDS:
1. Current Market Data Validation
   → CLI Command: python {SCRIPTS_BASE}/yahoo_finance_cli.py analyze {ticker} --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/alpha_vantage_cli.py quote {ticker} --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/fmp_cli.py profile {ticker} --env prod --output-format json
   → Verify: current_price, market_cap, trading_metrics, valuation ratios across multiple sources
   → Cross-reference: company_profile, analyst_data with multi-source validation
   → Confidence: Primary source validation (9.8/10.0 target) with 1.000 price consistency

2. Financial Statements Verification
   → CLI Command: python {SCRIPTS_BASE}/yahoo_finance_cli.py financials {ticker} --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/fmp_cli.py financials {ticker} --statement-type cash-flow-statement --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/fmp_cli.py insider {ticker} --env prod --output-format json
   → Validate: income_statement, balance_sheet, cash_flow data with enhanced metrics
   → Cross-check: enhanced financial metrics (EPS, ROE, revenue growth) calculations
   → Precision: Exact figures for institutional validation standards with multi-source consistency

3. Economic Context Validation
   → CLI Command: python {SCRIPTS_BASE}/fred_economic_cli.py rates --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/fred_economic_cli.py indicator UNRATE --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/fred_economic_cli.py indicator DGS10 --env prod --output-format json
   → CLI Command: python {SCRIPTS_BASE}/coingecko_cli.py sentiment --env prod --output-format json
   → Analyze: economic indicators, interest rate environment, cryptocurrency sentiment
   → Verify: economic regime assessment and sector implications
   → Context: Fed policy validation and broader market sentiment analysis

CLI INTEGRATION BENEFITS FOR VALIDATION:
- Direct access to 7 production-grade CLI services with standardized interfaces
- Multi-source price validation with institutional-grade confidence scoring
- Production caching and rate limiting improves API efficiency and reduces costs
- Comprehensive error handling with graceful degradation and source reliability scoring
- Real-time economic context integration with Fed policy and yield curve analysis
- Enhanced data reliability through built-in CLI validation and health monitoring
- **CLI Health Monitoring**: Real-time service health checks with operational status validation
- **Multi-Source Consistency**: Cross-validation across Yahoo Finance, Alpha Vantage, and FMP
- **Enhanced Financial Metrics**: Validation of calculated ratios (EPS, ROE, revenue growth)
- **Economic Context Validation**: Real-time Fed policy and cryptocurrency sentiment analysis
```

## Enhanced CLI Infrastructure Validation

**Multi-Source Data Validation via Comprehensive CLI Services Integration**:

```
ENHANCED CLI VALIDATION PROTOCOL:
1. Cross-Source Data Consistency Verification
   → SEC EDGAR CLI: python {SCRIPTS_BASE}/sec_edgar_cli.py search {ticker} --env prod --output-format json
   → Cross-validate financial statements between Yahoo Finance CLI and FMP CLI
   → Variance tolerance: ≤1% for regulatory data alignment
   → Validate filing dates and reporting periods for consistency across CLI sources

2. Economic Context Integration
   → FRED Economic CLI: python {SCRIPTS_BASE}/fred_economic_cli.py rates --env prod --output-format json
   → FRED Economic CLI: python {SCRIPTS_BASE}/fred_economic_cli.py indicator UNRATE --env prod --output-format json
   → Validate macroeconomic environment assessment using CLI economic data
   → Cross-reference inflation, interest rates, and sector performance via CLI services
   → Economic context confidence threshold: 9.0/10

3. Service Health Assessment
   → CLI Health Checks: python {service}_cli.py health --env prod for all 7 services
   → Validate CLI service operational status and API connectivity
   → Verify production environment configuration and API key validation
   → CLI service reliability confidence threshold: 9.5/10

4. Enhanced Analysis Integration
   → Use CLI services for comprehensive multi-source analysis:
     - Yahoo Finance CLI for financial metrics validation
     - FMP CLI for advanced financial statements and cash flow validation
     - Alpha Vantage CLI for real-time market data verification
     - SEC EDGAR CLI for regulatory context validation
     - FRED Economic CLI for economic environment verification
     - CoinGecko CLI for cryptocurrency sentiment validation
     - IMF CLI for global economic context validation
   → Investment thesis validation with multi-source CLI evidence
   → **Enhanced Financial Metrics Validation**: Verify calculated EPS, ROE, revenue growth
   → **Cash Flow Statement Validation**: Complete operating, investing, financing, and free cash flow
   → **Peer Group Analysis Validation**: Cross-validate industry comparisons and competitive positioning

CLI INTEGRATION QUALITY GATES:
- Multi-source data consistency: 9.5/10 minimum
- Economic context integration: 9.0/10 minimum
- CLI service health reliability: 9.5/10 minimum
- Infrastructure operational status: 9.0/10 minimum
```

**CLI-Enhanced Validation Standards**:
- **Primary Data** (0-2% variance): Grade A+ (9.8-10.0/10) - Perfect CLI multi-source validation
- **Minor Discrepancy** (2-5% variance): Grade A (9.0-9.7/10) - High CLI confidence
- **Moderate Error** (5-10% variance): Grade B (8.0-8.9/10) - REQUIRES CLI REVALIDATION
- **Major Inaccuracy** (>10% variance): Grade C-F (<8.0/10) - FAILS CLI MINIMUM THRESHOLD

**CRITICAL PRICE ACCURACY STANDARDS**:
- **Current Price Deviation >2%**: BLOCKING ISSUE - Analysis unsafe for decision-making
- **Outdated Price References**: BLOCKING ISSUE - Must be corrected before institutional usage
- **Price Inconsistency Across Document**: BLOCKING ISSUE - Requires immediate synthesis correction

## Output Structure

**File Naming**: `{TICKER}_{YYYYMMDD}_validation.json`
**Primary Location**: `./{DATA_OUTPUTS}/fundamental_analysis/validation/`

```json
{
  "metadata": {
    "command_name": "cli_enhanced_fundamental_analyst_validate",
    "execution_timestamp": "ISO_8601_format",
    "framework_phase": "cli_enhanced_validate_7_source",
    "ticker": "TICKER_SYMBOL",
    "validation_date": "YYYYMMDD",
    "validation_methodology": "comprehensive_dasv_workflow_validation_via_cli_services",
    "cli_services_utilized": "dynamic_array_of_successfully_utilized_services",
    "api_keys_configured": "production_keys_from_config/financial_services.yaml"
  },
  "overall_assessment": {
    "overall_reliability_score": "9.X/10.0",
    "decision_confidence": "High|Medium|Low|Do_Not_Use",
    "minimum_threshold_met": "true|false",
    "institutional_quality_certified": "true|false",
    "price_accuracy_validated": "true|false",
    "price_consistency_blocking_issue": "true|false",
    "cli_validation_quality": "9.X/10.0",
    "cli_services_health": "operational|degraded",
    "multi_source_consistency": "true|false"
  },
  "dasv_validation_breakdown": {
    "discovery_validation": {
      "market_data_accuracy": "9.X/10.0",
      "financial_statements_integrity": "9.X/10.0",
      "data_quality_assessment": "9.X/10.0",
      "cli_multi_source_validation": "9.X/10.0",
      "enhanced_financial_metrics_accuracy": "9.X/10.0",
      "cli_service_health_validation": "9.X/10.0",
      "overall_discovery_score": "9.X/10.0",
      "evidence_quality": "CLI_Primary|CLI_Secondary|Unverified",
      "key_issues": "array_of_cli_validation_findings"
    },
    "analysis_validation": {
      "financial_health_verification": "9.X/10.0",
      "competitive_position_assessment": "9.X/10.0",
      "risk_assessment_validation": "9.X/10.0",
      "cli_economic_context_validation": "9.X/10.0",
      "enhanced_metrics_calculation_accuracy": "9.X/10.0",
      "overall_analysis_score": "9.X/10.0",
      "evidence_quality": "CLI_Primary|CLI_Secondary|Unverified",
      "key_issues": "array_of_cli_analysis_findings"
    },
    "synthesis_validation": {
      "investment_thesis_coherence": "9.X/10.0",
      "valuation_model_verification": "9.X/10.0",
      "professional_presentation": "9.X/10.0",
      "cli_data_integration_quality": "9.X/10.0",
      "multi_source_evidence_strength": "9.X/10.0",
      "overall_synthesis_score": "9.X/10.0",
      "evidence_quality": "CLI_Primary|CLI_Secondary|Unverified",
      "key_issues": "array_of_cli_synthesis_findings"
    }
  },
  "cli_service_validation": {
    "service_health": {
      "yahoo_finance": "healthy|degraded|unavailable",
      "alpha_vantage": "healthy|degraded|unavailable",
      "fmp": "healthy|degraded|unavailable",
      "sec_edgar": "healthy|degraded|unavailable",
      "fred_economic": "healthy|degraded|unavailable",
      "coingecko": "healthy|degraded|unavailable",
      "imf": "healthy|degraded|unavailable"
    },
    "health_score": "0.0-1.0_operational_assessment",
    "services_operational": "count_of_working_cli_services",
    "services_healthy": "boolean_overall_status",
    "multi_source_consistency": "price_validation_consistency_score",
    "data_quality_scores": {
      "yahoo_finance_cli": "0.0-1.0_reliability_score",
      "alpha_vantage_cli": "0.0-1.0_reliability_score",
      "fmp_cli": "0.0-1.0_reliability_score",
      "fred_economic_cli": "0.0-1.0_reliability_score",
      "coingecko_cli": "0.0-1.0_reliability_score",
      "sec_edgar_cli": "0.0-1.0_reliability_score",
      "imf_cli": "0.0-1.0_reliability_score"
    }
  },
  "critical_findings_matrix": {
    "verified_claims_high_confidence": "array_with_evidence_citations",
    "questionable_claims_medium_confidence": "array_with_concern_explanations",
    "inaccurate_claims_low_confidence": "array_with_correcting_evidence",
    "unverifiable_claims": "array_with_limitation_notes"
  },
  "decision_impact_assessment": {
    "thesis_breaking_issues": "none|array_of_critical_flaws",
    "material_concerns": "array_of_significant_issues",
    "refinement_needed": "array_of_minor_corrections"
  },
  "usage_recommendations": {
    "safe_for_decision_making": "true|false",
    "price_accuracy_blocking_issue": "true|false",
    "required_corrections": "prioritized_array",
    "follow_up_research": "specific_recommendations",
    "monitoring_requirements": "key_data_points_to_track"
  },
  "methodology_notes": {
    "cli_services_consulted": "7_production_grade_cli_financial_services",
    "multi_source_validation": "yahoo_finance_alpha_vantage_fmp_cli_cross_validation",
    "economic_context_validation": "fred_economic_cli_and_coingecko_cli_verification",
    "enhanced_metrics_validation": "eps_roe_revenue_growth_calculation_verification",
    "cli_health_monitoring": "real_time_service_health_and_operational_status",
    "research_limitations": "what_could_not_be_verified_via_cli_services",
    "confidence_intervals": "where_cli_multi_source_uncertainty_exists",
    "validation_standards_applied": "institutional_quality_thresholds_via_cli_integration"
  },
  "enhanced_validation_features": {
    "price_consistency_validation": "cross_validated_across_3_sources_targeting_1.000_confidence",
    "price_accuracy_blocking_validation": "current_price_deviation_greater_than_2_percent_blocks_institutional_usage",
    "synthesis_price_reference_validation": "all_document_price_references_verified_against_cli_current_price",
    "financial_metrics_calculation_verification": "eps_roe_revenue_growth_cash_flow_validation",
    "economic_context_integration": "real_time_fed_policy_and_crypto_sentiment_analysis",
    "peer_group_analysis_validation": "industry_specific_competitor_comparison_verification",
    "regulatory_intelligence_validation": "sec_edgar_framework_and_insider_trading_verification"
  }
}
```

## Validation Execution Protocol

### Pre-Execution
1. Extract ticker and date from synthesis filename parameter
2. Locate and verify existence of all DASV output files
3. Initialize production CLI services connection for real-time data validation
4. Verify CLI service health across all 7 financial data services
5. Set institutional quality confidence thresholds (≥9.0/10)

### Main Execution
1. **CLI-Enhanced Discovery Validation**
   - Execute `python {SCRIPTS_BASE}/yahoo_finance_cli.py analyze {ticker} --env prod --output-format json` for market data verification
   - Execute `python {SCRIPTS_BASE}/alpha_vantage_cli.py quote {ticker} --env prod --output-format json` for price cross-validation
   - Execute `python {SCRIPTS_BASE}/fmp_cli.py profile {ticker} --env prod --output-format json` for company intelligence validation
   - Execute `python {SCRIPTS_BASE}/fmp_cli.py financials {ticker} --statement-type cash-flow-statement --env prod --output-format json` for cash flow verification
   - Validate enhanced financial metrics (EPS, ROE, revenue growth) calculations against FMP CLI data
   - Assess CLI data quality methodology and multi-source confidence scoring
   - Track successful CLI service responses in cli_services_utilized (only include services that provided validation data)

2. **CLI-Enhanced Analysis Validation**
   - Cross-check all financial health calculations against CLI-sourced data
   - Verify competitive position assessments with CLI-validated evidence
   - Execute `python {SCRIPTS_BASE}/fred_economic_cli.py rates --env prod --output-format json` for economic context validation
   - Execute `python {SCRIPTS_BASE}/coingecko_cli.py sentiment --env prod --output-format json` for crypto sentiment verification
   - Verify economic context integration and sector implications

3. **CLI-Enhanced Synthesis Validation**
   - Assess investment thesis logical coherence using CLI-validated evidence support
   - Verify valuation model calculations against CLI-sourced financial statement data
   - Evaluate professional presentation with CLI confidence integration
   - Validate multi-source data consistency throughout synthesis

4. **Comprehensive CLI Assessment**
   - Execute `python {service}_cli.py health --env prod` checks across all 7 financial services
   - Calculate overall reliability score across all DASV phases with CLI validation
   - Generate critical findings matrix with CLI evidence citations
   - Provide usage recommendations and CLI-validated corrections

### Post-Execution
1. **MANDATORY: Save validation output to ./{DATA_OUTPUTS}/fundamental_analysis/validation/**
   - **CRITICAL**: Every validation execution MUST generate and save a comprehensive report
   - For single ticker validation: `{TICKER}_{YYYYMMDD}_validation.json`
   - For cross-analysis validation: `{PHASE}_cross_analysis_{YYYYMMDD}_validation.json`
   - Verify file write success and report file size > 0 bytes
   - Include error handling for disk write failures with retry mechanisms
2. **Generate validation summary with institutional quality certification**
   - Document overall assessment scores and grade assignments
   - Include decision confidence levels and usage recommendations
   - Flag blocking issues and required corrections
3. **Flag any outputs failing minimum 9.0/10 threshold**
   - Mark non-compliant files for immediate attention
   - Generate prioritized remediation recommendations
4. **Document methodology limitations and research gaps**
   - Record CLI service availability and health status
   - Note data quality constraints and validation limitations
5. **VERIFICATION: Confirm report file integrity**
   - Validate JSON structure and completeness
   - Verify all required sections are populated
   - Check file permissions and accessibility
   - Log successful report generation with timestamp

## Security and Implementation Notes

### API Key Security
- API keys are stored securely in `./config/financial_services.yaml`
- API keys MUST NEVER be included in validation outputs or logs
- CLI services automatically access keys from secure configuration
- Output includes reference to config file: `"api_keys_configured": "production_keys_from_config/financial_services.yaml"`

### Dynamic Service Tracking
- `cli_services_utilized` field should only contain services that successfully provided validation data
- Do NOT include all 7 services statically - track actual successful responses
- Example: If CoinGecko fails, exclude "coingecko_cli" from the array
- Include services only after successful data retrieval and validation

## Quality Standards

### Institutional Quality Thresholds
- **Target Reliability**: >9.5/10 across all DASV phases
- **Minimum Threshold**: 9.0/10 for institutional usage certification
- **Mathematical Precision**: 9.8/10 for quantitative calculations
- **Evidence Standards**: Primary source verification required for all material claims

### Validation Requirements
- Complete DASV workflow assessment with cross-phase coherence verification
- Real-time market data validation via CLI financial services
- Institutional quality confidence scoring throughout assessment
- Evidence-based recommendations with specific correction priorities
- **MANDATORY REPORT GENERATION**: Every validation execution must produce and save a comprehensive validation report

### Cross-Analysis Report Management Standards
- **File Naming Convention**: `{PHASE}_cross_analysis_{YYYYMMDD}_validation.json`
- **Storage Location**: `./{DATA_OUTPUTS}/fundamental_analysis/validation/`
- **Minimum Content Requirements**:
  - Complete metadata with execution timestamp and methodology
  - Full file analysis breakdown with structural compliance scores
  - Detected issues matrix with severity classifications
  - Quality assessment with institutional certification status
  - Actionable recommendations for immediate fixes and improvements
- **Report Retention**: Maintain validation reports for audit trail and framework improvement analysis
- **File Integrity**: Verify JSON structure, completeness, and accessibility post-generation

## CLI Implementation Guidelines

### Validation Data Collection via CLI Services

**Use CLI Services for All Data Verification**:
```
# Primary validation workflow using CLI services
1. Market Data Cross-Validation:
   → python {SCRIPTS_BASE}/yahoo_finance_cli.py analyze {ticker} --env prod --output-format json
   → python {SCRIPTS_BASE}/alpha_vantage_cli.py quote {ticker} --env prod --output-format json
   → python {SCRIPTS_BASE}/fmp_cli.py profile {ticker} --env prod --output-format json

2. Data Quality Assessment:
   → Compare discovery outputs against fresh CLI data
   → Validate calculation precision using CLI standardized formats
   → Cross-reference data_quality indicators from CLI responses

3. Error Handling and Reliability:
   → Utilize CLI error responses for data quality flags
   → Leverage CLI cache_status for data freshness validation
   → Apply CLI completeness scores to validation confidence

CRITICAL: Always use production CLI services with proper configuration
```

### CLI-Enhanced Validation Methodology

**Institutional Quality Standards with CLI Integration**:
- **Data Consistency**: Use CLI standardized formats for precise cross-validation
- **Source Reliability**: Leverage CLI data_quality indicators and timestamps
- **Performance Optimization**: Utilize CLI caching for consistent validation data
- **Error Prevention**: Apply CLI error handling to prevent validation failures
- **Report Generation Integrity**: Implement file write verification and error handling for all validation reports

### Mandatory Report Saving Protocol

**CRITICAL IMPLEMENTATION REQUIREMENTS**:
```bash
# File saving verification protocol
1. Generate validation report in memory
2. Validate JSON structure and completeness
3. Write to disk with error handling:
   - Primary save attempt
   - Verify file write success (size > 0 bytes)
   - Retry mechanism for failed writes (up to 3 attempts)
   - Log success/failure with timestamps
4. Post-write verification:
   - Confirm file accessibility and permissions
   - Validate JSON parsing of saved file
   - Check all required sections are populated
   - Record successful completion in execution log
```

**Error Handling for Report Saving**:
- Disk space validation before write attempts
- Permission verification for target directory
- Backup location fallback for critical validation reports
- User notification for persistent save failures
- Automatic retry with exponential backoff for temporary failures

## Usage Examples

### Single Ticker Validation Examples

**Basic Single Ticker Validation:**
```bash
/fundamental_analysis:validate VTRS_20250725.md
```
- Validates complete DASV workflow for VTRS on July 25, 2025
- Uses default institutional validation depth
- Performs real-time CLI data validation
- Output: `VTRS_20250725_validation.json`

**Advanced Single Ticker Validation:**
```bash
/fundamental_analysis:validate AAPL_20250725.md --confidence_threshold=9.5 --validation_depth=comprehensive
```
- Higher confidence threshold requiring 9.5/10 minimum
- Comprehensive validation rigor
- Output: `AAPL_20250725_validation.json`

### DASV Phase Cross-Analysis Examples

**Analysis Phase Cross-Analysis (Current Request):**
```bash
/fundamental_analysis:validate analysis
```
- Analyzes latest 7 analysis files for consistency
- Detects hardcoded values and template artifacts
- Validates ticker specificity across files
- Output: `analysis_cross_analysis_20250725_validation.json`

**Discovery Phase Cross-Analysis:**
```bash
/fundamental_analysis:validate discovery --file_count=5
```
- Analyzes latest 5 discovery files
- Focuses on data collection consistency
- Output: `discovery_cross_analysis_20250725_validation.json`

**Synthesis Phase Cross-Analysis:**
```bash
/fundamental_analysis:validate synthesis --confidence_threshold=9.8
```
- Institutional-grade synthesis validation
- Higher confidence threshold for final documents
- Output: `synthesis_cross_analysis_20250725_validation.json`

**Validation Phase Cross-Analysis:**
```bash
/fundamental_analysis:validate validation
```
- Meta-validation of validation reports
- Ensures validation consistency and quality
- Output: `validation_cross_analysis_20250725_validation.json`

### Error Examples

**Invalid Parameter Format:**
```bash
/fundamental_analysis:validate VTRS_2025  # Missing .md extension
# Error: Invalid filename format. Must match {TICKER}_{YYYYMMDD}.md
```

**Invalid Phase Specification:**
```bash
/fundamental_analysis:validate testing   # Invalid phase name
# Error: Invalid phase. Must be discovery, analysis, synthesis, or validation
```

**Missing Parameters:**
```bash
/fundamental_analysis:validate           # No arguments
# Error: Missing required parameter. Specify filename or phase
```

**Integration with DASV Framework**: This microservice provides comprehensive quality assurance for the complete fundamental analysis workflow, ensuring institutional-quality reliability standards across all phases before publication or decision-making usage. All data verification is performed through the production CLI financial services to maintain consistency with the discovery and analysis phases.

## Validation Report Archive and Management

### Report Lifecycle Management
- **Creation**: Every validation execution automatically generates comprehensive reports
- **Storage**: All reports saved to `./{DATA_OUTPUTS}/fundamental_analysis/validation/` with standardized naming
- **Verification**: Post-generation integrity checks ensure report completeness and accessibility
- **Retention**: Maintain historical validation reports for framework improvement analysis
- **Cleanup**: Implement automated archival for reports older than 90 days (configurable)

### Audit Trail Requirements
- **Execution Logging**: Record all validation attempts with timestamps and outcomes
- **Report Catalog**: Maintain index of generated reports for easy retrieval
- **Quality Tracking**: Monitor validation scores and improvement trends over time
- **Compliance Documentation**: Ensure all reports meet institutional quality standards

### Integration Verification
- **Cross-Analysis Coverage**: Verify all DASV phases have corresponding cross-analysis validation reports
- **Consistency Monitoring**: Track framework evolution and standardization progress
- **Quality Assurance**: Ensure validation reports support institutional compliance requirements
- **Framework Improvement**: Use validation findings to enhance analysis methodologies

**Author**: Cole Morton
**Confidence**: [Validation confidence will be calculated based on assessment completeness and evidence quality]
**Data Quality**: [Data quality score based on source verification and validation thoroughness via CLI services]
**Report Generation**: [MANDATORY - All validation executions must produce comprehensive saved reports]

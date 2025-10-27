# Company Analysis (Simple)

**Single-Phase Company Intelligence Analysis**

Streamlined company analysis combining discovery, analysis, and synthesis into one execution phase for rapid business intelligence generation with direct markdown output.

## Purpose

Generate comprehensive company intelligence analysis in a single pass, producing institutional-quality business intelligence documents without intermediate JSON artifacts. This command consolidates the multi-phase DASV workflow into a unified execution for faster insights.

## Parameters

### Required
- `company_name`: Company name or organization (required, will be normalized)

### Optional
- `depth`: Analysis depth - `summary` | `standard` | `comprehensive` (default: `standard`)
  - `summary`: High-level overview with key metrics only (~5 min execution)
  - `standard`: Balanced analysis with core business intelligence (~10 min execution)
  - `comprehensive`: Deep-dive analysis with extensive market context (~20 min execution)

## Execution Flow

### Phase 1: Research & Data Collection
1. **Company Profile Research**
   - Web search for company overview, business model, products/services
   - Company website analysis for official information
   - Recent news and press releases (last 12 months)
   - Leadership team and organizational structure

2. **Business Intelligence Gathering**
   - Industry classification and market positioning
   - Competitive landscape and major competitors
   - Revenue model and customer segments
   - Technology stack and operational infrastructure

3. **Market Context Analysis**
   - Industry trends and market dynamics
   - Regulatory environment and compliance status
   - Strategic partnerships and alliances
   - Recent developments and strategic initiatives

### Phase 2: Analysis & Assessment

1. **Business Model Analysis (A-F Grading)**
   - **Value Proposition**: Market fit, customer value, differentiation
   - **Revenue Model**: Revenue streams, pricing strategy, scalability
   - **Operations**: Operational efficiency, technology infrastructure, resource utilization
   - **Market Position**: Market share, brand strength, innovation capacity

2. **Competitive Analysis (0-10 Scoring)**
   - Market advantages and competitive differentiation
   - Barriers to entry and strategic moats
   - Industry position and ecosystem influence
   - Leadership quality and organizational effectiveness

3. **Strategic Assessment**
   - Strategic positioning and market opportunity
   - Growth initiatives and business development priorities
   - Strategic partnerships and alliance strategy
   - Market timing and strategic flexibility

4. **Risk Assessment (Probability × Impact)**
   - Operational risks and execution challenges
   - Competitive threats and market disruption
   - Regulatory compliance and policy risks
   - Technology risks and adaptation capability

### Phase 3: Synthesis & Document Generation

Generate publication-ready markdown document with:
- Executive summary with strategic assessment scoring
- Company intelligence dashboard with key metrics
- Business model scorecard with A-F grades and trend indicators
- Competitive analysis with market positioning evaluation
- Strategic assessment with growth drivers and initiatives
- Risk assessment matrix with mitigation strategies
- Market analysis with industry trends and competitive landscape
- Company intelligence summary (150-200 words)

## Output Structure

**File Naming**: `{COMPANY_NAME}_{YYYYMMDD}_analysis.md`
**Location**: `./data/outputs/company_analysis/`
**Format**: Publication-ready markdown with structured sections

### Document Sections

#### 1. Executive Summary
- Company overview and business description
- Strategic assessment summary with scoring
- Key highlights (growth metrics, challenges, strategic position)
- High-level investment/engagement recommendation

#### 2. Company Intelligence Dashboard
- Company foundation (legal entity, registration, headquarters)
- Leadership & governance assessment
- Product & service portfolio
- Market positioning metrics

#### 3. Business Model Scorecard
- **Value Proposition**: Grade (A+ to F) with trend indicator (—/’/˜)
- **Revenue Model**: Grade with revenue stream analysis
- **Operations**: Grade with operational efficiency assessment
- **Market Position**: Grade with competitive positioning
- Overall business model grade with justification

#### 4. Competitive Analysis
- **Competitive Positioning Score**: X.X/10.0
- Market advantages and differentiation factors
- Industry position and ecosystem influence
- Leadership quality assessment
- Competitive sustainability evaluation

#### 5. Strategic Assessment
- Strategic positioning framework
- Growth initiatives and catalysts
- Market opportunity analysis
- Strategic scenario analysis (growth/baseline/challenge)

#### 6. Risk Assessment Matrix
- **Operational Risk**: Probability × Impact with mitigation
- **Competitive Risk**: Market threats and response capability
- **Regulatory Risk**: Compliance requirements and policy impact
- **Technology Risk**: Disruption threats and adaptation capability
- Overall risk score with business resilience assessment

#### 7. Market Analysis
- Industry environment and trends
- Market cycle position and implications
- Competitive landscape evaluation
- Geographic and market expansion analysis

#### 8. Company Intelligence Summary
- 150-200 word synthesis of complete analysis
- Strategic positioning assessment
- Business intelligence applications and recommendations

## Quality Standards

### Analysis Rigor
- **Business Model Grading**: Evidence-based A-F assessment with clear justification
- **Competitive Scoring**: 0-10 scale with specific criteria and supporting evidence
- **Risk Quantification**: Probability (0.0-1.0) × Impact framework with mitigation strategies
- **Market Context**: Industry-specific trends and competitive dynamics integration

### Professional Presentation
- **Structured Format**: Clear section hierarchy with emoji indicators (<â, =Ê, <¯, =È,  )
- **Data Tables**: Professional markdown tables for metrics and scorecards
- **Confidence Indicators**: Explicit confidence levels for key assessments
- **Evidence Attribution**: Clear sourcing for material claims and data points

### Content Quality Targets (by Depth Level)

**Summary** (depth=summary):
- Execution time: ~5 minutes
- Confidence target: e7.5/10.0
- Data completeness: e70% core fields
- Focus: High-level overview with key metrics only

**Standard** (depth=standard, default):
- Execution time: ~10 minutes
- Confidence target: e8.5/10.0
- Data completeness: e85% core fields
- Focus: Balanced analysis with comprehensive business intelligence

**Comprehensive** (depth=comprehensive):
- Execution time: ~20 minutes
- Confidence target: e9.0/10.0
- Data completeness: e95% core fields
- Focus: Deep-dive analysis with extensive market context and validation

## Implementation Notes

### Research Methodology
- **Web Search**: Company overview, recent news, competitive landscape, industry trends
- **Company Website**: Official information, products/services, leadership team, strategic initiatives
- **Business Databases**: Company profiles, industry classification, market positioning (if available)
- **News Sources**: Recent developments, strategic announcements, market perception
- **Best Effort Approach**: Use available sources, flag gaps, avoid speculation

### Analysis Approach
- **Direct Markdown Generation**: No intermediate JSON files
- **Single-Pass Execution**: Combine research, analysis, synthesis in one workflow
- **Practical Quality Standards**: Institutional-grade content without multi-phase validation overhead
- **Transparent Limitations**: Document data gaps and confidence constraints

### Efficiency Optimizations
- **Parallel Research**: Concurrent web searches for company, industry, competitors
- **Template-Free Generation**: Direct markdown composition without template orchestration
- **Minimal Overhead**: No sub-agent delegation, schema validation, or multi-source reconciliation
- **Fast Iteration**: Single command execution for complete analysis

## Usage Examples

### Basic Usage (Standard Depth)
```bash
/company_analysis_simple "Tesla Inc"
```
Output: `Tesla_Inc_20251024_analysis.md` with standard depth analysis

### Summary Analysis (Quick Overview)
```bash
/company_analysis_simple "Stripe" --depth=summary
```
Output: `Stripe_20251024_analysis.md` with high-level summary (~5 min)

### Comprehensive Deep-Dive
```bash
/company_analysis_simple "Commonwealth Bank of Australia" --depth=comprehensive
```
Output: `Commonwealth_Bank_of_Australia_20251024_analysis.md` with extensive analysis (~20 min)

## Comparison to Multi-Phase Workflow

### Multi-Phase (DASV) Workflow
- **Commands**: 3 sequential commands (discover ’ analyze ’ synthesize)
- **Outputs**: 2 JSON files + 1 markdown file
- **Execution Time**: ~30-45 minutes (comprehensive)
- **Complexity**: Sub-agent orchestration, schema validation, multi-source reconciliation
- **Quality**: Institutional-grade (e9.5/10) with extensive validation

### Single-Phase (Simple) Workflow
- **Commands**: 1 unified command
- **Outputs**: 1 markdown file (no JSON artifacts)
- **Execution Time**: ~5-20 minutes (based on depth)
- **Complexity**: Direct research and analysis, best-effort validation
- **Quality**: Professional-grade (e8.5/10 standard) with practical rigor

### Use Case Guidance
- **Use Multi-Phase** when: Institutional-grade validation required, archival JSON needed, maximum confidence critical
- **Use Single-Phase** when: Rapid insights needed, markdown-only output sufficient, 85%+ confidence acceptable

## Expected Outcomes

### Deliverables
-  Publication-ready markdown document with comprehensive company intelligence
-  A-F business model scorecard with evidence-backed grades
-  0-10 competitive positioning score with sustainability assessment
-  Risk assessment matrix with probability × impact framework
-  Strategic positioning analysis with scenario evaluation
-  Company intelligence summary synthesizing complete analysis

### Quality Metrics
- **Standard Depth**: e8.5/10 confidence, e85% data completeness, ~10 min execution
- **Comprehensive Depth**: e9.0/10 confidence, e95% data completeness, ~20 min execution
- **Professional Presentation**: Structured markdown, clear formatting, evidence-based claims
- **Business Intelligence Value**: Actionable insights for strategic decision-making

---

**Author**: Cole Morton
**Framework**: Streamlined Single-Phase Company Analysis
**Optimization**: 70% complexity reduction from multi-phase DASV workflow
**Status**: Production-ready for rapid company intelligence generation

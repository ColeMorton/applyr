# Company Intelligence Analyze

**DASV Phase 2: Company-Specific Intelligence Analysis Requirements**

Generate comprehensive company analysis focusing on business model assessment, competitive positioning evaluation, and strategic intelligence with institutional-grade quality standards.

## Purpose

Define the analytical requirements for transforming company discovery data into comprehensive business intelligence. This specification focuses on company analysis domain requirements while delegating CLI-enhanced analytical methodology to the analyst sub-agent.

## Microservice Integration

**Framework**: DASV Phase 2
**Role**: company_analyst
**Action**: analyze
**Input Source**: cli_enhanced_company_analyst_discover
**Output Location**: `./{DATA_OUTPUTS}/company_analysis/analysis/`
**Next Phase**: company_analyst_synthesize
**Template Integration**: `./{TEMPLATES_BASE}/analysis/company_analysis_template.md`
**Implementation Delegation**: Analyst sub-agent handles CLI-enhanced analysis methodology

## Analysis Parameters

### Core Requirements
- `discovery_file`: Path to company discovery JSON file (required) - format: {COMPANY_NAME}_{YYYYMMDD}_discovery.json
- `confidence_threshold`: Minimum confidence for analytical conclusions - `0.8` | `0.9` | `0.95` (optional, default: 0.9)

### Company Analysis Features
- `business_model_assessment`: Enable A-F graded business model evaluation - `true` | `false` (optional, default: true)
- `competitive_intelligence`: Enable competitive positioning analysis - `true` | `false` (optional, default: true)
- `strategic_analysis`: Enable strategic positioning framework - `true` | `false` (optional, default: true)
- `leadership_assessment`: Enable leadership team evaluation - `true` | `false` (optional, default: true)
- `market_positioning`: Enable market analysis and industry trends - `true` | `false` (optional, default: true)

## Company-Specific Intelligence Requirements

### 1. Business Model Assessment Framework (A-F Grading)

**Value Proposition Analysis**:
- **Core Value Analysis**: Unique value propositions and customer benefit assessment
- **Market Problem Solution Fit**: Problem-solution alignment and market need validation
- **Differentiation Strategy**: Competitive differentiation factors and sustainable advantages
- **Value Creation Consistency**: Value delivery predictability and customer satisfaction metrics

**Revenue Model Evaluation**:
- **Revenue Stream Analysis**: Primary revenue sources, diversification, and sustainability assessment
- **Customer Segmentation**: Target customer analysis and segment profitability evaluation
- **Pricing Strategy Assessment**: Pricing power, model sustainability, and competitive positioning
- **Growth Scalability**: Revenue model scalability and expansion potential evaluation

**Business Operations Framework**:
- **Operational Excellence**: Process efficiency, quality management, and operational scalability
- **Technology Infrastructure**: Platform capabilities, digital transformation, and innovation adoption
- **Supply Chain Assessment**: Supply chain resilience, partner relationships, and operational dependencies
- **Resource Utilization**: Human capital, technology assets, and operational resource optimization

**Market Position Metrics**:
- **Market Share Analysis**: Current position, growth trends, and competitive dynamics
- **Customer Acquisition**: Customer growth rates, acquisition costs, and retention metrics
- **Brand Strength**: Brand recognition, customer loyalty, and market perception assessment
- **Innovation Capacity**: R&D investment, product development pipeline, and innovation track record

### 2. Competitive Intelligence Requirements

**Competitive Positioning Assessment (1-10 Scoring)**:
- **Market Advantage Identification**: Brand recognition, customer loyalty, operational efficiency, and strategic assets
- **Competitive Differentiation**: Unique selling propositions, product/service differentiation, and market positioning
- **Barriers to Entry**: Industry entry barriers, regulatory requirements, and competitive protection factors
- **Competitive Response**: Competitive response capability, strategic flexibility, and market defense strength

**Industry Ecosystem Analysis**:
- **Market Dynamics**: Industry growth trends, market maturity, and competitive intensity assessment
- **Value Chain Position**: Supplier relationships, customer concentration, and strategic partnerships evaluation
- **Industry Influence**: Market leadership, industry standard-setting, and ecosystem influence assessment
- **Strategic Alliances**: Partnership strategies, joint ventures, and collaborative competitive advantages

**Leadership Quality Evaluation**:
- **Executive Assessment**: Leadership team background, track record, and strategic vision evaluation
- **Strategic Decision Making**: Historical strategic decisions, market timing, and execution capability
- **Organizational Excellence**: Company culture, talent management, and organizational effectiveness
- **Adaptability**: Strategic flexibility, market adaptation, and change management capability

**Innovation and Growth Analysis**:
- **Innovation Strategy**: R&D investment, product development pipeline, and innovation culture assessment
- **Technology Adoption**: Digital transformation, technology integration, and modernization initiatives
- **Market Expansion**: Geographic expansion, new market entry, and growth strategy execution
- **Future Readiness**: Emerging technology adoption, market trend anticipation, and strategic positioning

### 3. Strategic Analysis Requirements

**Strategic Positioning Framework**:
- **Market Strategy**: Market positioning, target customer strategy, and competitive strategy analysis
- **Growth Strategy**: Expansion plans, market penetration, and strategic growth initiatives evaluation
- **Strategic Partnerships**: Alliance strategy, joint ventures, and partnership ecosystem assessment
- **Strategic Assets**: Intellectual property, brand assets, and strategic resource evaluation
- **Strategic Flexibility**: Strategic options, pivot capability, and strategic risk management
- **Market Timing**: Strategic timing, market entry/exit strategies, and strategic opportunity assessment

**Business Model Analysis**:
- **Value Creation**: Value proposition strength, customer value delivery, and value capture mechanisms
- **Scalability Assessment**: Business model scalability, growth potential, and expansion capability
- **Sustainability Factors**: Business model sustainability, competitive durability, and long-term viability
- **Innovation Integration**: Technology integration, innovation adoption, and business model evolution

**Market Opportunity Assessment**:
- **Market Size Analysis**: Total addressable market, serviceable market, and market growth potential
- **Market Trends**: Industry trends, consumer behavior shifts, and market evolution analysis
- **Competitive Landscape**: Competitive intensity, market fragmentation, and competitive dynamics
- **Market Entry Strategy**: Market penetration approach, customer acquisition strategy, and market timing

**Strategic Scenario Analysis**:
- **Growth Scenario**: Optimistic growth assumptions, strategic success, and favorable market conditions
- **Baseline Scenario**: Most likely strategic outcome with realistic market assumptions
- **Challenge Scenario**: Conservative assumptions, strategic obstacles, and adverse market conditions
- **Strategic Probability Assessment**: Scenario likelihood evaluation and strategic outcome weighting

### 4. Market Context Integration Requirements

**Industry Environment Impact**:
- **Industry Growth Trends**: Sector growth patterns, market maturity, and industry lifecycle assessment
- **Regulatory Environment**: Industry regulations, compliance requirements, and regulatory risk evaluation
- **Technology Disruption**: Industry disruption trends, technology adoption, and digital transformation impact
- **Market Consolidation**: Industry consolidation trends, M&A activity, and market structure evolution

**Economic Environment Assessment**:
- **Economic Sensitivity**: Business model sensitivity to economic cycles and macroeconomic factors
- **Market Resilience**: Company performance during economic downturns and recovery patterns
- **Growth Positioning**: Economic expansion opportunities and market share growth potential
- **Economic Indicators**: Relevant economic indicators impact on business performance and market position

**Market Dynamics Analysis**:
- **Market Growth**: Market expansion trends, customer demand patterns, and growth trajectory assessment
- **Market Volatility**: Market stability, demand volatility, and business model resilience evaluation
- **Consumer Behavior**: Customer behavior trends, preference shifts, and market demand evolution
- **Market Accessibility**: Market entry barriers, customer acquisition challenges, and market reach assessment

### 5. Business Risk Assessment and Quantification

**Company-Specific Risk Matrix (Probability × Impact)**:
- **Operational Risk**: Business execution risk, key personnel dependency, and operational disruption probability
- **Strategic Risk**: Strategic execution risk, market positioning risks, and strategic decision impact assessment
- **Competitive Risk**: Market share erosion, competitive disruption, and competitive response capability evaluation
- **Regulatory Risk**: Regulatory changes, compliance requirements, and policy impact on business operations
- **Technology Risk**: Technology disruption threat, digital transformation risks, and adaptation capability assessment

**Business Sustainability Risk Integration**:
- **Environmental Impact**: Environmental sustainability, regulatory compliance, and climate change adaptation
- **Social Responsibility**: Community relations, employee satisfaction, and social impact considerations
- **Governance Quality**: Leadership effectiveness, organizational governance, and stakeholder management assessment
- **Reputation Risk**: Brand reputation, public perception, and stakeholder confidence impact evaluation

**Business Resilience Testing**:
- **Market Stress**: Market downturn scenarios and business model resilience during adverse conditions
- **Competitive Pressure**: Competitive intensity scenarios and market share defense capability assessment
- **Operational Disruption**: Supply chain disruption, operational continuity, and business recovery analysis
- **Strategic Adaptation**: Strategic flexibility, pivot capability, and long-term competitive positioning recovery

## Output Structure Requirements

**File Naming**: `{COMPANY_NAME}_{YYYYMMDD}_analysis.json`
**Primary Location**: `./{DATA_OUTPUTS}/company_analysis/analysis/`

### Required Output Sections

1. **Business Model Assessment Scorecard**
   - A-F grades for value proposition, revenue model, operations, and market position
   - Supporting qualitative and quantitative metrics with peer comparison context
   - Strategic trend analysis and forward-looking business assessment
   - Grade justification with evidence and confidence scoring

2. **Competitive Intelligence Assessment**
   - Competitive positioning scoring (1-10) with strategic sustainability analysis
   - Industry position evaluation and market dynamics assessment
   - Leadership quality evaluation and strategic positioning analysis
   - Innovation capabilities and market adaptation evaluation

3. **Strategic Analysis Framework**
   - Strategic positioning analysis with detailed assumptions and scenario planning
   - Market opportunity assessment with competitive comparison and strategic rationale
   - Business model sustainability integration and strategic momentum assessment
   - Scenario-weighted strategic positioning with probability assignments

4. **Market Context Integration**
   - Industry trends impact and market environment sensitivity assessment
   - Economic cycle positioning and market resilience evaluation
   - Market dynamics correlation and business volatility sensitivity
   - Industry factor attribution and business model market implications

5. **Quantified Business Risk Assessment**
   - Risk matrix with evidence-backed probability × impact scoring for business risks
   - Business sustainability risk integration and operational considerations
   - Stress testing scenarios with strategic recovery timeline analysis
   - Risk mitigation strategies and strategic monitoring frameworks

## Quality Standards and Evidence Requirements

### Company Research Integration Standards
- **Multi-Source Validation**: Company websites, industry reports, news sources, and public filings data consistency
- **Research Health Monitoring**: Real-time source availability and data quality assessment
- **Data Quality Attribution**: Source confidence scoring and cross-validation requirements
- **Information Protocols**: Source degradation handling and data reliability maintenance

### Company Analysis Standards
- **Information Quality**: Company data accuracy, source verification, and information quality assessment
- **Peer Group Selection**: Appropriate comparable companies and industry classification for competitive analysis
- **Historical Context**: Multi-year company analysis and industry cycle consideration
- **Strategic Intelligence Integration**: Company guidance, strategic announcements, and management communications

### Institutional-Grade Requirements
- **Analysis Confidence**: ≥9.0/10.0 baseline with comprehensive company research integration
- **Evidence Requirement**: All grades and scores supported by company-specific analysis
- **Cross-Validation**: Multiple information sources and consistency verification
- **Professional Standards**: Business intelligence-level analytical rigor and methodology

### Strategic Analysis Methodology Standards
- **Strategic Rigor**: Detailed strategic positioning modeling with explicit assumptions
- **Competitive Validation**: Peer group appropriateness and competitive positioning reasonableness
- **Scenario Analysis**: Comprehensive strategic sensitivity and scenario modeling
- **Strategic Assessment Confidence**: Strategic positioning confidence intervals and assumption testing

## Implementation Notes

**Analyst Sub-Agent Integration**: This specification defines WHAT company analysis is required. The analyst sub-agent handles HOW through:
- Company research-enhanced analytical framework execution
- Universal quality standards and confidence scoring enforcement
- Discovery data preservation with multi-source validation
- Template synthesis preparation and structure optimization

**Key Company Analysis Focus Areas**:
- **Business Model Assessment**: Comprehensive A-F grading with evidence-backed assessment
- **Competitive Positioning**: Detailed sustainability analysis and strategic competitive positioning
- **Strategic Analysis**: Multi-method approach with scenario weighting and strategic sensitivity analysis
- **Risk Integration**: Comprehensive business risk quantification with sustainability and resilience testing
- **Market Context**: Industry factor integration and business cycle positioning

**Company Research Dependencies**: Optimized for multi-source company intelligence integration with real-time source health monitoring and quality attribution through analyst sub-agent orchestration.

---

**Framework Integration**: Optimized for DASV analyst sub-agent execution focusing on company analysis domain expertise and institutional-grade business intelligence standards.

**Author**: Cole Morton
**Optimization**: 45% complexity reduction through company research methodology delegation to analyst sub-agent
**Confidence**: Company analysis domain specification with institutional-grade business intelligence quality

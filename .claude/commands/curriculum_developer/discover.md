# Curriculum Intelligence Discover

**DASV Phase 1: Topic-Based Learning Content Discovery and Resource Aggregation**

Comprehensive educational content discovery engine that systematically searches project data repositories and supplements with current web research to create the foundation for ultimate learning materials on any subject.

## Purpose

The Curriculum Development Discovery phase defines requirements for systematic collection and initial structuring of all learning resources required for comprehensive topic-based curriculum development. This specification focuses on **what** educational content is needed rather than **how** to obtain it, delegating technical implementation to the researcher sub-agent.

**Expected Output Schema**: `/{SCRIPTS_BASE}/schemas/curriculum_discovery_schema.json`
**Researcher Sub Task**: Use the researcher sub-agent to execute educational content discovery. Ensure output conforms to `/{SCRIPTS_BASE}/schemas/curriculum_discovery_schema.json`.

## Microservice Integration

**Framework**: DASV Phase 1
**Role**: curriculum_developer
**Action**: discover
**Output Location**: `./{DATA_OUTPUTS}/curriculum_development/discovery/`
**Next Phase**: curriculum_developer_analyze
**Template Reference**: `./{TEMPLATES_BASE}/education/curriculum_template.md` (final output structure awareness)

## Parameters

### Core Parameters
- `topic`: Subject or keyword for curriculum development (required, normalized format)
- `depth`: Research depth - `foundational` | `comprehensive` | `expert` | `mastery` (optional, default: comprehensive)
- `learning_level`: Target audience - `beginner` | `intermediate` | `advanced` | `all_levels` (optional, default: all_levels)
- `timeframe`: Content recency - `current` | `2y` | `5y` | `historical` (optional, default: current)
- `confidence_threshold`: Minimum confidence for content quality - `0.7` | `0.8` | `0.9` (optional, default: 0.8)
- `web_supplement`: Enable web research enhancement - `true` | `false` (optional, default: true)

## Data Discovery Requirements

### Primary Discovery Source: Project Data Repository

**Local Data Intelligence Requirements**:
- **Systematic File System Scanning**: Complete search through `./data/outputs/` and `./data/raw/` directories
- **Content Pattern Matching**: Intelligent topic relevance detection across all file formats
- **Metadata Extraction**: File dates, sizes, formats, creation timestamps, and modification history
- **Cross-Reference Analysis**: Identify relationships between different data sources
- **Content Categorization**: Classify resources by educational value and topic relevance

**Project Data Categories**:

#### Career Development Intelligence
- **Job Market Data**: Job descriptions (`./data/outputs/job_descriptions/`), market summaries, technology trend analysis
- **Application Strategy**: Cover letters (`./data/outputs/cover_letters/`), application tracking (`./data/raw/advertisements.csv`)
- **Professional Positioning**: Resume data, work experience, professional descriptions (`./data/raw/`)
- **Company Intelligence**: Business analysis reports (`./data/outputs/company_analysis/`)
- **Market Intelligence**: Salary benchmarking, hiring patterns, industry insights

#### Technical Implementation Resources
- **Web Scraping Methodology**: SEEK scraper implementation, anti-bot measures, data extraction techniques
- **Data Processing Pipelines**: Aggregation scripts, CSV manipulation, markdown conversion workflows
- **PDF Generation Systems**: Multiple styling templates, brand integration, WeasyPrint implementation
- **CLI Interface Design**: Command-line architecture, user experience optimization
- **Application Tracking**: Status workflows, database management, success ratio analysis

#### Strategic Analysis Frameworks
- **Company Research**: Business model evaluation, competitive positioning, strategic assessment
- **Market Analysis**: Technology demand patterns, competitive landscape evaluation
- **Risk Assessment**: Business resilience testing, scenario planning methodologies
- **Performance Metrics**: Success tracking, optimization strategies, outcome measurement

### Secondary Discovery Source: Web Research Enhancement

**Current Information Supplementation**:
- **Industry Best Practices**: Latest methodologies and proven approaches
- **Technology Updates**: Current tools, frameworks, and implementation strategies
- **Academic Resources**: Educational theory, learning science, pedagogical frameworks
- **Expert Content**: Thought leadership articles, case studies, professional insights
- **Tutorial Libraries**: Step-by-step guides, video content, interactive resources
- **Community Resources**: Forums, discussion boards, peer learning platforms

**Web Research Categories**:
- **Educational Methodology**: Teaching strategies, learning theory, instructional design
- **Topic Expertise**: Subject matter expert content, authoritative sources
- **Current Trends**: Latest developments, emerging practices, industry evolution
- **Tool Reviews**: Software recommendations, platform comparisons, implementation guides
- **Case Studies**: Real-world examples, success stories, implementation reports

### Quality Standards

- **Multi-Source Validation**: Cross-validation between project data and external sources with confidence scoring
- **Educational Value Assessment**: Content quality ≥ 0.85 for comprehensive curriculum development
- **Content Completeness**: ≥ 90% topic coverage across all educational levels
- **Source Reliability**: ≥ 80% credibility score across web research sources
- **Recency Validation**: Current information verification for time-sensitive topics

## Content Organization Structure

**File Naming**: `{TOPIC}_{YYYYMMDD}_discovery.json`
**Primary Location**: `./{DATA_OUTPUTS}/curriculum_development/discovery/`
**Schema Definition**: `/{SCRIPTS_BASE}/schemas/curriculum_discovery_schema.json`

### Required Discovery Components

#### 1. Project Data Intelligence
- **Local Resource Inventory**: Complete catalog of relevant project files with metadata
- **Content Relationship Mapping**: Cross-references between different data sources
- **Educational Value Scoring**: Assessment of teaching potential for each resource
- **Topic Relevance Grading**: Alignment score between content and curriculum topic
- **Learning Example Identification**: Real-world cases suitable for educational purposes

#### 2. Web Research Intelligence
- **Authoritative Source Collection**: High-quality external resources and references
- **Current Best Practices**: Latest industry standards and proven methodologies
- **Educational Framework References**: Pedagogical approaches and learning theory
- **Tool and Resource Recommendations**: Software, platforms, and implementation guides
- **Expert Content Curation**: Thought leadership and professional insights

#### 3. Learning Content Architecture
- **Skill Level Mapping**: Content categorization by difficulty and prerequisites
- **Learning Path Identification**: Optimal sequence for knowledge building
- **Practical Application Opportunities**: Hands-on exercises and real-world implementation
- **Assessment Framework Elements**: Knowledge check possibilities and evaluation methods
- **Resource Integration Strategy**: How to combine project data with external sources

#### 4. Content Gap Analysis
- **Missing Information Identification**: Areas requiring additional research
- **Learning Objective Coverage**: Completeness assessment for educational goals
- **Difficulty Level Distribution**: Balance verification across skill levels
- **Practical Exercise Opportunities**: Implementation and practice scenario availability
- **Current Information Requirements**: Need for up-to-date supplemental content

### Schema Compliance Standards
- Multi-source educational content validation targeting high confidence scores
- Complete discovery insights with curriculum development priorities identified
- Comprehensive learning resource quality standards compliance
- Source attribution and link preservation for all web-based resources

## Expected Outcomes

### Discovery Quality Targets
- **Overall Content Quality**: ≥ 95% confidence through multi-source validation
- **Educational Completeness**: ≥ 90% across all required learning levels and objectives
- **Project Data Integration**: ≥ 85% utilization of relevant local resources
- **Web Research Quality**: ≥ 80% credibility score across external sources

### Key Deliverables
- Comprehensive topic-based resource inventory with educational value assessment
- Multi-source validated learning content and reference materials
- Learning path foundation with skill progression identification
- Content relationship analysis with cross-reference mapping
- Discovery insights identifying curriculum development priorities and resource gaps
- Complete source attribution with clickable links and reference preservation
- Quality assessment with confidence scoring and source reliability metrics

## Web Research Integration Protocol

### Search Strategy Framework
**Primary Research Targets**:
- Educational content repositories (Khan Academy, Coursera, edX)
- Industry publication databases (Harvard Business Review, MIT Sloan)
- Professional development platforms (LinkedIn Learning, Pluralsight)
- Technical documentation sites (MDN, Stack Overflow, GitHub)
- Government and institutional resources (Bureau of Labor Statistics, university publications)

**Search Query Optimization**:
- Keyword expansion using topic synonyms and related terms
- Academic database searches for peer-reviewed content
- Industry-specific search within professional publications
- Video and multimedia content discovery for diverse learning styles
- Current event searches for up-to-date information and trends

### Source Validation and Attribution
**Credibility Assessment Framework**:
- Author expertise verification and background research
- Publication date and information currency validation
- Source institution reputation and authority evaluation
- Peer review and citation analysis where applicable
- Cross-reference validation with multiple independent sources

**Link Preservation and Export**:
- Complete URL collection with metadata (title, author, date, description)
- Archive link creation for content preservation
- Citation format standardization for academic integrity
- Content summary generation for quick reference
- Access validation to ensure link availability

## Integration with DASV Framework

**Foundation for Analysis Phase**: This discovery provides the comprehensive resource base required for the subsequent analyze phase, ensuring high-quality input for systematic curriculum development and learning path design.

**Educational Content Specialization**: Unlike traditional research discovery, this focuses specifically on educational value, learning potential, and pedagogical application of discovered resources.

**Project Data Leverage**: Maximizes the extensive applyr project repository as a real-world case study foundation while supplementing with current industry knowledge and best practices.

**Author**: Cole Morton
**Optimization**: Topic-focused educational content discovery with project data integration
**Confidence**: Comprehensive curriculum foundation with multi-source validation quality

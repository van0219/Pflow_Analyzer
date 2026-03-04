---
inclusion: auto
name: rice-methodology
description: RICE methodology (Reports, Interfaces, Conversions, Enhancements), ANA-050 functional specifications, DES-020 technical specifications, requirements analysis, deliverables. Use when working with RICE items or specification documents.
---

# RICE Methodology and Specifications

## Table of Contents

- [Overview](#overview)
- [RICE Categories](#rice-categories)
  - [Reports (R)](#reports-r)
  - [Interfaces (I)](#interfaces-i)
  - [Conversions (C)](#conversions-c)
  - [Enhancements (E)](#enhancements-e)
- [Specification Documents](#specification-documents)
  - [ANA-050 Functional Specification](#ana-050-functional-specification)
  - [DES-020 Technical Specification](#des-020-technical-specification)
  - [Document Relationships](#document-relationships)
- [AI Analysis Workflow](#ai-analysis-workflow)
  - [Step 1: Identify RICE Type](#step-1-identify-rice-type)
  - [Step 2: Determine IPA vs LPL](#step-2-determine-ipa-vs-lpl)
  - [Step 3: Determine Deliverables](#step-3-determine-deliverables)
  - [Step 4: Separate Requirements](#step-4-separate-requirements)
- [IPA vs LPL Decision Matrix](#ipa-vs-lpl-decision-matrix)
- [Solution Deliverables](#solution-deliverables)
- [Document Formatting Standards](#document-formatting-standards)
- [Related Steering Files](#related-steering-files)

## Overview

**RICE** is a standard ERP project methodology for categorizing deliverables in Infor FSM implementations:

- **R**eports - System outputs (data summaries, analytics)
- **I**nterfaces - Data exchange with external systems
- **C**onversions - Data migration from legacy systems
- **E**nhancements - Customizations extending standard functionality

**Key Principle**: One RICE item = one complete solution that may include:

- One or more IPAs (main process + subprocesses)
- LPL configuration code (UI/form changes)
- File channels (for file-triggered processes)
- Menu definitions, form modifications, security configurations
- Combined ANA-050 + DES-020 specification document

**Automated Analysis**: Use `ReusableTools/IPA_Analyzer/` to automatically identify RICE type from ANA-050 documents.

## RICE Categories

### Reports (R)

**Purpose**: System outputs containing data summaries, detailed views, or analytics

**Common Implementations**:

- Infor BI reports
- FSM Lists
- Spreadsheet Designer
- Custom report generation (IPA-driven)

**Typical Deliverables**:

- Report specification document
- Report definition files
- Testing guide
- User documentation
- ANA-050 + DES-020 specification

**IPA/LPL**: Usually neither (unless report generation is automated via IPA)

### Interfaces (I)

**Purpose**: Connections between FSM and external systems for data exchange

**Common Implementations**:

- **IPA** (most common) - Process automation for data integration
- ION - Infor's integration platform
- Web Services - REST/SOAP APIs
- File-based integrations - SFTP, File Channels

**Typical Deliverables**:

- IPA process files (.lpd)
- File Channel configurations (if file-triggered)
- Field mapping specifications
- Interface testing guide
- Deployment procedures
- Combined ANA-050 + DES-020 specification

**IPA/LPL**: IPA required, LPL optional

**Key Insight**: IPA is most commonly used for Interfaces where data or processes move between FSM and external systems.

### Conversions (C)

**Purpose**: Data migration from legacy systems into FSM

**Common Implementations**:

- IPA for data transformation
- Data Migrator tools
- ETL (Extract, Transform, Load) processes
- Custom migration scripts

**Typical Deliverables**:

- Data mapping specifications
- Conversion scripts/IPAs
- Data validation reports
- Rollback procedures
- Testing and validation guide
- ANA-050 + DES-020 specification

**IPA/LPL**: IPA common, LPL optional

### Enhancements (E)

**Purpose**: Customizations or extensions to standard FSM functionality

**Common Implementations**:

- **IPA and/or LPL** - Custom workflows and UI changes
- Business class extensions
- Custom fields and validations
- Specialized processing logic

**Typical Deliverables**:

- IPA process files (if workflow automation)
- LPL configuration code (if UI changes)
- Menu definitions, form modifications
- Security configurations
- Testing guide
- Combined ANA-050 + DES-020 specification

**IPA/LPL**: Both common, depends on requirements

## Specification Documents

### ANA-050 Functional Specification

**Purpose**: Blueprint for implementation defining business requirements

**Standard Sections**:

1. Introduction - High-level overview
2. Scope - Inclusions and exclusions
3. Business Requirements - Detailed requirements with acceptance criteria
4. Process Flow - Workflow diagrams and step-by-step descriptions
5. Data Requirements - Data sources, fields, validation rules
6. User Roles & Permissions - Access control definitions
7. Integration Points - ION, SFTP, API interfaces
8. Error Handling - Error scenarios and management strategies
9. Reporting & Notifications - Reports, alerts, email requirements
10. Approval Workflow - Approval steps and routing (if applicable)
11. Appendix - Supporting information

**Key Content**:

- Business objectives and scenarios
- Functional requirements with acceptance criteria
- Process flow diagrams
- Field mapping tables
- Business rules and validation logic
- User interface requirements
- Integration specifications
- Test scenarios

### DES-020 Technical Specification

**Purpose**: Technical blueprint providing developers with implementation instructions

**Standard Sections**:

1. Introduction - Technical solution overview
2. Technical Architecture - System components and interaction diagrams
3. Data Mapping & Transformation - Field mappings and transformation logic
4. Interface Specifications - API definitions, file formats, integration points
5. Configuration Details - System settings, environment variables, parameters
6. Security & Access Controls - User roles, permissions, data protection
7. Error Handling & Logging - Error management and logging strategies
8. Development Steps - Detailed build and deployment instructions
9. Testing & Validation - Technical test cases and validation procedures
10. Appendix - Supporting diagrams, tables, references

**Key Content**:

- Technical architecture diagrams
- Detailed field mappings with data types
- IPA process activity specifications
- LPL configuration code
- File channel configurations
- Security configurations
- Deployment procedures
- Technical test cases

### Document Relationships

**ANA-050 → DES-020 Flow**:

- ANA-050 defines the "what" (business requirements)
- DES-020 defines the "how" (technical implementation)
- Combined template merges both for comprehensive documentation

**Usage in Project Lifecycle**:

- **Project Initiation**: ANA-050 establishes requirements
- **Design & Development**: DES-020 guides technical implementation
- **Testing & UAT**: Both serve as validation references
- **Documentation**: Record for maintenance and enhancements

## AI Analysis Workflow

**CRITICAL**: When analyzing ANA-050 documents, follow this 4-step process in order.

### Step 1: Identify RICE Type

**Every ANA-050 document represents a RICE item.** Identify the category FIRST before technical analysis.

**Identification Methods**:

1. **Check document title and RICE ID**:
   - "FPI-ANA-050-MATCH-REPORT" → Interface
   - "CLIENT-ANA-050-INVOICE-APPROVAL" → Enhancement

2. **Look for keywords**:
   - "extract", "import", "export", "integration" → **Interface**
   - "report", "analytics", "dashboard" → **Report**
   - "migration", "conversion", "legacy data" → **Conversion**
   - "workflow", "approval", "UI change", "new field" → **Enhancement**

3. **Analyze business objectives**:
   - Data exchange with external systems → **Interface**
   - Information delivery to users → **Report**
   - One-time data load → **Conversion**
   - Process improvement or customization → **Enhancement**

### Step 2: Determine IPA vs LPL

**Decision Matrix**:

| Requirement Type | IPA | LPL | Workunit |
|------------------|-----|-----|----------|
| Data integration with external system | ✅ | ❌ | ✅ |
| Scheduled data extract/export | ✅ | ❌ | ✅ |
| File-triggered processing | ✅ | ❌ | ✅ |
| Approval workflow | ✅ | Maybe | ✅ |
| UI form modification only | ❌ | ✅ | ❌ |
| New field on business class | ❌ | ✅ | ❌ |
| Menu/navigation change only | ❌ | ✅ | ❌ |
| LPL action triggering process | ✅ | ✅ | ✅ |

**Key Insight**: IPA is most commonly used for **Interfaces** where data or processes move between FSM and external systems.

### Step 3: Determine Deliverables

**Based on RICE type and IPA/LPL determination, identify required deliverables.**

**Interface (I) - File-Triggered**:

```text
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 02_IPA_Technical_Specification.md
├── 03_[ProjectName].lpd
├── 04_File_Channel_Configuration.md  ← REQUIRED
├── 05_Testing_Guide.md
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

**Interface (I) - Scheduled Outbound**:

```text
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 02_IPA_Technical_Specification.md
├── 03_[ProjectName].lpd
├── 05_Testing_Guide.md  ← NO File Channel (scheduled via Process Server Admin)
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

**Enhancement (E) - LPL Only**:

```text
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 07_LPL_Configuration_Codes.md
├── 08_Menu_Definitions.lpl (if needed)
├── 09_Form_Modifications.lpl (if needed)
├── 10_Field_Configurations.lpl (if needed)
├── 05_Testing_Guide.md
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

**Enhancement (E) - IPA + LPL**:

```text
├── 00_Solution_Summary.md
├── 01_Requirements_Analysis.md
├── 02_IPA_Technical_Specification.md
├── 03_[ProjectName].lpd
├── 07_LPL_Configuration_Codes.md
├── [LPL files as needed]
├── 05_Testing_Guide.md
├── 06_Deployment_Guide.md
└── ANA-050_DES-020_Combined_Specification.docx
```

### Step 4: Separate Requirements

**Distinguish between IPA and LPL requirements when analyzing ANA-050 documents.**

**IPA Flow Requirements** (Process Automation):

- Approval routing logic and approver determination
- Email notifications and content
- Workflow actions (Approve, Return, Reject)
- Business class queries and data retrieval
- Process flow logic and branching
- Integration with external systems
- Error handling and exception management
- Scheduled data extraction
- File processing and transformation

**Configuration Console Requirements** (LPL/UI Changes):

- Field protection and read-only settings
- Form field display and visibility
- Default value population
- Required field validation
- UI layout and formatting
- Service/Process Definition enablement
- Form behavior and user experience
- Menu and navigation changes
- List configurations
- Security class updates

**Analysis Approach**:

1. **Identify UI/Form Changes**: Requirements mentioning "hide fields", "protect fields", "display", "default values" are Configuration Console tasks
2. **Focus IPA Scope**: Extract only approval logic, notifications, and process flow requirements
3. **Separate Concerns**: UI modifications require LPL changes via Configuration Console, not IPA flows
4. **Document Both**: Clearly separate IPA requirements from Configuration Console requirements in analysis

**Example: Invoice Approval Enhancement**

**IPA Requirements**:

- Determine approver based on invoice amount and department
- Send email notification to approver
- Wait for approval action
- Escalate if no response within 2 business days
- Update invoice status upon approval/rejection
- Log all approval actions

**LPL Requirements**:

- Protect invoice amount field after submission
- Hide approval history section from non-approvers
- Add "Submit for Approval" button to invoice form
- Display approval status indicator
- Set default values for department and cost center
- Enable Service Definition for approval process

## IPA vs LPL Decision Matrix

### When IPA is Required

- **Data Integration**: Exchanging data with external systems
- **Scheduled Processing**: Automated data extraction or transformation
- **File Processing**: Triggered by file arrival or scheduled
- **Approval Workflows**: Multi-step approval processes with notifications
- **Business Logic**: Complex processing that spans multiple business classes
- **Error Handling**: Sophisticated error management and recovery

### When LPL is Required

- **UI Modifications**: Form layout, field visibility, protection
- **Field Defaults**: Populating default values
- **Validation Rules**: Client-side or server-side validation
- **Menu Changes**: Adding or modifying navigation
- **List Configurations**: Custom list views and filters
- **Security**: Role-based access control
- **Form Behavior**: Custom actions and event handling

### When Both are Required

- **Approval Workflows with UI**: Process automation + form modifications
- **Triggered Processes**: LPL button/action triggers IPA process
- **Complex Enhancements**: Both process logic and UI changes needed
- **Integrated Solutions**: End-to-end functionality requiring both layers

## Solution Deliverables

### Automated RICE Analysis

**IPA Analyzer** (`ReusableTools/IPA_Analyzer/`) automatically analyzes ANA-050 documents:

**Features**:

1. **RICE Type Identification** - Analyzes document content and filename
2. **IPA vs LPL Determination** - Identifies process automation vs UI requirements
3. **Requirements Extraction** - Extracts numbered requirements and bullet points (top 50)
4. **Requirements Traceability** - Maps requirements to implemented activities
5. **Gap Analysis** - Identifies missing features and scope gaps

**Usage**:

```python
from ReusableTools.IPA_Analyzer.ipa_analyzer import analyze_ipa_project

result = analyze_ipa_project(
    project_name='ProjectName',
    lpd_files=['path/to/file.lpd'],
    wu_log_file='path/to/log.txt',
    functional_spec='path/to/ANA-050.docx'  # Enables RICE analysis
)

# Access RICE analysis results
rice_type = result.functional_spec_analysis['rice_type']
ipa_vs_lpl = result.functional_spec_analysis['ipa_vs_lpl']
traceability = result.functional_spec_analysis['traceability']
gaps = result.functional_spec_analysis['gaps']
```

## Document Formatting Standards

### Combined ANA-050 + DES-020 Template

**Purpose**: Single document approach for complete project specification

**Structure**:

- **Title Page**: Infor logo, project name, RICE ID
- **Document Control**: Version history, reviewers, approvers
- **Table of Contents**: Auto-generated with hyperlinks
- **Functional Specifications** (Sections 2-3): Business requirements, process flows, interface specs
- **Technical Design** (Section 4): Solution architecture, configurations, implementation
- **Testing Process** (Section 5): Test steps and validation
- **Appendix** (Section 6): Artifacts and supporting documentation

**Key Formatting**:

- **Page Size**: A4 (8.27" x 11.69")
- **Font**: Arial (NOT Calibri)
- **Headings**: H1 (14pt, ALL CAPS), H2 (14pt, Title Case), H3 (12pt, ALL CAPS), H4 (12pt, Title Case)
- **Tables**: Black header background, white text, 8pt font
- **Colors**: Infor Blue (#13A3F7) for highlights

**CRITICAL**: NO "Part I" or "Part II" headers - use continuous numbered sections

## Related Steering Files

- `00_Core_System_Rules.md` - Reusable Tools (IPA Analyzer)
- `01_IPA_and_IPD_Complete_Guide.md` - IPA/IPD concepts and implementation
- `06_FSM_Business_Classes_and_API.md` - RICE tracking and business classes
- `10_IPA_Report_Generation.md` - IPA peer review and client handover documentation

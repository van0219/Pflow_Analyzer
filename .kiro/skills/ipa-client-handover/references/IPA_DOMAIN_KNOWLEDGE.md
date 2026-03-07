# IPA Domain Knowledge for Client Handover Documentation

This reference provides essential IPA/IPD knowledge for generating client-facing documentation. Focus on business-friendly explanations suitable for client handover reports.

## Table of Contents

- [Activity Type Descriptions](#activity-type-descriptions)
- [Common Process Patterns](#common-process-patterns)
- [Integration Patterns](#integration-patterns)
- [Data Access Patterns](#data-access-patterns)
- [ANA-050 Specification Structure](#ana-050-specification-structure)
- [Business Requirements Extraction](#business-requirements-extraction)

## Activity Type Descriptions

When documenting IPA processes for clients, use these business-friendly descriptions:

### Control Activities

| Activity Type | Client-Friendly Name | Business Purpose |
|---------------|---------------------|------------------|
| START | Process Entry Point | Initializes the workflow and sets up required variables |
| END | Process Completion | Marks successful completion of the workflow |
| ASSGN | Data Processing | Performs calculations, data transformations, and business logic |
| BRANCH | Decision Point | Routes the workflow based on business rules and conditions |
| SUBPROC | Sub-Workflow | Calls reusable workflow components for modular processing |
| Timer | Wait Period | Introduces time delays for scheduled operations or escalation |

### Data Activities

| Activity Type | Client-Friendly Name | Business Purpose |
|---------------|---------------------|------------------|
| ACCFIL | File Operations | Reads, writes, or manages files in the system storage |
| FileTransfer | External File Transfer | Transfers files to/from external SFTP servers |
| JSONPARSER | Data Parser | Extracts information from structured data formats |
| For Each | Data Iterator | Processes multiple records or items in sequence |

### Communication Activities

| Activity Type | Client-Friendly Name | Business Purpose |
|---------------|---------------------|------------------|
| EMAIL | Email Notification | Sends email notifications to users or stakeholders |
| SMS | Text Message | Sends SMS notifications for urgent alerts |
| ION Outbox | System Integration | Sends data to other Infor applications via ION |

### Integration Activities

| Activity Type | Client-Friendly Name | Business Purpose |
|---------------|---------------------|------------------|
| LM | Database Operations | Queries or updates FSM business data |
| WEBRN | API Integration | Connects to external systems via web services |
| Web Service | SOAP Integration | Integrates with legacy web services |

### Approval Activities

| Activity Type | Client-Friendly Name | Business Purpose |
|---------------|---------------------|------------------|
| UA | Approval Action | Waits for user approval or rejection with escalation support |

## Common Process Patterns

### Multi-Level Approval Pattern

**Business Description**: Implements hierarchical approval workflows where transactions route through multiple approval levels based on business rules.

**Key Features**:
- Dynamic approver assignment based on transaction attributes
- Automatic escalation if approvers don't respond within timeframe
- Reason code collection for audit compliance
- Email notifications at each approval level
- Milestone tracking for audit trail

**When Used**: Invoice approvals, payment approvals, contract approvals, journal entry approvals

**Client Benefit**: Ensures proper authorization controls while maintaining audit compliance and timely processing

### File Interface Pattern

**Business Description**: Automates data exchange with external systems through file-based integration.

**Key Features**:
- Automatic file monitoring and processing
- Data validation and transformation
- Error handling with notification
- Archive management for processed files
- Reconciliation and reporting

**When Used**: Bank reconciliation, GL interfaces, vendor data imports, customer data exports

**Client Benefit**: Reduces manual data entry, improves accuracy, and provides automated reconciliation

### OAuth2 Authentication Pattern

**Business Description**: Securely authenticates with external systems using industry-standard OAuth2 protocol.

**Key Features**:
- Environment-specific credential management
- Automatic token acquisition and refresh
- Secure credential storage
- Error handling for authentication failures

**When Used**: API integrations with external systems (Coupa, Workday, banking systems)

**Client Benefit**: Ensures secure, compliant integration with external systems

## Integration Patterns

### Compass API Integration (Data Lake Queries)

**Business Description**: Extracts large volumes of data from the Infor Data Lake for reporting and analysis.

**Key Features**:
- Asynchronous query execution for large datasets
- Automatic pagination for millions of records
- Multiple output formats (CSV, JSON)
- Query status monitoring

**When Used**: GL balance extracts, invoice reports, transaction history exports

**Client Benefit**: Enables efficient extraction of large datasets without impacting system performance

### Landmark Business Class Integration

**Business Description**: Directly interacts with FSM business data for real-time operations.

**Key Features**:
- Real-time data access
- Transactional integrity
- Native FSM operations
- Field-level security

**When Used**: Approval workflows, single-record operations, status updates

**Client Benefit**: Provides real-time data access with full transactional integrity

### File Channel Integration

**Business Description**: Automatically processes files transferred from external SFTP servers.

**Key Features**:
- Automatic file detection and processing
- Configurable monitoring schedules
- Error handling and notification
- Archive management

**When Used**: Inbound file interfaces from external systems

**Client Benefit**: Eliminates manual file processing and ensures timely data integration

## Data Access Patterns

### When to Use Compass API vs Landmark Nodes

| Scenario | Recommended Approach | Reason |
|----------|---------------------|--------|
| Large data extracts (>10K records) | Compass API | Optimized for bulk data retrieval with pagination |
| Real-time approval workflows | Landmark Nodes | Direct database access with transactional integrity |
| Reporting and analytics | Compass API | Data Lake optimized for analytical queries |
| Single record operations | Landmark Nodes | Faster for individual record access |
| External system integration | Compass API | Better for batch processing and file generation |

### File Operations Architecture

**FSM File Storage**:
- Cloud-based storage managed by FSM
- Accessible by File Access activities
- Used for temporary processing and internal file management

**External SFTP Servers**:
- Customer-managed file servers
- Accessible by File Transfer activities
- Used for integration with external systems

**File Channel**:
- Automatic bridge between SFTP and FSM File Storage
- Monitors SFTP directories and triggers IPA processes
- Manages file lifecycle (process → archive → cleanup)

## ANA-050 Specification Structure

### Standard Sections

1. **Introduction** - High-level overview and business context
2. **Scope** - What's included and excluded from the solution
3. **Business Requirements** - Detailed functional requirements with acceptance criteria
4. **Process Flow** - Step-by-step workflow descriptions with diagrams
5. **Data Requirements** - Data sources, field mappings, validation rules
6. **User Roles & Permissions** - Access control and security requirements
7. **Integration Points** - External system connections (ION, SFTP, APIs)
8. **Error Handling** - Error scenarios and management strategies
9. **Reporting & Notifications** - Reports, alerts, and email requirements
10. **Approval Workflow** - Approval steps and routing logic (if applicable)
11. **Appendix** - Supporting information and references

### Key Content for Client Handover

**Business Objectives**:
- Why the solution was implemented
- Business problems it solves
- Expected benefits and outcomes

**Functional Requirements**:
- Numbered requirements with acceptance criteria
- Source attribution (section references)
- Priority levels (Critical, High, Medium, Low)
- Stakeholder assignments

**Process Flow**:
- Workflow diagrams showing process steps
- Decision points and routing logic
- Integration touchpoints
- Error handling paths

**Field Mappings**:
- Source to target field mappings
- Data transformation rules
- Validation requirements
- Default values

## Business Requirements Extraction

### Requirement Categories

**Data Integration Requirements**:
- File formats and structures
- Data sources and destinations
- Transformation rules
- Validation requirements
- Error handling

**Approval Workflow Requirements**:
- Approval hierarchy and routing
- Approver determination logic
- Escalation rules and timeframes
- Reason code requirements
- Notification requirements

**User Interface Requirements**:
- Form modifications (LPL)
- Field visibility and protection
- Default values
- Required field validation
- Button actions

**Integration Requirements**:
- External system connections
- Authentication methods
- Data exchange frequency
- Error notification
- Reconciliation requirements

### Requirement Attributes

Each requirement should include:

- **ID**: Sequential identifier (BR-001, BR-002, etc.)
- **Title**: Brief requirement description
- **Description**: Detailed requirement explanation
- **Category**: Functional area (Data Integration, Approval, UI, etc.)
- **Priority**: Critical, High, Medium, Low
- **Source**: ANA-050 section reference
- **Stakeholder**: Business owner or responsible party
- **Acceptance Criteria**: How to verify requirement is met

### Extracting Requirements from ANA-050

**Look for these indicators**:

- Numbered requirement lists
- "The system shall..." statements
- "The process must..." statements
- Bullet points under "Requirements" sections
- Acceptance criteria sections
- Business rules sections

**Common requirement patterns**:

```text
"The system shall send email notifications to approvers within 5 minutes"
→ BR-001: Email Notification Timeliness
   Category: Notification
   Priority: High

"Invoices over $10,000 require VP approval"
→ BR-002: High-Value Invoice Approval
   Category: Approval Workflow
   Priority: Critical

"File must be in CSV format with pipe delimiter"
→ BR-003: File Format Specification
   Category: Data Integration
   Priority: High
```

### Separating IPA vs LPL Requirements

**IPA Requirements** (Process Automation):
- Approval routing and logic
- Email notifications
- Workflow actions
- Business class queries
- Integration with external systems
- Error handling
- Scheduled processing
- File processing

**LPL Requirements** (UI/Form Changes):
- Field protection and visibility
- Default value population
- Required field validation
- Form layout changes
- Button actions
- Menu modifications
- List configurations

**Example Separation**:

ANA-050 states: "Invoice amount field should be protected after submission, and approver should receive email notification"

- **IPA**: Send email notification to approver (process automation)
- **LPL**: Protect invoice amount field after submission (UI change)

## Related References

- `COMMON_ISSUES.md` - Known issues and troubleshooting
- `WORKFLOW_GUIDE.md` - Complete workflow for generating client handover documentation
- `PHASE3_CONFIGURATION_GUIDE.md` - Configuration extraction patterns
- `JSON_SCHEMAS.md` - Data structure specifications


---
inclusion: auto
name: process-patterns
description: IPA process patterns library with 450+ analyzed workflows, approval patterns, interface patterns, EDI, file processing, GL interfaces. Use when creating new LPD files, analyzing existing processes, troubleshooting workflows, or designing approval hierarchies.
---

# Process Patterns Library

## Table of Contents

- [Purpose and Scope](#purpose-and-scope)
- [Quick Reference](#quick-reference)
  - [Pattern Selection Guide](#pattern-selection-guide)
  - [Common Activity Types](#common-activity-types)
  - [Key Design Patterns](#key-design-patterns)
- [Error Patterns](#error-patterns)
  - [System Errors](#system-errors)
  - [Configuration Errors](#configuration-errors)
  - [Authentication Errors](#authentication-errors)
  - [FSM Security Errors](#fsm-security-errors)
- [Approval Patterns](#approval-patterns)
  - [Multi-Level Approval Pattern](#multi-level-approval-pattern)
  - [Reason Code Pattern](#reason-code-pattern)
  - [Department Transaction Approval](#department-transaction-approval)
  - [Cash Ledger Payment Approval](#cash-ledger-payment-approval)
  - [Contract Negotiation Final Approval](#contract-negotiation-final-approval)
- [Financial Processing Patterns](#financial-processing-patterns)
- [Interface Patterns](#interface-patterns)
  - [OAuth2 Authentication Pattern](#oauth2-authentication-pattern)
  - [Bank Reconciliation Interface](#bank-reconciliation-interface)
  - [DNA GL Interface](#dna-gl-interface)
- [File Generation Patterns](#file-generation-patterns)
- [EDI Processing Patterns](#edi-processing-patterns)
- [IPD Sample Solutions](#ipd-sample-solutions)
- [Troubleshooting Patterns](#troubleshooting-patterns)
  - [Column Mapping Mismatch in File Transformations](#column-mapping-mismatch-in-file-transformations)
- [Implementation Guidelines](#implementation-guidelines)
- [Pattern Library Summary](#pattern-library-summary)
- [Quick Pattern Lookup](#quick-pattern-lookup)

## Purpose and Scope

This is a reference library of 450+ analyzed IPA (Infor Process Automation) process patterns from production implementations. Use these patterns to:

- Design new LPD files based on proven approaches
- Understand common workflow structures and routing logic
- Troubleshoot existing process issues by comparing against working patterns
- Implement approval hierarchies, interfaces, and file processing workflows
- Identify reusable code patterns and activity sequences

**Key Principle**: Adapt patterns to specific requirements rather than copying verbatim. Each pattern demonstrates proven approaches that can be customized for your use case.

## Quick Reference

### Pattern Selection Guide

Choose the appropriate pattern based on your use case:

| Use Case                 | Recommended Pattern                   | Reference File                       |
|--------------------------|---------------------------------------|--------------------------------------|
| Multi-level approval     | Department Transaction Approval       | DepartmentTransactionApproval.lpd    |
| Payment approval         | Cash Ledger Payment Approval          | CashLedgerPaymentApproval.lpd        |
| Contract approval        | Contract Negotiation Final Approval   | CMContNegFinalAppr.lpd               |
| File interface           | Bank Reconciliation Interface         | CheckReconCLInterface.lpd            |
| GL interface             | DNA GL Interface                      | DNAGLInterface.lpd                   |
| EDI processing           | EDI Data Exchange Inbound             | EDIDataExchange_Inbound.lpd          |
| File generation          | Dunning Letter CSV Generation         | DunningLetterCSVFileGeneration.lpd   |
| Minimal callback         | Budget Edit Callback                  | BudgetEditCallBack.lpd               |
| OAuth2 integration       | CheckRecon or DNA patterns            | Multiple files                       |

### Common Activity Types

Understanding activity types is essential for building IPA processes:

| Activity Type | Purpose                                    | Typical Usage                                                |
|---------------|--------------------------------------------|--------------------------------------------------------------|
| `LM`          | Landmark transaction (query/update FSM data) | Retrieve approval levels, update business object status      |
| `UA`          | User Action (approval/rejection)           | Multi-level approval workflows with timeout escalation       |
| `BRANCH`      | Conditional routing                        | Route based on approval level, reason codes, error conditions |
| `ASSGN`       | Variable assignment                        | Set flags, calculate values, prepare data for next activity  |
| `JSONPARSER`  | Parse JSON input                           | Process external system data, extract transaction details    |
| `EMAIL`       | Send email notification                    | Approval requests, error alerts, status updates              |
| `EDIEX`       | EDI exchange                               | Inbound/outbound EDI file transfer with carriers             |
| `SUBPROC`     | Call sub-process                           | Concurrency checks, reusable logic modules                   |
| `WEBRN`       | Web service call                           | REST API calls, OAuth2 authentication, external integrations |

### Key Design Patterns

These patterns appear repeatedly across successful implementations:

1. **Multi-Level Approval**: Query approval level → Branch (level 0 = done) → User action → Update level → Loop back
2. **Reason Code Logic**: Query reason code flag → Branch → Route to appropriate user action (with/without reason code)
3. **OAuth2 Authentication**: Select credentials by environment → Acquire token → Set headers → Make API call
4. **File Processing**: Monitor directory → Read file → Parse/transform → Process → Archive/error handling
5. **Error Recovery**: Try operation → Branch on error code → Send notification → Route to error/success path
6. **Concurrency Control**: Check for concurrent work units → Branch (if running, exit; if not, proceed)
7. **JSON Input Processing**: Parse JSON → Extract fields → Validate → Process business logic

## Error Patterns

**Purpose**: Common error patterns from production IPA processes with root causes and resolution strategies. Use these to diagnose issues quickly and implement proper error handling.

### System Errors

#### Timeout Escalation Pattern (WU 10141)

**Symptoms**: Single line timeout message, process hanging, system intervention
**Pattern**: `Timeout escalation: Dispatch Action taken by system for [WorkUnit]`
**Root Cause**: Process execution exceeding configured timeout thresholds

**Resolution**:

1. Optimize process performance (reduce queries, improve logic efficiency)
2. Implement timeout handling in user actions
3. Review escalation configuration settings
4. Consider breaking into smaller sub-processes for long-running operations

#### OAuth Configuration Error Pattern (WU 7868)

**Symptoms**: JSON parsing failure, HTTP 400 Bad Request, malformed URLs, blank email addresses
**Pattern**: `SyntaxError: Empty JSON string` → `HTTP 400: Ambiguous URI empty segment`
**Root Cause**: Empty service account configuration, missing OAuth credentials

**Resolution**:

1. Validate service account JSON before parsing (check for empty strings)
2. Implement null checks for OAuth credentials
3. Test API authentication with valid credentials before deployment
4. Add error handling for malformed URLs in WEBRN activities

#### Security Proxy Configuration Error Pattern (WU 8464)

**Symptoms**: User delegation failures, SMTP server unavailable, cascading errors across activities
**Pattern**: `User [user] is not configured to run as a proxy for grantor [grantor]`
**Root Cause**: Proxy user not configured in FSM security settings

**Resolution**:

1. Configure user delegation in FSM security settings (Admin → Security → User Delegation)
2. Validate SMTP connectivity before sending emails
3. Test proxy user configuration with sample work unit
4. Implement alternative notification methods (in-app notifications, logging)

### Configuration Errors

#### Missing Configuration Variables

**Symptoms**: Process fails immediately, undefined variable errors, file access failures
**Example**: MatchReport_Outbound process (WU 3589)
**Root Cause**: Required configuration variables not defined (FileName, ProcessedFileDirectory, MonitorDirectory)

**Resolution**:

1. Define all required variables in process configuration or Start activity
2. Implement null checks before variable usage (ES5 compatible):

   ```javascript
   if (typeof FileName === 'undefined' || FileName === '') {
       FileName = '/default/path/file.txt';
   }
   ```

3. Add default values for missing configuration parameters
4. Validate file paths and directory permissions before file operations

#### CSV Delimiter Mismatch

**Symptoms**: Zero records processed (TotalRec = 0), parsing failures, empty result sets
**Example**: GeoSyntec Virtual Card GL Interface (WU 3141)
**Root Cause**: JavaScript uses wrong delimiter for CSV file format

**Resolution**:

```javascript
// WRONG: Pipe delimiter for comma-delimited CSV
var inputDelimiterPattern = /\|(?=(?:(?:[^"]*"){2})*[^"]*$)/;

// CORRECT: Comma delimiter (handles quoted fields with commas)
var inputDelimiterPattern = /,(?=(?:(?:[^"]*"){2})*[^"]*$)/;

// CORRECT: Tab delimiter
var inputDelimiterPattern = /\t(?=(?:(?:[^"]*"){2})*[^"]*$)/;
```

**Key Point**: Always verify the actual file delimiter before implementing parsing logic. Test with sample data.

### Authentication Errors

#### OAuth Configuration Error

**Symptoms**: HTTP 400 Bad Request, empty JSON string errors, malformed URLs
**Example**: IMS smoke test currency (WU 7868)
**Root Cause**: Empty service account configuration, JSON parsing failure

**Resolution**:

1. Validate service account JSON before parsing
2. Implement null checks for OAuth credentials
3. Test API authentication with valid credentials
4. Add error handling for malformed URLs

#### Security Proxy Configuration Error

**Symptoms**: User delegation failures, SMTP server unavailable, cascading errors
**Example**: Immediate approval process (WU 8464)
**Pattern**: `User [user] is not configured to run as a proxy for grantor [grantor]`

**Resolution**:

1. Configure user delegation in FSM security settings
2. Validate SMTP connectivity before sending emails
3. Test proxy user configuration
4. Implement alternative notification methods

#### SFTP Authentication Failure

**Symptoms**: `FileTransfer: SshException: No more authentication methods available`

**Resolution**:

1. Verify SFTP credentials (username/password)
2. Test authentication method (password vs key-based)
3. Validate SFTP server connectivity and firewall rules
4. Check network access and port availability

### FSM Security Errors

#### New Account Security Role Issues

**Symptoms**: Element not found errors, different FSM interface layout, work unit search unavailable
**Pattern**: `no such element: Unable to locate element: {"method":"xpath","selector":"//input[@type='text'][3]"}`
**Root Cause**: New FSM accounts lack required security roles for work unit page access

**Resolution**:

1. Contact FSM administrator to verify role assignments
2. Required roles: "Work Unit Administrator", "Process Administrator", "System Administrator"
3. Navigate to work units page manually to verify access level
4. Use manual work unit analysis while waiting for roles
5. Submit formal security role request to FSM admin

#### Timeout Escalation

**Symptoms**: Single line timeout message, process hanging
**Pattern**: `Timeout escalation: Dispatch Action taken by system for [WorkUnit]`
**Root Cause**: Process execution exceeding timeout thresholds

**Resolution**:

1. Optimize process performance (reduce queries, improve logic)
2. Implement timeout handling in user actions
3. Review escalation configuration
4. Consider breaking into smaller sub-processes

## Approval Patterns

**Purpose**: Multi-level approval workflows with dynamic routing, escalation, and reason code support. These patterns handle complex approval hierarchies common in financial and procurement systems.

**Common Features Across All Approval Patterns**:

- Dynamic approval levels retrieved from FSM business objects
- Escalation management with configurable timeouts
- Reason code support (conditional or mandatory)
- Email notifications with rich HTML content
- Milestone tracking for multi-level approvals
- Audit trail maintenance

### Multi-Level Approval Pattern

**Standard Flow**:

1. Query approval level information (ApprovalLevel, DerivedCurrentApprovalResource, etc.)
2. Branch on ApprovalLevel (0 = complete, >0 = continue)
3. User action with approve/reject options and timeout escalation
4. Update approval level or complete process based on decision
5. Handle escalation on timeout

**Key Activities**:

```xml
<!-- Get Approval Level Info -->
<activity activityType="LM" caption="GetApprovalLevelInfo">
    <prop name="transactionString">
        _dataArea="<!appProdline>" & _module="[module]" & _objectName="[object]" &
        _actionName="Find" & _actionType="SingleRecordQuery" &
        [key fields] &
        ApprovalLevel & DerivedCurrentApprovalResource & DerivedCurrentApprovalActor &
        DerivedCurrentApprovalTeam & DerivedCurrentTeamActorList &
        DerivedCurrentApproverEscalationDays & DerivedCurrentApproverEscalationHours
    </prop>
</activity>

<!-- Approval Level Check -->
<activity activityType="BRANCH" caption="CheckApprovalLevel">
    <prop name="conditions">
        <condition name="Complete" expr="ApprovalLevel == 0" btexe="EndActivity"/>
        <condition name="Continue" expr="ApprovalLevel > 0" btexe="UserAction"/>
    </prop>
</activity>
```

**Implementation Notes**:

- Always query approval level at the start of each iteration
- Use derived fields (DerivedCurrentApprovalResource, etc.) for dynamic approver assignment
- Implement proper escalation handling with configurable timeouts
- Maintain state flags (IsEscalated, IsReassigned) for audit trails

### Reason Code Pattern

**When to Use**: Processes requiring mandatory reason codes for rejections or specific actions (common in financial approvals, contract modifications).

**Implementation**:

```xml
<!-- Check Reason Code Requirement -->
<activity activityType="BRANCH" caption="NeedReasonCode?">
    <prop name="conditions">
        <condition name="Not Required" expr="RejectReasonCodeRequired == false" btexe="StandardUserAction"/>
        <condition name="Required" expr="RejectReasonCodeRequired == true" btexe="ReasonCodeUserAction"/>
    </prop>
</activity>
```

**User Action Types**:

- **Standard**: Approve/Reject without mandatory reason codes (faster for routine approvals)
- **Reason Code**: Approve/Reject with mandatory reason code collection (audit compliance)

**Best Practices**:

- Query reason code requirement flag from business object configuration
- Provide clear reason code options relevant to the business process
- Capture both reason code and free-text comments for audit trails
- Consider making reason codes mandatory for rejections but optional for approvals

### Department Transaction Approval

**File**: DepartmentTransactionApproval.lpd
**Use Case**: GL department transaction approval with JSON input processing
**Key Features**:

- JSON input parsing from external systems
- Dynamic approval levels
- Conditional reason code logic
- Escalation management
- State tracking (escalation/reassignment flags)

**Process Flow**:

1. Parse JSON input (_inputData) → Extract transaction details
2. Query approval level information
3. Branch on ApprovalLevel (0 = done, >0 = continue)
4. Branch on reason code requirement
5. User action (standard or with reason code)
6. Update approval level or complete

**Technical Details**:

```xml
<!-- JSON Input Processing -->
<activity activityType="JSONPARSER" caption="JSON Parser">
    <prop name="varText">
        GeneralLedgerDepartmentTransaction->GeneralLedgerDepartmentTransaction<!GeneralLedgerDepartmentTransaction
        GeneralLedgerDepartmentTransaction->FinanceEnterpriseGroup<!FinanceEnterpriseGroup
    </prop>
    <prop name="jsonText"><!_inputData></prop>
</activity>
```

### Cash Ledger Payment Approval

**File**: CashLedgerPaymentApproval.lpd
**Use Case**: Complex payment approval with multi-path routing
**Key Features**:

- Multiple user action types (One Approver, Many Approvers, Assigned Approver)
- Approver count logic (single vs multiple)
- Assignment management ("Assign To Me", "Unassign From Me")
- Reason code support
- Complex routing based on multiple conditions

**User Action Types**:

- **One Approver**: Single approver scenarios
- **Many Approvers**: Team-based approval with assignment
- **Assigned Approver**: Individual assignment with unassignment option
- Each type has reason code variant

### Contract Negotiation Final Approval

**File**: CMContNegFinalAppr.lpd
**Use Case**: Contract approval with terms modification tracking
**Key Features**:

- Terms modification detection (DerivedPFFinalApproverTermsModified flag)
- Dual path routing (terms modified vs not modified)
- Three-level approval hierarchy
- Contract state branching (Released, Addendum, Amendment)
- Triple action support (Approve/Submit Changes, Reject, Disapprove)

**Process Flow**:

1. Check if terms modified at each level
2. Route to appropriate user action based on terms status
3. Branch on contract state (Released/Addendum/Amendment)
4. Execute appropriate Landmark action based on decision
5. Send context-aware email notifications

### Depreciation Approval

**File**: DepreciationApproval.lpd
**Use Case**: Asset management depreciation approval
**Key Features**:

- BookCalendar object operations
- Rich HTML email notifications with invoice details
- Multi-level approval with escalation
- Service classification ("CloseApproval")

**Email Notification Example**:

```xml
<prop name="actionNotifyEmailContent">
    The following invoice has been submitted for your approval:<br>
    Company: <!ApCompany><br>
    Vendor: <!VendorName><br>
    Invoice: <!Invoice><br>
    Invoice Date: <!InvoiceDate><br>
    Due Date: <!DueDate><br>
    Amount: <!InvoiceAmount><br>
    AP Clerk: <!APClerkName><br>
    Click <a href="[URL]">here</a> to review invoice.
</prop>
```

### Detail Payment Void/Stop Pay Approval

**File**: DetailPaymentVoidStopPayApproval.lpd
**Use Case**: Cash ledger payment void/stop operations
**Key Features**:

- CashLedgerPayablesPayment object operations
- Bank transaction tracking (BankTransactionCode, TransactionIDNumber)
- Conditional reason code logic
- Service classification ("CMContNegFinalApprNoUpdate")

### Budget Edit Callback

**File**: BudgetEditCallBack.lpd
**Use Case**: Minimal callback process for notifications
**Key Features**:

- Simple start-to-end flow
- No user interaction
- Lightweight processing
- Minimal resource usage

**When to Use**: Callback/notification scenarios requiring minimal overhead.

## Financial Processing Patterns

**Purpose**: Financial transaction processing including GL interfaces, payment processing, and bank reconciliation. These patterns handle complex financial workflows with proper controls and audit trails.

### Bank Statement Distribution Approval

**File**: BankStatementDistributionApproval.lpd
**Use Case**: Cash management bank statement distribution approval
**Key Features**:

- BankStatement object operations
- Reason code logic (RejectStatementDistribReasonCodeRequired)
- Multi-level approval with escalation
- Financial controls for cash management

### Billing Invoice Output

**File**: BillingInvoiceOutput.lpd
**Use Case**: Invoice file generation and distribution
**Key Features**:

- Timestamp-based file naming for uniqueness
- Data aggregation (header + detail records)
- File attachment to business objects for audit trail
- Optional FTP distribution to external systems
- Automatic file cleanup to prevent disk space issues

**Process Flow**:

1. Generate output file with timestamp
2. Combine header and detail records
3. Attach file to business object
4. Conditional FTP transfer (if destination configured)
5. Delete temporary files

## Interface Patterns

**Purpose**: Integration with external systems via files, APIs, and EDI. These patterns demonstrate proven approaches for data exchange, authentication, and error handling.

### OAuth2 Authentication Pattern

**When to Use**: API integrations requiring OAuth2 token-based authentication (common for modern REST APIs, cloud services).

**Implementation**:

```javascript
// Environment-specific credential selection
OauthCreds = FEG == "AGW" ? _configuration.Interface.API_AuthCred_AGW :
             FEG == "AGC" ? _configuration.Interface.API_AuthCred_AGC :
             FEG == "FCIL" ? _configuration.Interface.API_AuthCred_FCIL :
             FEG == "FMFC" ? _configuration.Interface.API_AuthCred_FMFC :
             FEG == "FCE" ? _configuration.Interface.API_AuthCred_FCE : "";

// Token acquisition (password grant type)
req = "grant_type=password&username=" + ClientUsername + 
      "&password=" + ClientPassword + "&scope=&client_id=" + ClientID + 
      "&client_secret=" + ClientSecret;
```

**Best Practices**:

- Store credentials in configuration variables (never hardcode)
- Implement environment-specific credential selection
- Cache tokens to reduce authentication calls
- Handle token expiration and refresh logic
- Add error handling for authentication failures

### Bank Reconciliation Interface

**File**: CheckReconCLInterface.lpd
**Use Case**: Bank reconciliation with OAuth2 and file processing
**Key Features**:

- File processing workflow (Monitor → Process → Archive/Error)
- OAuth2 authentication with multi-environment support
- Data transformation (fixed-width → CSV → JSON)
- Variance detection and reporting
- Error recovery with flag file management

**Process Flow**:

1. Monitor directory for input files
2. Authenticate via OAuth2
3. Read and parse fixed-width file
4. Transform to CSV then JSON
5. Process reconciliation
6. Archive or route to error directory

### DNA GL Interface

**File**: DNAGLInterface.lpd
**Use Case**: Custom GL interface with API-based processing
**Key Features**:

- Multi-environment support (AGW, AGC, FCE, FCIL, FMFC)
- OAuth2 authentication
- Fixed-width file parsing
- CSV to JSON transformation
- REST API calls (vs traditional Landmark activities)
- Same business logic as standard solution (GLTransactionInterface.InterfaceTransactions)
- Run group management with duplicate detection

**Technical Implementation**:

```javascript
// Fixed-width field extraction
InstitutionNbr = fileRecArr[i].substring(0, 4);
CompanyEntityBranchCostCenter = fileRecArr[i].substring(4, 15);
AccountSubaccount = fileRecArr[i].substring(15, 24);
TransactionCode = fileRecArr[i].substring(40, 42);
Amount = fileRecArr[i].substring(42, 55);
EffectiveDate = fileRecArr[i].substring(119, 127);

// Entity-specific account code formatting
if (FEG == "AGW") {
    AccountingEntity = "18";
    if (fileRecArr[i].substring(20, 24) == "0000") {
        AccountCode = fileRecArr[i].substring(15, 20);
    } else {
        AccountCode = fileRecArr[i].substring(15, 20) + "-" + fileRecArr[i].substring(20, 24);
    }
}

// CSV to JSON transformation
function csvJSON(csv) {
    var lines = csv.split("\n");
    var result = [];
    var headers = lines[0].split(",");
    
    for(var i=1; i<lines.length; i++) {
        var obj = {};
        var currentline = lines[i].split(",");
        for(var j=0; j<headers.length; j++) {
            obj[headers[j]] = currentline[j];
        }
        var div = '{"message": "BatchImport","_fields": '+JSON.stringify(obj)+'}';
        result.push(div);
    }
    return '{"_records": ['+result+']}';
}
```

### Error Notification Callback Pattern

**When to Use**: Interface processes that need to notify external systems when FSM import/processing fails (common for bidirectional integrations with third-party systems like Coupa, Workday, etc.).

**Use Case**: After importing data from an external system into FSM, send error notifications back to the source system for records that failed validation or processing.

**Key Features**:

- Query FSM business class for records with `RecordInError = true`
- Build error list with invoice/transaction IDs and error messages
- Loop through error records and call external API
- Only notify for records with valid external system IDs
- Separate error notification from success processing

**Process Flow**:

1. Import data into FSM (DBImport, Landmark transactions, etc.)
2. Query business class for error records by run group
3. Build error invoice list with details
4. ForEach loop through error list
5. Branch: Check if external system ID exists
6. WebRun: Send error notification to external API
7. Email: Notify internal team of interface errors

**Implementation**:

```xml
<!-- Query Error Records from FSM Business Class -->
<activity activityType="LM" caption="GetErrorRecords">
    <prop name="transactionString">
        _dataArea="<!appProdline>" & _module="ap" & 
        _objectName="PayablesInvoiceImport" & 
        _actionName="Find" & _actionType="MultipleRecordQuery" &
        _filterString=RecordInError = "true" &
        _setName="ByRunGroup" &
        RunGroup="<!vRunGroup>" &
        Company & Vendor & Invoice & ErrorMessage & ExternalSystemId
    </prop>
</activity>

<!-- Build Error List -->
<activity activityType="ASSGN" caption="BuildErrorList">
    <prop name="script">
        if(vInvoiceInterfaceError != "") {
            vInvoiceInterfaceError = vInvoiceInterfaceError + NL + 
                ExternalSystemId + "|" + vRunGroup + "|" + 
                Company + "|" + Vendor + "|" + Invoice + "|" + 
                ErrorMessage;
        } else {
            vInvoiceInterfaceError = ExternalSystemId + "|" + vRunGroup + "|" + 
                Company + "|" + Vendor + "|" + Invoice + "|" + 
                ErrorMessage;
        }
    </prop>
</activity>

<!-- Loop Through Error Records -->
<activity activityType="FOREACH" caption="ForEachError">
    <prop name="arrayVariable">vInvoiceInterfaceError</prop>
    <prop name="delimiter">NL</prop>
</activity>

<!-- Check External System ID Exists -->
<activity activityType="BRANCH" caption="HasExternalId?">
    <prop name="conditions">
        <condition name="No ID" expr="vExternalId == 0 || vExternalId == ''" btexe="EndForEach"/>
        <condition name="Has ID" expr="vExternalId != 0 &amp;&amp; vExternalId != ''" btexe="WebRunErrorNotif"/>
    </prop>
</activity>

<!-- Send Error Notification to External System -->
<activity activityType="WEBRN" caption="WebRunErrorNotif">
    <prop name="url">https://api.externalsystem.com/api/invoices/<!vExternalId></prop>
    <prop name="method">POST</prop>
    <prop name="requestBody">
        <![CDATA[<?xml version="1.0" encoding="UTF-8" ?>
        <root>
            <custom-fields>
                <custom-field>
                    <name>FSM-Import-Status</name>
                    <value>Error</value>
                </custom-field>
                <custom-field>
                    <name>FSM-Error-Message</name>
                    <value><!vErrorMessage></value>
                </custom-field>
            </custom-fields>
        </root>]]>
    </prop>
</activity>
```

**Best Practices**:

- Always query by run group to isolate current batch errors
- Only send notifications for records with valid external system IDs
- Include detailed error messages in the callback payload
- Log all API responses for troubleshooting
- Send internal email notification summarizing all errors
- Consider retry logic for transient API failures
- Use separate WebRun nodes for error vs success notifications

**Common Pitfall**: Don't assume all records need error notifications. Only records with `RecordInError = true` AND a valid external system ID should trigger callbacks.

**Real-World Example**: Coupa expense report integration where FSM validates distributions. If validation fails (e.g., "Distributions required for open invoice"), FSM updates the expense report status in Coupa via API callback so users can correct the issue in the source system.

**Entity Configurations**:

- **AGW**: AccountingEntity=18, supports sub-accounts with dash notation
- **AGC**: AccountingEntity=72, simple account format
- **FCE**: Dynamic AccountingEntity from file
- **FCIL**: AccountingEntity=14
- **FMFC**: AccountingEntity=962

### Contract Final Approval Workflow

**File**: cmcontfinalappr.lpd
**Use Case**: Multi-level contract approval
**Key Features**:

- Conditional routing (regular contracts, addendums, amendments)
- Three-level approval hierarchy
- Milestone tracking
- Landmark integration for status updates
- Rich email notifications

## File Generation Patterns

**Purpose**: Generate output files (CSV, text, EDI) with proper formatting and distribution. These patterns handle file creation, formatting, attachment, and distribution to external systems.

### Dunning Letter CSV Generation

**File**: DunningLetterCSVFileGeneration.lpd
**Use Case**: Generate dunning letter CSV files with FTP distribution
**Key Features**:

- Dynamic timestamp-based file naming for uniqueness
- Header/detail pattern (47-field CSV structure)
- File attachment to business objects for audit trail
- Conditional FTP transfer to external systems
- Automatic file cleanup to prevent disk space issues

**Process Flow**:

1. Format timestamp for file naming
2. Query DunningCSVOutput header
3. Generate CSV header (47 fields)
4. Iterate detail records (DunningCSVOutputDetail)
5. Write CSV file
6. Attach to business object
7. Conditional FTP transfer
8. Delete temporary files

**File Naming Convention**:

```javascript
function formatDate(dt) {
    var d = new Date(dt);
    var padMonth = (d.getMonth()+1).toString().length == 1 ? '0' + (d.getMonth()+1).toString() : (d.getMonth()+1).toString();
    var padDay = d.getDate().toString().length == 1 ? '0' + d.getDate().toString() : d.getDate().toString();
    return d.getFullYear().toString().substring(2) + padMonth + padDay;
}

DetailFile = DataFileDirectory + "/" + GetHeader_CSVFileNameOutputFileName + FileTimeStamp + ".csv";
```

**CSV Fields** (47 total):

- Customer Information: Company, Customer, CustomerName, CustomerTaxID
- Address: CustomerDAAddr1-4, City, PostalCode, State, Country
- Credit Agency: Name, Address fields, City, State, Country
- Dunning Details: CycleID, Level, TextCode, Text1-12
- Financial: CurrentBalance, DunningFee, TransactionAmount, PastDueAmount
- Transaction: Invoice, Type, Date, DueDate, DueDays

**Best Practices**:

- Always use timestamp-based file naming to prevent overwrites
- Implement proper CSV escaping for fields containing commas or quotes
- Validate all required fields before file generation
- Test FTP connectivity before attempting transfer
- Maintain audit trail by attaching files to business objects

## EDI Processing Patterns

**Purpose**: EDI file exchange and processing (inbound/outbound). These patterns handle EDI transactions with carriers, translation, and error handling.

### EDI Data Exchange Inbound Translation

**File**: EDIDataExchange_Inbound_Translate.lpd
**Use Case**: EDI inbound with translation
**Key Features**:

- EDI exchange activity (file retrieval from carriers)
- Translation integration (TranslateInbound action)
- Dual email notifications (success/error paths)
- Carrier variable mapping
- File count tracking for monitoring
- Error code branching for proper error handling

**Process Flow**:

1. EDI exchange (retrieve files from carriers)
2. Handle undefined variables
3. Branch on error code
4. Send appropriate email notification
5. Process inbound EDI translation
6. Complete

**Email Notification Pattern**:

```xml
<!-- Success Email -->
<prop name="content">
    Carrier Name: <!EDIExchange_ediCarrier>
    WorkUnit: <!WorkUnit>
    Work Title: <!Description>
    ProcessName: <!ProcessName>
    Total Files Successfully Retrieved: <!EDIExchange_processedFileCount>
    Files Retrieved: <!EDIExchange_processedFileList>
</prop>

<!-- Error Email -->
<prop name="content">
    Errors occurred retrieving files from <!EDIExchange_ediCarrier>
    Error Messages: <!EDIExchange_returnMessage>
</prop>
```

**Best Practices**:

- Always implement both success and error email notifications
- Track file counts for monitoring and troubleshooting
- Log carrier information for audit trails
- Handle undefined variables gracefully

### EDI Data Exchange Outbound Single

**File**: EDIDataExchange_Outbound_Single.lpd
**Use Case**: Single-instance EDI outbound with concurrency control
**Key Features**:

- Concurrency control (CheckForConcurrentWorkUnits sub-process)
- Outbound direction (dirSelection=1)
- Single instance design (prevents concurrent execution)
- Error handling with email notifications

**Concurrency Pattern**:

```xml
<!-- Concurrency Check -->
<activity activityType="SUBPROC" caption="CheckForConcurrency">
    <prop name="subProcessName">CheckForConcurrentWorkUnits</prop>
</activity>

<!-- Branch Logic -->
<activity activityType="BRANCH" caption="AreThereConcurrent">
    <prop name="conditions">
        <condition name="NoConccurentRunning" expr="!ActiveWorkUnitsExist" btexe="EDIExchange"/>
        <condition name="ConcurentRunning" expr="ActiveWorkUnitsExist" btexe="End"/>
    </prop>
</activity>
```

### EDI 822 Bank Fee Statement

**File**: EDI822BankFeeStatementData.lpd
**Use Case**: Bank statement interface with EDI 822 format
**Key Features**:

- BankStatementInterfaceHeader creation
- EDI 822 format specialization (FileFormat=60)
- Auto import logic (conditional)
- Multi-stage processing (header → task → import decision)
- Channel integration (routing)

**Technical Implementation**:

```xml
<!-- Bank Statement Interface Header -->
<activity activityType="LM" caption="CreateBSIH">
    <prop name="transactionString">
        _dataArea=<!appProdline> & _module="cashmgmt" & _objectName="BankStatementInterfaceHeader" &
        _actionName="Create" & _actionType="CreateUpdateDelete" &
        Filename=<!FileName> & Data=<!_inputData> & Workunit=<!WorkUnit> &
        FileFormat="60" & Channel=<!Channel> & Receiver=<!Receiver>
    </prop>
</activity>

<!-- Auto Import Decision -->
<activity activityType="BRANCH" caption="Branch">
    <prop name="conditions">
        <condition name="Auto Import" expr="AutoImport==true" btexe="ImportAction"/>
        <condition name="Manual Import" expr="true" btexe="End"/>
    </prop>
</activity>
```

### EDI 832 Import

**File**: EDI832Import.lpd
**Use Case**: Minimal EDI 832 catalog import
**Key Features**:

- Simple start → landmark → end flow
- EDI 832 specialization (catalog price/sales information)
- File attachment (XML to Edi832StageFile object)
- Basic error notification

## IPD Sample Solutions

**Purpose**: Reference templates from Infor Process Designer sample solutions (100+ templates). These provide starting points for common business processes.

### Activity Approval Patterns

- **actaddapproval.lpd**: Activity addition approval with email notifications, S3 queries, configuration-based addressing
- **actbudchgreq.lpd**: Budget change request workflows with multi-level approval and budget validation
- **jeapproval.lpd**: Journal entry approval with financial hierarchies and audit trails

### Purchase Order Processing

- **poapprove.lpd**: PO approval with vendor validation, budget checking, multi-level authorization
- **Buyer_POApproval_A/B.lpd**: Buyer-specific PO approvals with role-based routing and conditional paths

### Financial Controls

- **apglapproval.lpd**: AP GL approval with account validation and financial controls
- **costallocation.lpd**: Cost allocation with department/project distribution and reporting

### ION Integration Patterns

- **ION_actaddapproval.lpd**: ION-enabled activity approvals with message processing and event-driven workflows
- **ION_jeapproval2.lpd**: Enhanced ION journal entry approval with advanced routing and BOD processing

### Notification and Communication

- **LSRIPA_Default_Process.lpd**: Default notification template with HTML email formatting, dynamic content, report links

### Warehouse and Inventory

- **whshipment.lpd**: Warehouse shipment processing with inventory updates and shipping notifications
- **whbatch.lpd**: Warehouse batch processing with bulk operations and status tracking

### Credit and Risk Management

- **creditchkfail.lpd**: Credit check failure handling with risk assessment and automated holds
- **pcardrequest.lpd**: Procurement card request with approval workflows and credit limit management

### IPD Technical Architecture

**Core Dependencies**:

- BPM Framework: bpm-commons.jar, bpm-interfaces.jar
- Security: clientsecurity.jar, security.jar
- Integration: webservs.jar, axis2, cxf libraries
- Database: JDBC drivers (SQL Server, Oracle, DB2)
- Cloud Services: aws-java-sdk.jar
- Third-party: Jackson, Apache Commons, Log4j

**Display Templates** (LSODisplays):

- **disptemplate.xml**: Standard display with query-driven data, grid/list components, form integration
- **effortcert.xml**: Effort certification displays with time tracking and compliance reportingporting

**Configuration Management**:

- Multi-environment: 21+ configured environments
- Connection management: CloudSuite HTTPS endpoints
- User context: Role-based access control
- Debug support: Development and troubleshooting tools

## Troubleshooting Patterns

**Purpose**: Common troubleshooting scenarios and diagnostic approaches for IPA process failures. Use these patterns to quickly identify and resolve production issues.

### Column Mapping Mismatch in File Transformations

**Symptom**: All records fail validation with the same error (e.g., "Item: 0 does not exist") despite input file containing valid data.

**Root Cause**: JavaScript column index configuration doesn't match actual input file format.

**Example Case** (WU 4014 - RHR_SCM_POS_Inbound_Agilisys):

**Input File Format**:
```
"E","20260305",3007,30,0,2606, 19.00,1.0000, 19.00
 [0]    [1]    [2] [3][4] [5]   [6]    [7]    [8]
```

**Incorrect Configuration**:
```javascript
var COL_ITEM = 4;           // Reading field [4] = 0 (placeholder)
var COL_UNIT_PRICE = 5;     // Reading field [5] = 2606 (actual item!)
var COL_QUANTITY = 6;       // Reading field [6] = 19.00 (actual price)
var COL_EXTENDED_AMOUNT = 7; // Reading field [7] = 1.0000 (actual qty)
```

**Result**: Process reads "0" as item number, fails validation, logs exception "Item: 0 does not exist" for every line.

**Diagnostic Steps**:

1. **Examine Exception Pattern**: If ALL records fail with identical error value, suspect column mapping issue
2. **Review Sample Input Data**: Look at raw input file content in work unit log (ReadFile_outputData variable)
3. **Count Fields**: Manually count comma-separated fields in sample data
4. **Compare to Configuration**: Check JavaScript COL_* variable definitions in Transform activity
5. **Verify Field Positions**: Confirm each COL_* index matches actual data position

**Resolution**:

```javascript
// Correct configuration
var COL_ITEM = 5;           // Now reads field [5] = 2606 ✓
var COL_UNIT_PRICE = 6;     // Now reads field [6] = 19.00 ✓
var COL_QUANTITY = 7;       // Now reads field [7] = 1.0000 ✓
var COL_EXTENDED_AMOUNT = 8; // Now reads field [8] = 19.00 ✓
```

**Prevention**:

1. **Document File Format**: Maintain clear documentation of expected input format with field positions
2. **Sample Data Testing**: Test with actual sample data during development
3. **Field Count Validation**: Add JavaScript validation to check expected field count:
   ```javascript
   if (fields.length < EXPECTED_FIELD_COUNT) {
       exceptions.push({
           lineNumber: lineNumber,
           reason: "Malformed line - expected " + EXPECTED_FIELD_COUNT + " fields, got " + fields.length
       });
       continue;
   }
   ```
4. **Configuration Comments**: Document field positions in JavaScript:
   ```javascript
   // Input format: "RecordType","Date",Location,Unused,Placeholder,Item,Price,Qty,ExtAmt
   var COL_RECORD_TYPE = 0;  // "E"
   var COL_POS_DATE = 1;     // "20260305"
   var COL_LOCATION = 2;     // 3007
   var COL_UNUSED = 3;       // 30
   var COL_PLACEHOLDER = 4;  // 0 (not used)
   var COL_ITEM = 5;         // 2606 (actual item number)
   ```

**Related Patterns**:

- Fixed-width file parsing with incorrect position/length specifications
- CSV files with optional fields causing index shifts
- Header row presence/absence causing off-by-one errors
- Quote-enclosed fields with embedded commas breaking simple split logic

**Key Takeaway**: When all records fail with the same constant value, the issue is almost always in the parsing logic, not the data itself. Always verify column mapping against actual input data format.

## Performance Optimization Patterns

### String Concatenation in Pagination Loops

**Context**: Common in Compass API pagination, file processing, data aggregation

**Anti-Pattern (O(n²) complexity)**:
```javascript
var OutputRecords = "";
while (hasMoreData) {
    var pageData = fetchPage();
    OutputRecords += pageData + "
";  // Creates new string each iteration
    offset += limit;
}
```

**Best Practice (O(n) complexity)**:
```javascript
var OutputRecordsArray = [];
while (hasMoreData) {
    var pageData = fetchPage();
    OutputRecordsArray.push(pageData);  // Reuses array memory
    offset += limit;
}
var OutputRecords = OutputRecordsArray.join("
");  // Single allocation
```

**Performance Impact**:
- 500 iterations: 45 minutes → 54 seconds (50x faster)
- Memory: 1.25GB → 5MB (250x less copying)

### Nested Loop Optimization

**Context**: Matching invoices to PO lines, vendor lookups, data correlation

**Anti-Pattern (O(n²) complexity)**:
```javascript
for (var i = 0; i < invoices.length; i++) {
    for (var j = 0; j < poLines.length; j++) {
        if (invoices[i].poNumber === poLines[j].poNumber) {
            // Match found
        }
    }
}
```

**Best Practice (O(n) complexity)**:
```javascript
// Build lookup map
var poLookup = {};
for (var i = 0; i < poLines.length; i++) {
    poLookup[poLines[i].poNumber] = poLines[i];
}

// Single loop with O(1) lookup
for (var i = 0; i < invoices.length; i++) {
    var poLine = poLookup[invoices[i].poNumber];
    if (poLine) {
        // Match found
    }
}
```

**Performance Impact**:
- 1,000 × 5,000 items: 5M comparisons → 6K operations (833x faster)

**Reference**: See `.kiro/skills/ipa-javascript-es5-analyzer/` for complete optimization guide.

## Implementation Guidelines

### Common Success Factors

When implementing IPA processes based on these patterns, follow these proven practices:

1. **Configuration-Driven Design**: Externalize environment-specific settings to configuration variables (never hardcode URLs, credentials, file paths)
2. **Comprehensive Error Handling**: Implement multiple error paths with specific handling for each error type
3. **Audit Trail Maintenance**: Complete logging of all decisions, actions, and state changes
4. **State Management**: Use clear process variables to track workflow state throughout execution
5. **User Experience**: Provide rich notifications with actionable content (links, context, next steps)
6. **System Integration**: Use proper Landmark activity syntax for data updates and queries

### Performance Considerations

1. **Batch Processing**: Group operations for efficiency (process multiple records in single query when possible)
2. **Async Operations**: Use non-blocking calls where possible to improve responsiveness
3. **Resource Management**: Proper cleanup of temporary files, connections, and cached data
4. **Caching**: Cache tokens and configuration data to reduce API calls and improve performance

### Security Best Practices

1. **Credential Management**: Secure storage and rotation of API credentials (use configuration variables, not hardcoded values)
2. **Access Control**: Role-based approval assignments using FSM security model
3. **Audit Logging**: Complete trail of all security-relevant events (who, what, when, why)
4. **Data Encryption**: Secure transmission of sensitive data (use HTTPS, SFTP, encrypted files)

### Reusable Design Patterns

1. **Property Initialization**: Configuration-driven property setup at Start activity
2. **Workflow Activities**: Standardized activity sequences and routing logic
3. **Error Handling**: Consistent error logging and notification across all processes
4. **Integration Points**: Standardized external system connections (OAuth2, SFTP, email)
5. **Customization**: Adapt patterns for specific business logic while maintaining core structure

### Learning Focus Areas

When studying these patterns, focus on:

- **Property Blocks**: How configuration variables are referenced and initialized
- **Activity Sequences**: Standard workflow patterns and routing logic
- **Error Handling**: How errors are detected, logged, and communicated
- **Integration Patterns**: ION, SFTP, email, and database connectivity approaches

## Pattern Library Summary

### Analyzed Patterns

**Total**: 450+ patterns from 51+ LPD files + IPD sample solutions + error patterns

**Categories**:

- **Approval workflows**: Multi-level, reason codes, escalation, team-based
- **Financial processing**: GL interfaces, payment processing, bank reconciliation
- **Interface patterns**: OAuth2, file processing, API integration, REST APIs
- **File generation**: CSV, text, EDI with FTP distribution
- **EDI processing**: Inbound/outbound, translation, concurrency control
- **Error patterns**: Configuration, authentication, security, system errors

### FSM_ION Integration Patterns (130+ Files)

**Naming Convention**: All files start with `FSM_ION_`

**Common Properties**:

- Data area, encoding type, locale
- Workfile import flag
- Business classes
- Output directory

**Activities**: Data synchronization, import/export, error handling

**Integration**: Heavy use of ION connectors and BOD (Business Object Document) patterns

### FSM_Strata Export Patterns (10 Files)

**Common Properties**:

- Checkpoint (Boolean)
- vInterfaceDirectory, vEmailFrom, vEmailTo
- vFileDelimiter, LastRunDate, vFileExtension

**Export Types**:

- AP/GL/PO Capital and Detail exports
- Inventory extracts
- Vendor exports

### GL & Financial Interface Patterns

- GL interfaces (automated, block funding, interest rate swaps, leasewave)
- Financial processing (payroll GL, non-accrual GL)
- Report generation (match reports, positive pay files, dunning letters)

### Contract & Vendor Management

- Contract processing (HealthTrust, Vizient GPO synchronization)
- Vendor workflows (request new vendor, update information, supplier approval)

### Sync & Bank Statement Patterns

**Bank Statement Formats**: BAI2, CAMT053, CAMT05X, CSV, MT940, MT942
**PGP Support**: Encrypted file processing variants
**Procurement Cards**: Master and Visa card synchronization

### Common Integration Points

- **ION Connectors**: Data exchange between FSM and external systems
- **Email Notifications**: Sender/recipient properties, triggered on completion or error
- **SFTP/FTP**: File transfers in export/import flows
- **Database Export**: Data area, business classes, output directory properties

### Error Handling Patterns (Universal)

- **Logging**: `<log>true</log>` and `<logString>` elements capture error details
- **Email Notification**: `<emailCon/>` triggers notifications on error
- **Return Messages**: Output data and error codes logged for troubleshooting

## Quick Pattern Lookup

Use these tables to quickly find the right pattern for your use case.

### By Business Function

| Function            | Pattern Files                                                                | Key Features                                                                 |
|---------------------|------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| AP Approval         | apglapproval.lpd, DetailPaymentVoidStopPayApproval.lpd                      | GL account validation, financial controls, void/stop operations             |
| GL Interface        | DNAGLInterface.lpd, GeoSyntec_INT_VirtualCard_GLInterface.lpd               | OAuth2, fixed-width parsing, CSV transformation, REST API                   |
| Contract Approval   | CMContNegFinalAppr.lpd, cmcontfinalappr.lpd                                 | Terms modification tracking, three-level hierarchy, state branching         |
| Bank Reconciliation | CheckReconCLInterface.lpd, BankStatementDistributionApproval.lpd            | OAuth2, file processing, variance detection, cash management                |
| EDI Processing      | EDIDataExchange_Inbound.lpd, EDI822BankFeeStatementData.lpd                 | Carrier integration, translation, concurrency control, format specialization |
| File Generation     | DunningLetterCSVFileGeneration.lpd, BillingInvoiceOutput.lpd                | Timestamp naming, header/detail pattern, FTP distribution, cleanup          |
| Asset Management    | DepreciationApproval.lpd                                                     | BookCalendar operations, rich HTML emails, multi-level approval             |

### By Technical Feature

| Feature                | Pattern Files                                                                | Implementation Notes                                                         |
|------------------------|------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| OAuth2 Authentication  | CheckReconCLInterface.lpd, DNAGLInterface.lpd                                | Environment-specific credentials, token caching, error handling             |
| JSON Input Processing  | DepartmentTransactionApproval.lpd                                            | JSONPARSER activity, field extraction, validation                           |
| Multi-Level Approval   | All approval patterns                                                        | Dynamic levels, escalation, reason codes, audit trails                      |
| Reason Code Logic      | DepartmentTransactionApproval.lpd, CashLedgerPaymentApproval.lpd            | Conditional requirements, separate user actions, audit compliance           |
| File Processing        | CheckReconCLInterface.lpd, GeoSyntec_INT_VirtualCard_GLInterface.lpd        | Monitor → Process → Archive/Error pattern, delimiter handling               |
| Concurrency Control    | EDIDataExchange_Outbound_Single.lpd                                          | CheckForConcurrentWorkUnits sub-process, single instance design             |
| Terms Modification     | CMContNegFinalAppr.lpd                                                       | DerivedPFFinalApproverTermsModified flag, dual path routing                 |

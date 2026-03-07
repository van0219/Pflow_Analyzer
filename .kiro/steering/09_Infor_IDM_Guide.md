---
inclusion: auto
name: idm-guide
description: Infor Document Management (IDM), BOD integration, ContentDocument, CaptureDocument, document upload/retrieval, IDM API, IDM nodes. Use when working with IDM integration or document management.
---

# Infor Document Management (IDM) Guide

## Quick Reference for AI

**When to Use This Guide**: User mentions IDM, document management, ContentDocument/CaptureDocument BODs, document upload/retrieval, or IDM integration.

**Critical Information**:

- **IDM Class**: `com.lawson.bpm.processflow.workFlow.flowGraph.FgaIDM`
- **OAuth Format**: `tenantId#serviceAccountKey` (note the `#` separator)
- **API Base**: `/IDM/api/v1/documents`
- **First Check**: Always check ION Connect for BOD errors before deeper troubleshooting

**Integration Method Selection**:

- **ION API (REST)**: New integrations, high throughput, modern architecture (RECOMMENDED)
- **ION BOD Messaging**: Event-driven workflows, guaranteed delivery, ERP integration
- **Direct API**: Back-end services, batch processing, custom applications
- **IPA IDM Node**: Document operations within IPA processes

**BOD Direction Quick Reference**:

- `ProcessContentDocument`: ERP → IDM (create/update documents)
- `SyncContentDocument`: IDM → ERP (document status/metadata updates)
- `CaptureDocument`: IDM → ERP (scanned/imported documents)

**Common Operations**:

1. **Upload Document**: IDM node in IPA or `POST /IDM/api/v1/documents` with multipart/form-data
2. **Retrieve Document**: `POST /IDM/api/v1/documents/search` then download from returned URL
3. **BOD Integration**: Configure connection points with correct document directions
4. **Troubleshooting**: ION Connect → Error BODs → Check OAuth credentials → Verify metadata

## Table of Contents

- [Quick Reference for AI](#quick-reference-for-ai)
- [Overview](#overview)
- [IDM Architecture](#idm-architecture)
- [Deployment Models](#deployment-models)
- [Integration Methods](#integration-methods)
- [BOD Integration Patterns](#bod-integration-patterns)
- [API Integration](#api-integration)
- [IPA IDM Activity Node](#ipa-idm-activity-node)
- [Configuration and Setup](#configuration-and-setup)
- [Document Types and Security](#document-types-and-security)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Integration Checklist](#integration-checklist)

---

## Overview

**Infor Document Management (IDM)** is a cloud-based document repository integrated with Infor OS that provides lifecycle management including archiving, security, collaboration, and versioning.

### Key Capabilities

- **Central Repository**: Common business rules and storage for all document types
- **Document Types**: Invoices, POs, employee records, specifications, contracts, and more
- **Lifecycle Management**: Automated archiving, security controls, collaboration tools, version control
- **In-Context Access**: Seamless document access within ERP applications (FSM, M3, LN)
- **Security**: Role-based permissions, security groups, and governance controls
- **Integration**: Native ION BOD messaging and REST API integration

### Supported Document Types

| Category | Document Types |
|----------|----------------|
| **Financial** | Purchase Orders, Requisitions, Invoices, Payment Documents |
| **HR** | Employee Records, Contracts, Performance Reviews |
| **Operations** | Product Specifications, Certificates, Quality Documents |
| **Legal** | Terms & Conditions, Contracts, Compliance Documents |
| **Procurement** | RFQ Documents, Supplier Documents |
| **Scanned** | Scanned Documents, Images, OCR-processed files |

**AI Note**: When user mentions a document type, verify it's supported and identify the appropriate category for security group configuration.

## IDM Architecture

### Core Components

| Component | Purpose | AI Implementation Notes |
|-----------|---------|-------------------------|
| **IDM Server** | Document storage and retrieval engine | Backend service - not directly accessible |
| **IDM Client** | Web-based interface for document management | User-facing UI - reference for user guidance |
| **IDM Connector** | Integration layer with ERP applications | Handles BOD messaging and API calls |
| **Control Center** | Administrative interface for configuration | Document type and security setup |
| **ION Integration** | Business Object Document (BOD) messaging | Primary integration mechanism for ERP |

### Integration Architecture

```text
┌─────────────────────────────────────┐
│  ERP Application (FSM/M3/LN)       │
│  - Generate documents               │
│  - Request document retrieval       │
└──────────────┬──────────────────────┘
               │ BODs/API Calls
               ↓
┌─────────────────────────────────────┐
│  ION Messaging Platform             │
│  - Connection Points                │
│  - BOD Routing                      │
│  - Error Handling                   │
└──────────────┬──────────────────────┘
               │ ContentDocument/CaptureDocument BODs
               ↓
┌─────────────────────────────────────┐
│  IDM Document Repository            │
│  - Document Storage                 │
│  - Metadata Management              │
│  - Security & Access Control        │
└──────────────┬──────────────────────┘
               │ Storage/Retrieval
               ↓
┌─────────────────────────────────────┐
│  Document Storage Backend           │
│  - Physical file storage            │
│  - Version management               │
└─────────────────────────────────────┘
```

### Data Flow Patterns

| Pattern | Flow | Use Case | AI Implementation Notes |
|---------|------|----------|-------------------------|
| **Document Creation** | ERP → ProcessContentDocument BOD → IDM | Automatic document storage from ERP processes | Most common pattern for IPA integrations |
| **Document Updates** | IDM → SyncContentDocument BOD → ERP | Document status/metadata synchronization | Configure connection point for bidirectional sync |
| **Document Capture** | Scanner/Import → CaptureDocument BOD → IDM → ERP | Scanned invoices, imported documents | Requires Ephesoft Smart Capture configuration |
| **Document Retrieval** | ERP → IDM API → Document Content | On-demand document access | Use REST API for better performance |

**AI Note**: When implementing document workflows, identify which pattern applies and configure the appropriate BOD direction in connection points.

## Deployment Models

### Cloud Multi-Tenant (Most Common)

**Characteristics**:

- Automatic provisioning as part of Infor OS subscription
- No separate installation required
- Access via Infor OS Portal and Ming.le
- Pre-configured for CloudSuite applications
- Managed by Infor Cloud Operations

**AI Implementation Notes**: For cloud tenants, focus on configuration rather than installation. IDM is already available - verify access and configure document types.

### On-Premises/Single-Tenant

**Characteristics**:

- Windows Server with IIS required
- SQL Server or Oracle backend database
- Infor Grid infrastructure required
- Manual IDM Server installation
- Customer-managed maintenance

**AI Implementation Notes**: Rare in modern implementations. If user mentions on-premises, verify deployment model before providing guidance.

### Hybrid Deployment

**Characteristics**:

- IDM Cloud: Document storage in Infor Cloud
- ERP On-Premises: Local ERP with cloud IDM integration
- ION Gateway: Secure communication bridge

**AI Implementation Notes**: Common for customers migrating to cloud. Focus on ION Gateway configuration and network connectivity.

## Integration Methods

### Decision Matrix

Choose integration method based on use case:

| Method | Use When | Pros | Cons | AI Recommendation |
|--------|----------|------|------|-------------------|
| **ION API (REST)** | New integrations, high throughput | Modern, scalable, easy monitoring | Requires OAuth2 setup | **RECOMMENDED** for new work |
| **ION BOD Messaging** | Event-driven workflows, ERP integration | Guaranteed delivery, retry logic | More complex setup | Use for ERP-triggered workflows |
| **Direct API** | Back-end services, batch processing | Direct access, no ION dependency | Less monitoring, manual retry | Use for custom applications |
| **Context Business Messages** | In-app document access | Seamless UX, deep ERP integration | Limited to supported ERPs | Use for user-facing features |

### 1. ION API (REST) - Recommended

**When to Use**: New integrations, IPA processes, custom applications

**Key Characteristics**:

- **Authentication**: OAuth2 with Infor OS (service account format: `tenantId#serviceAccountKey`)
- **Endpoint**: Via Infor Ming.le API Gateway (`https://{tenant}.inforcloudsuite.com/IDM/api/v1/`)
- **Format**: RESTful API calls with JSON payloads
- **Security**: Token-based authentication with refresh tokens
- **Performance**: High throughput, horizontally scalable

**AI Implementation Pattern**:

```javascript
// Step 1: Authenticate (get OAuth token)
// Step 2: Call IDM API endpoint with Bearer token
// Step 3: Handle response and errors
// Step 4: Refresh token if expired (401 response)
```

### 2. ION BOD Messaging

**When to Use**: ERP-triggered document workflows, guaranteed delivery requirements

**Key Characteristics**:

- **Protocol**: Business Object Documents (XML-based)
- **Transport**: ION messaging infrastructure
- **Reliability**: Guaranteed delivery with automatic retry logic
- **Monitoring**: ION Connect monitoring and error handling

**AI Implementation Pattern**:

```text
1. Configure connection point with correct BOD directions
2. ERP generates BOD (ProcessContentDocument/SyncContentDocument)
3. ION routes BOD to IDM
4. Monitor in ION Connect for errors
```

### 3. Direct API Integration

**When to Use**: Back-end services without ION, batch processing

**Key Characteristics**:

- **Authentication**: OAuth1 or OAuth2 (direct to IDM)
- **Use Case**: Service-to-service integration
- **Impersonation**: User context for document creation
- **Configuration**: Consumer key/secret authentication

**AI Implementation Notes**: Less common. Prefer ION API for better monitoring and error handling.

### 4. Context Business Messages

**When to Use**: In-app document access within ERP forms

**Key Characteristics**:

- **Integration**: Deep ERP integration (FSM, M3, LN)
- **Context**: Document access within ERP forms and screens
- **UI**: Related Information context apps
- **Experience**: Seamless user experience without leaving ERP

**AI Implementation Notes**: Configuration-based, not code-based. Guide user to ERP-specific documentation.

## BOD Integration Patterns

### ContentDocument BOD (Bidirectional)

**Purpose**: Primary document management BOD for create/update operations

#### Outbound (ERP → IDM): ProcessContentDocument

**Direction**: `Receive` (from IDM perspective)

**Usage**:

- Automatic document creation from ERP processes
- Report generation and storage
- Document creation workflows

**Trigger Examples**:

- Invoice report generated in FSM
- Purchase order PDF created
- Employee document uploaded

**AI Implementation Notes**: Most common pattern for IPA integrations. Configure connection point with `Process.ContentDocument` direction `Receive`.

#### Inbound (IDM → ERP): SyncContentDocument

**Direction**: `Send` (from IDM perspective)

**Usage**:

- Document status updates to ERP
- Metadata synchronization
- Version update notifications

**Trigger Examples**:

- Document approved in IDM
- Document version updated
- Metadata changed by user

**AI Implementation Notes**: Required for bidirectional sync. Configure connection point with `Sync.ContentDocument` direction `Send`.

### CaptureDocument BOD (Outbound from IDM)

**Purpose**: Document capture and scanning integration

**Direction**: `Send` (from IDM perspective)

**Flow**: Scanner/Import → IDM → CaptureDocument BOD → ERP

**Usage**:

- Scanned invoices (AP automation)
- Imported documents from external sources
- OCR-processed documents

**Integration**: Uses Ephesoft Smart Capture technology for OCR/ICR processing

**AI Implementation Notes**: Configure connection point with `Sync.CaptureDocument` direction `Send`. Requires Ephesoft configuration for OCR.

### BOD Configuration Example

```xml
<!-- IDM Connection Point Configuration -->
<ConnectionPoint name="IDM" description="Infor Document Management">
    <Documents>
        <!-- Receive documents from ERP for storage -->
        <Document name="Process.ContentDocument" direction="Receive" />
        
        <!-- Send document updates back to ERP -->
        <Document name="Sync.ContentDocument" direction="Send" />
        
        <!-- Send captured/scanned documents to ERP -->
        <Document name="Sync.CaptureDocument" direction="Send" />
    </Documents>
</ConnectionPoint>
```

**AI Implementation Checklist**:

- [ ] Verify connection point name matches IDM configuration
- [ ] Set correct direction for each BOD type (Send vs Receive)
- [ ] Test BOD flow in ION Connect
- [ ] Monitor for errors in ION Connect > Error BODs

## API Integration

### OAuth2 Authentication Pattern

**Service Account Format**: `tenantId#serviceAccountKey` (note the `#` separator - this is critical)

**Authentication Flow**:

1. Request access token from OAuth2 endpoint
2. Use Bearer token in API requests
3. Refresh token when expired (401 response)
4. Handle token expiration gracefully

**ES5-Compatible Authentication Code**:

```javascript
// OAuth2 Token Request (ES5 Compatible for IPA)
var tenantId = "TENANT_tenant";
var serviceAccountKey = "serviceAccountName";
var serviceAccountSecret = "serviceAccountPassword";
var clientId = "clientIdFromION";
var clientSecret = "clientSecretFromION";

// CRITICAL: Username format is tenantId#serviceAccountKey
var username = tenantId + "#" + serviceAccountKey;

// Build token request body
var tokenRequest = "grant_type=password" +
                  "&username=" + encodeURIComponent(username) +
                  "&password=" + encodeURIComponent(serviceAccountSecret) +
                  "&client_id=" + clientId +
                  "&client_secret=" + clientSecret;

// Token endpoint URL
var tokenUrl = "https://{tenant}.inforcloudsuite.com/" + tenantId + "/as/token.oauth2";

// POST request to get token
// Response: { "access_token": "...", "token_type": "Bearer", "expires_in": 3600 }
```

**AI Implementation Notes**:

- Always use `tenantId#serviceAccountKey` format (not `tenantId/serviceAccountKey` or other separators)
- Store tokens securely (never hardcode in LPD files)
- Implement token refresh logic (tokens expire after 1 hour typically)
- Handle 401 responses by refreshing token and retrying

### Document Upload API Pattern

**Endpoint**: `POST /IDM/api/v1/documents`

**Content-Type**: `multipart/form-data`

**Required Parts**:

1. `metadata` - JSON string with document properties
2. `file` - Binary file content
3. `fileName` - Original file name

**ES5-Compatible Upload Code**:

```javascript
// Document Upload to IDM (ES5 Compatible for IPA)
var invoiceNumber = "INV-12345";
var supplierCode = "SUP-001";
var supplierName = "Acme Corporation";
var invoiceAmount = "1500.00";

// Document metadata (will be stringified to JSON)
var documentMetadata = {
    documentType: "Invoice",
    title: "Invoice_" + invoiceNumber,
    description: "Supplier Invoice for " + supplierName,
    keywords: ["invoice", "supplier", "accounts_payable"],
    customAttributes: {
        InvoiceNumber: invoiceNumber,
        SupplierCode: supplierCode,
        Amount: invoiceAmount,
        SupplierName: supplierName
    }
};

// API endpoint
var uploadUrl = "https://{tenant}.inforcloudsuite.com/IDM/api/v1/documents";

// Headers
// Authorization: Bearer {access_token}
// Content-Type: multipart/form-data

// Form data parts:
// - metadata: JSON.stringify(documentMetadata)
// - file: <binary file content>
// - fileName: "Invoice_INV-12345.pdf"
```

**AI Implementation Checklist**:

- [ ] Validate document type exists in IDM
- [ ] Include all required custom attributes
- [ ] Use descriptive title and keywords for searchability
- [ ] Handle file encoding correctly (binary, not base64)
- [ ] Check response for documentId (needed for retrieval)

### Document Retrieval API Pattern

**Endpoint**: `POST /IDM/api/v1/documents/search`

**Content-Type**: `application/json`

**Response**: Document metadata + temporary download URLs

**ES5-Compatible Retrieval Code**:

```javascript
// Document Search and Retrieval (ES5 Compatible for IPA)
var invoiceNumber = "INV-12345";
var startDate = "2026-01-01T00:00:00Z";
var endDate = "2026-12-31T23:59:59Z";

// Search criteria
var searchCriteria = {
    documentType: "Invoice",
    customAttributes: {
        InvoiceNumber: invoiceNumber
    },
    dateRange: {
        from: startDate,
        to: endDate
    },
    maxResults: 10
};

// API endpoint
var searchUrl = "https://{tenant}.inforcloudsuite.com/IDM/api/v1/documents/search";

// Headers
// Authorization: Bearer {access_token}
// Content-Type: application/json

// Request body: JSON.stringify(searchCriteria)

// Response structure:
// {
//   "documents": [
//     {
//       "documentId": "doc-12345",
//       "downloadUrl": "https://...signed-url...",
//       "title": "Invoice_INV-12345",
//       "documentType": "Invoice",
//       "createdDate": "2026-02-08T10:30:00Z",
//       "version": "1.0",
//       "customAttributes": { ... }
//     }
//   ],
//   "totalResults": 1
// }
```

**AI Implementation Notes**:

- Download URL is temporary (expires after 15-30 minutes typically)
- Use documentId for subsequent operations (update, delete)
- Search by custom attributes for precise results
- Implement pagination for large result sets (maxResults parameter)

## IPA IDM Activity Node

### IDM Node Overview

**Activity Type**: IDM

**Class Name**: `com.lawson.bpm.processflow.workFlow.flowGraph.FgaIDM`

**Purpose**: Integrate IPA processes with Infor Document Management for document operations

**When to Use**: Document upload/download/search within IPA workflows

### Supported IDM Operations

| Operation | Purpose | Required Properties | AI Implementation Notes |
|-----------|---------|---------------------|-------------------------|
| `UPLOAD` | Upload document to IDM | documentType, filePath, metadata | Most common operation in IPA |
| `DOWNLOAD` | Download document from IDM | documentId, targetPath | Use after search to retrieve file |
| `SEARCH` | Search for documents | searchCriteria | Returns documentId for download |
| `UPDATE` | Update document metadata | documentId, metadata | Modify existing document properties |
| `DELETE` | Delete document | documentId | Use with caution - permanent deletion |

### IPA IDM Node Configuration Example

```xml
<!-- Upload Document to IDM -->
<activity activityType="IDM" caption="UploadInvoiceToIDM" 
         className="com.lawson.bpm.processflow.workFlow.flowGraph.FgaIDM">
    
    <!-- Operation type: UPLOAD, DOWNLOAD, SEARCH, UPDATE, DELETE -->
    <prop name="operation" propType="SIMPLE">
        <anyData><![CDATA[UPLOAD]]></anyData>
    </prop>
    
    <!-- Document type (must exist in IDM) -->
    <prop name="documentType" propType="SIMPLE">
        <anyData><![CDATA[Invoice]]></anyData>
    </prop>
    
    <!-- Local file path (absolute path recommended) -->
    <prop name="filePath" propType="SIMPLE">
        <anyData><![CDATA[<!LocalFilePath>]]></anyData>
    </prop>
    
    <!-- Document metadata (JSON string) -->
    <prop name="metadata" propType="SIMPLE">
        <anyData><![CDATA[<!DocumentMetadata>]]></anyData>
    </prop>
    
    <!-- Optional: Document title -->
    <prop name="title" propType="SIMPLE">
        <anyData><![CDATA[Invoice_<!InvoiceNumber>]]></anyData>
    </prop>
    
    <!-- Optional: Document description -->
    <prop name="description" propType="SIMPLE">
        <anyData><![CDATA[Supplier Invoice for <!SupplierName>]]></anyData>
    </prop>
</activity>
```

### IDM Node Best Practices

**Error Handling**:

- Always include error connectors for IDM operations
- Capture error messages in process variables
- Implement retry logic for transient failures (network issues)
- Log errors for troubleshooting

**Metadata Validation**:

- Validate document metadata before upload
- Ensure required custom attributes are present
- Check document type exists in IDM
- Validate data types (numbers, dates, strings)

**File Path Handling**:

- Use absolute paths for document operations
- Verify file exists before upload
- Check file permissions
- Clean up temporary files after upload

**Authentication**:

- Configure IDM connection with proper OAuth credentials
- Use service account (not user account) for automated processes
- Store credentials securely (not in LPD file)
- Handle token expiration gracefully

**Performance**:

- Batch document operations when possible
- Use asynchronous patterns for large documents
- Implement timeout handling
- Monitor IDM node execution time

### Common IPA IDM Patterns

#### Pattern 1: Upload Generated Report

```text
1. Generate Report (PDF/Excel)
2. Save to temporary location
3. IDM Node: UPLOAD operation
4. Capture documentId in process variable
5. Clean up temporary file
6. Error handling: Retry on failure
```

#### Pattern 2: Search and Download Document

```text
1. IDM Node: SEARCH operation with criteria
2. Parse search results for documentId
3. IDM Node: DOWNLOAD operation with documentId
4. Process downloaded document
5. Error handling: Document not found
```

#### Pattern 3: Update Document Metadata

```text
1. IDM Node: SEARCH to find document
2. Prepare updated metadata JSON
3. IDM Node: UPDATE operation
4. Verify update success
5. Error handling: Document locked or not found
```

**AI Implementation Notes**:

- Always validate inputs before IDM operations
- Use descriptive captions for IDM nodes (e.g., "UploadInvoiceToIDM" not "IDM1")
- Implement comprehensive error handling
- Log all IDM operations for audit trail
- Test with actual IDM connection (not mock data)

## Configuration and Setup

### CloudSuite IDM Configuration (2021.03+)

**Modern Tenants** (most common):

- **Auto-Provisioning**: IDM integration ready out-of-the-box
- **User GUID**: Configure in File Server Setup (required for document access)
- **Connection**: Automatic ION connectivity (no manual setup)
- **Document Types**: Pre-configured for common business documents

**AI Implementation Steps**:

1. Verify IDM is provisioned (check Infor OS Portal)
2. Configure User GUID in File Server Setup
3. Test document upload/retrieval
4. Configure custom document types if needed

### Legacy Tenant Configuration (Pre-2021.03)

**Older Tenants** (less common):

- **Manual Setup**: IDM configuration required
- **ION Connection**: Manual connection point setup
- **Document Types**: Manual document type configuration
- **User Mapping**: Manual user GUID configuration

**AI Implementation Steps**:

1. Create IDM connection point in ION
2. Configure BOD directions (Send/Receive)
3. Set up document types in IDM Control Center
4. Configure user GUID mapping
5. Test BOD flow in ION Connect

### ERP Integration Setup

**Required Configuration Steps**:

1. **Event Handlers**: Verify TaskPostPerform event handler is active (for automatic document creation)
2. **Document Types**: Configure shared groups for document types (security)
3. **User Permissions**: Assign appropriate groups to users (access control)
4. **Output Media**: Configure PDF generation and IDM storage (report integration)
5. **Connection Points**: Set up ION connection points for BOD messaging (integration)

**AI Implementation Checklist**:

- [ ] Event handler active and configured
- [ ] Document types created with security groups
- [ ] Users assigned to appropriate groups
- [ ] Output media configured for reports
- [ ] Connection points configured with correct BOD directions
- [ ] Test document creation from ERP

### IDM Control Center Configuration

**Administrative Tasks**:

| Task | Purpose | AI Implementation Notes |
|------|---------|-------------------------|
| **Document Types** | Define business document categories | Create before integration testing |
| **Security Groups** | Configure access permissions | Map to ERP user roles |
| **Workflow Rules** | Set up approval and routing rules | Optional - for advanced workflows |
| **Import/Export** | Configuration backup and migration | Use for environment promotion |
| **User Management** | Role-based access control | Sync with ERP user permissions |

**AI Implementation Notes**: Guide user to IDM Control Center for administrative tasks. Most configuration is UI-based, not code-based.

## Document Types and Security

### Standard Document Types

| Category | Document Types | Typical Security Groups | AI Implementation Notes |
|----------|----------------|-------------------------|-------------------------|
| **Financial** | Invoices, Purchase Orders, Payment Vouchers | AccountsPayable, Finance, Auditors | Most common - configure first |
| **HR** | Employee Records, Contracts, Performance Reviews | HumanResources, Management, Employees | Sensitive - strict access control |
| **Operations** | Specifications, Certificates, Quality Documents | Operations, QualityControl, Engineering | Technical documents |
| **Legal** | Terms & Conditions, Contracts, Compliance Documents | Legal, Compliance, Management | Highly restricted access |

### Security Configuration Example

```xml
<!-- Document Type Security Configuration -->
<DocumentType name="Invoice">
    <SharedGroups>
        <!-- Read/Write access for AP team -->
        <Group name="AccountsPayable" permissions="ReadWrite" />
        
        <!-- Read-only access for finance team -->
        <Group name="Finance" permissions="Read" />
        
        <!-- Read-only access for auditors -->
        <Group name="Auditors" permissions="Read" />
    </SharedGroups>
    
    <Attributes>
        <!-- Required attributes for Invoice document type -->
        <Attribute name="InvoiceNumber" required="true" type="String" />
        <Attribute name="SupplierCode" required="true" type="String" />
        <Attribute name="Amount" required="true" type="Decimal" />
        <Attribute name="InvoiceDate" required="true" type="Date" />
        <Attribute name="DueDate" required="false" type="Date" />
        <Attribute name="PONumber" required="false" type="String" />
    </Attributes>
</DocumentType>
```

### Access Control Patterns

| Pattern | Use Case | Implementation | AI Implementation Notes |
|---------|----------|----------------|-------------------------|
| **Role-Based** | Permissions based on user roles | Map IDM groups to ERP roles | Most common pattern |
| **Group-Based** | Document type access by security groups | Configure shared groups per document type | Standard approach |
| **Attribute-Based** | Fine-grained control using document attributes | Use custom attributes for filtering | Advanced scenarios |
| **Context-Based** | Access control based on business context | Combine with ERP context | Complex workflows |

**AI Implementation Notes**:

- Always configure security groups before document types
- Map IDM groups to existing ERP user roles
- Test access control with different user accounts
- Document security model for audit purposes

## Troubleshooting

### Troubleshooting Decision Tree

```text
Document not appearing in IDM?
├─ Using BOD integration?
│  ├─ Step 1: Check ION Connect > Error BODs
│  │  └─ BOD errors found? → Fix BOD configuration
│  ├─ Step 2: Verify connection point configuration
│  │  └─ Check BOD direction (Send vs Receive)
│  └─ Step 3: Check document type exists in IDM
│     └─ Create document type if missing
└─ Using API integration?
   ├─ Step 1: Check OAuth token validity
   │  └─ Test token with simple API call
   ├─ Step 2: Verify API endpoint URL
   │  └─ Confirm tenant URL and API path
   └─ Step 3: Check document metadata requirements
      └─ Validate required attributes present
```

### Common Integration Issues

#### Issue 1: BOD Flow Problems

**Symptom**: CaptureDocument BOD found in ION, but document not visible in ERP

**Root Causes**:

1. IDM not configured to publish BODs
2. Sync.CaptureDocument BOD not added to connection point
3. ION connection point direction incorrect (Send vs Receive)
4. Document type mapping missing in ERP

**Resolution Steps**:

1. Verify IDM BOD publishing configuration in Control Center
2. Check connection point document configuration (must include Sync.CaptureDocument with direction "Send")
3. Review ION error logs in Connect > Error BODs
4. Verify document type exists in both IDM and ERP
5. Test BOD flow with sample document

**AI Implementation Notes**: Always check ION Connect first - most BOD issues show up as error BODs with detailed error messages.

#### Issue 2: Authentication Failures

**Symptom**: HTTP 401/403 errors during API calls

**Root Causes**:

1. Invalid OAuth credentials (client ID, secret, service account)
2. Expired tokens (not refreshing properly)
3. Incorrect user GUID configuration in File Server Setup
4. Service account format incorrect (missing `#` separator)

**Resolution Steps**:

1. Verify OAuth configuration (client ID, secret, tenant)
2. Check token expiration and refresh logic (tokens expire after ~1 hour)
3. Validate user GUID in File Server Setup
4. Confirm service account format: `tenantId#serviceAccountKey`
5. Test authentication with Postman or similar tool

**AI Implementation Notes**: Service account format is critical - `tenantId#serviceAccountKey` (not `/` or other separators).

#### Issue 3: Document Upload Failures

**Symptom**: Documents not appearing in IDM after upload, or API returns error

**Root Causes**:

1. Invalid document type configuration (document type doesn't exist)
2. Missing required metadata attributes
3. File path or permission issues (file not accessible)
4. File size exceeds limits (typically 100MB max)
5. Invalid file format for document type

**Resolution Steps**:

1. Verify document type exists and is active in IDM Control Center
2. Check required attribute configuration (all required fields present)
3. Validate file permissions and paths (use absolute paths)
4. Check file size (compress if needed)
5. Verify file format is supported (PDF, DOCX, XLSX, etc.)

**AI Implementation Notes**: Validate document type and required attributes before attempting upload - saves troubleshooting time.

#### Issue 4: Document Not Found in Search

**Symptom**: Search returns no results, but document exists in IDM

**Root Causes**:

1. Search criteria too restrictive (no matches)
2. Custom attribute values don't match (case sensitivity, formatting)
3. Document not indexed yet (recent upload)
4. User doesn't have permission to view document
5. Date range excludes document creation date

**Resolution Steps**:

1. Simplify search criteria (remove optional filters)
2. Check custom attribute values (exact match required)
3. Wait for indexing (typically 1-5 minutes after upload)
4. Verify user has access to document type (security groups)
5. Expand date range or remove date filter

**AI Implementation Notes**: Start with broad search criteria, then narrow down. Custom attributes are case-sensitive.

### Diagnostic Steps

**Standard Troubleshooting Workflow**:

1. **ION Monitoring**: Check ION Connect > Error BODs for BOD-related issues
2. **IDM Logs**: Review IDM server logs for errors (if accessible)
3. **API Testing**: Test API endpoints with Postman or curl (validate credentials)
4. **Configuration Validation**: Verify all configuration settings (connection points, document types)
5. **Network Connectivity**: Check firewall and network access (especially for hybrid deployments)

**AI Implementation Checklist**:

- [ ] Check ION Connect for error BODs
- [ ] Verify OAuth token is valid (test with simple API call)
- [ ] Confirm document type exists in IDM
- [ ] Validate required metadata attributes
- [ ] Check user permissions and security groups
- [ ] Review file path and permissions
- [ ] Test with sample document first

### Error Code Reference

| Error Code | Meaning | Resolution | AI Implementation Notes |
|------------|---------|------------|-------------------------|
| **401** | Unauthorized - invalid or expired token | Refresh OAuth token | Implement token refresh logic |
| **403** | Forbidden - insufficient permissions | Check user security groups | Verify user has access to document type |
| **404** | Not Found - document or endpoint doesn't exist | Verify document ID and API endpoint | Check for typos in URL |
| **413** | Payload Too Large - file size exceeds limit | Compress file or split into parts | Typical limit is 100MB |
| **422** | Unprocessable Entity - invalid metadata | Validate required attributes | Check attribute data types |
| **500** | Internal Server Error - IDM service issue | Check IDM service status, retry | Contact Infor support if persistent |

**AI Implementation Notes**: Log all error responses with full details for troubleshooting. Error messages often contain specific guidance.

## Best Practices

### Document Management Strategy

**Naming Conventions**:

- Use consistent patterns: `{DocumentType}_{Identifier}_{Date}.{ext}`
- Example: `Invoice_INV-12345_20260208.pdf`
- Include key identifiers in filename for easy recognition
- Avoid special characters (use underscore, not spaces)

**Metadata Standards**:

- Define required vs optional attributes per document type
- Use consistent data types (String, Decimal, Date, Boolean)
- Include searchable keywords for document discovery
- Document metadata schema for developers

**Version Control**:

- Enable versioning for critical document types
- Use semantic versioning (1.0, 1.1, 2.0) for major changes
- Document version history and change reasons
- Implement approval workflows for version updates

**Retention Policies**:

- Define retention periods per document type (e.g., 7 years for invoices)
- Implement automated archiving and cleanup
- Comply with regulatory requirements (SOX, GDPR, etc.)
- Test retention policies in non-production first

**Security Governance**:

- Regular access reviews (quarterly recommended)
- Principle of least privilege (minimum required access)
- Audit trail for sensitive documents
- Document security model and exceptions

### Integration Best Practices

**Error Handling**:

- Implement comprehensive error handling for all IDM operations
- Use retry logic for transient failures (network issues, timeouts)
- Log all errors with context (document ID, operation, timestamp)
- Alert on persistent failures (3+ consecutive failures)
- Implement circuit breaker pattern for API calls

**Performance**:

- Batch operations for bulk document processing (upload multiple documents)
- Use asynchronous patterns for large documents (>10MB)
- Implement caching for frequently accessed documents
- Monitor API rate limits and throttle requests
- Optimize search queries (use indexed attributes)

**Monitoring**:

- Proactive monitoring of integration health (uptime, response time)
- Set up alerts for failures (BOD errors, API errors)
- Track key metrics (documents uploaded, search latency, error rate)
- Regular review of ION Connect error logs
- Dashboard for integration status

**Testing**:

- Thorough testing of document workflows (upload, search, download)
- Test with various file types and sizes
- Test error scenarios (invalid metadata, missing files)
- Load testing for high-volume scenarios
- Test in non-production environment first

**Documentation**:

- Maintain integration documentation (architecture, configuration)
- Document custom attributes and their purpose
- API endpoint reference with examples
- Troubleshooting guide for common issues
- Runbook for support team

### IPA Integration Patterns

**Async Processing**:

- Use asynchronous patterns for large documents (avoid blocking)
- Implement callback mechanisms for completion notification
- Queue document operations for batch processing
- Monitor queue depth and processing time

**Batch Operations**:

- Group multiple document operations (upload 10-50 documents at once)
- Use parallel processing where possible
- Implement checkpointing for restart capability
- Monitor batch success rate

**Error Recovery**:

- Implement robust error recovery mechanisms (retry, fallback)
- Store failed operations for manual review
- Implement dead letter queue for persistent failures
- Alert on error recovery failures

**Logging**:

- Comprehensive logging for troubleshooting (all operations)
- Include context: document ID, operation, user, timestamp
- Log performance metrics (execution time, file size)
- Implement log rotation and retention
- Use structured logging (JSON format)

**Configuration**:

- Environment-specific configuration management (dev, test, prod)
- Externalize credentials (not in LPD files)
- Use configuration variables for endpoints and settings
- Document configuration requirements
- Version control configuration files

### Security Best Practices

**Least Privilege**:

- Grant minimum required permissions (read vs read/write)
- Use service accounts for automated processes (not user accounts)
- Regular review of permissions (quarterly)
- Remove unused accounts and permissions

**Regular Reviews**:

- Periodic access reviews (quarterly recommended)
- Review security group memberships
- Audit document access logs
- Review and update security policies

**Audit Trails**:

- Comprehensive audit logging (who, what, when)
- Log all document operations (create, read, update, delete)
- Retain audit logs per compliance requirements
- Regular review of audit logs for anomalies

**Encryption**:

- Document encryption at rest (IDM handles this)
- Encryption in transit (HTTPS/TLS for API calls)
- Secure credential storage (encrypted, not plaintext)
- Key rotation per security policy

**Compliance**:

- Adherence to regulatory requirements (SOX, GDPR, HIPAA)
- Document retention policies per regulations
- Data privacy controls (PII handling)
- Regular compliance audits

### Performance Optimization

**Caching**:

- Cache frequently accessed documents (reduce API calls)
- Implement cache invalidation strategy (time-based, event-based)
- Use CDN for global document access
- Monitor cache hit rate

**Compression**:

- Use document compression for storage efficiency (PDF compression)
- Compress large files before upload (ZIP for multiple files)
- Balance compression ratio vs processing time
- Test compressed file compatibility

**CDN**:

- Content delivery networks for global access (reduce latency)
- Cache documents at edge locations
- Implement cache warming for critical documents
- Monitor CDN performance

**Indexing**:

- Proper indexing for fast search and retrieval (custom attributes)
- Index frequently searched attributes
- Avoid over-indexing (impacts write performance)
- Monitor index performance

**Cleanup**:

- Regular cleanup of obsolete documents (per retention policy)
- Archive old documents (move to cold storage)
- Delete temporary files after processing
- Monitor storage usage and growth

**AI Implementation Notes**:

- Always implement error handling and logging first
- Test in non-production before deploying to production
- Monitor integration health proactively
- Document all custom configurations
- Follow security best practices (least privilege, encryption)

## Integration Checklist

### Pre-Implementation

**Planning Phase**:

- [ ] Verify IDM provisioning and access (check Infor OS Portal)
- [ ] Identify document types needed (invoices, POs, etc.)
- [ ] Define metadata schema (required vs optional attributes)
- [ ] Plan document naming and metadata strategy (consistent patterns)
- [ ] Identify security groups and access requirements (who needs access)
- [ ] Review compliance and retention requirements (regulatory)

**Configuration Phase**:

- [ ] Configure ION connection points (if using BOD integration)
- [ ] Set up document types in IDM Control Center (with required attributes)
- [ ] Configure security groups and permissions (role-based access)
- [ ] Test authentication and API connectivity (OAuth2 token flow)
- [ ] Create test documents for validation (sample files)

**AI Implementation Notes**: Complete planning phase before configuration - changes are harder after implementation.

### Implementation

**Development Phase**:

- [ ] Configure ERP integration settings (event handlers, output media)
- [ ] Set up BOD messaging flows (connection points, BOD directions)
- [ ] Implement error handling and retry logic (comprehensive)
- [ ] Configure user permissions and access (security groups)
- [ ] Implement logging and monitoring (all operations)

**Testing Phase**:

- [ ] Test document upload/retrieval workflows (happy path)
- [ ] Test error scenarios (invalid metadata, missing files)
- [ ] Test with different file types and sizes (PDF, DOCX, large files)
- [ ] Test security and access control (different user roles)
- [ ] Load testing for high-volume scenarios (if applicable)

**AI Implementation Notes**: Test thoroughly in non-production environment before deploying to production.

### Post-Implementation

**Deployment Phase**:

- [ ] Deploy to production environment (after successful testing)
- [ ] Monitor integration health and performance (first 24-48 hours critical)
- [ ] Verify document workflows in production (smoke test)
- [ ] Set up alerting for failures (BOD errors, API errors)
- [ ] Document deployment and configuration (runbook)

**Operations Phase**:

- [ ] Train users on document management workflows (upload, search, access)
- [ ] Establish maintenance and support procedures (troubleshooting guide)
- [ ] Plan for capacity and growth (storage, API rate limits)
- [ ] Schedule regular access reviews (quarterly recommended)
- [ ] Monitor and optimize performance (response time, error rate)

**AI Implementation Notes**: Monitor closely after deployment - most issues surface in first week of production use.

---

## AI Assistant Quick Reference

**Critical Information to Remember**:

- **IDM Class**: `com.lawson.bpm.processflow.workFlow.flowGraph.FgaIDM`
- **OAuth Format**: `tenantId#serviceAccountKey` (the `#` separator is critical)
- **API Base**: `/IDM/api/v1/documents`
- **First Troubleshooting Step**: Always check ION Connect for BOD errors

**Common Mistakes to Avoid**:

1. Wrong OAuth format (using `/` instead of `#` separator)
2. Incorrect BOD direction (Send vs Receive from IDM perspective)
3. Missing required metadata attributes (causes upload failures)
4. Not implementing token refresh logic (tokens expire after ~1 hour)
5. Using relative file paths instead of absolute paths in IPA

**When User Asks About**:

- **Document upload**: Guide to ION API (REST) or IPA IDM node
- **BOD integration**: Check connection point configuration and BOD directions
- **Authentication errors**: Verify OAuth format and token refresh logic
- **Document not found**: Check ION Connect first, then verify document type and metadata
- **Performance issues**: Suggest batching, async processing, and caching

**Best Practices to Recommend**:

1. Use ION API (REST) for new integrations (better than BOD for most cases)
2. Implement comprehensive error handling and retry logic
3. Use service accounts (not user accounts) for automated processes
4. Test in non-production environment first
5. Monitor ION Connect proactively for BOD errors

**Code Examples**:

- All JavaScript examples are ES5-compatible (for IPA)
- Use `var` (not `let` or `const`)
- No arrow functions (use `function` keyword)
- Include error handling in all examples
- Use descriptive variable names for clarity

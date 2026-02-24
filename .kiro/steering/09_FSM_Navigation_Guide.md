---
inclusion: auto
name: fsm-navigation
description: FSM UI navigation, Playwright browser automation, Process Server administration, IPA Designer, Service Definitions, triggers, scheduling. Use when navigating FSM interface or automating browser interactions.
---

# FSM Navigation & Browser Automation Guide

*Practical guide for FSM navigation, Playwright automation, and process management*

## Table of Contents

- [Critical Rules for AI](#critical-rules-for-ai)
  - [Rule 1: ALWAYS Expand Sidebar First](#rule-1-always-expand-sidebar-first)
  - [Rule 2: Use Browser Zoom, Not CSS Zoom](#rule-2-use-browser-zoom-not-css-zoom)
  - [Rule 3: Authentication by Environment](#rule-3-authentication-by-environment)
  - [Rule 4: Double-Click for Record Details](#rule-4-double-click-for-record-details)
  - [Rule 5: Use Search for Comprehensive Lists](#rule-5-use-search-for-comprehensive-lists)
- [Environment & Authentication](#environment--authentication)
  - [Environment Hierarchy](#environment-hierarchy)
  - [Credential Management](#credential-management)
- [Browser Automation Patterns](#browser-automation-patterns)
  - [Playwright MCP Integration](#playwright-mcp-integration)
  - [Standard Automation Sequence](#standard-automation-sequence)
  - [Click Handling Strategies](#click-handling-strategies)
  - [Element Selector Best Practices](#element-selector-best-practices)
  - [Interface Optimization](#interface-optimization)
- [FSM Navigation Patterns](#fsm-navigation-patterns)
  - [Search-Based Navigation (Recommended)](#search-based-navigation-recommended)
  - [Record Access Patterns](#record-access-patterns)
  - [Menu Navigation with Carets](#menu-navigation-with-carets)
- [Process Server Administrator Navigation](#process-server-administrator-navigation)
  - [Overview](#overview)
  - [Accessing Process Server Administrator](#accessing-process-server-administrator)
  - [Process Definitions Management](#process-definitions-management)
  - [Process Scheduling and Triggers](#process-scheduling-and-triggers)
  - [FSM Process Management Workflow](#fsm-process-management-workflow)
  - [Process Definition Filtering and Search](#process-definition-filtering-and-search)
  - [Common Process Management Tasks](#common-process-management-tasks)
  - [Integration with Work Unit Analysis](#integration-with-work-unit-analysis)
- [Invoice Approval Workflow Example](#invoice-approval-workflow-example)
  - [Workflow Overview](#workflow-overview)
  - [Key Components](#key-components)
  - [Automated Workflows](#automated-workflows)
  - [Key Principles](#key-principles)
  - [Navigation Tips](#navigation-tips)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)
- [Environment-Specific Data Quality](#environment-specific-data-quality)

## Critical Rules for AI

### Rule 1: ALWAYS Expand Sidebar First

**MOST IMPORTANT FSM NAVIGATION RULE**: Before ANY navigation, click hamburger icon (☰) to expand sidebar.

```javascript
// ALWAYS do this first
await page.click('button[aria-label="Toggle Navigation"]');
await page.waitForTimeout(500); // Wait for sidebar expansion
```

**Why Critical**:

- FSM starts with collapsed sidebar
- Most menu items hidden when collapsed
- Navigation fails without expanded sidebar
- Template upload, admin functions require sidebar

### Rule 2: Use Browser Zoom, Not CSS Zoom

**CORRECT** - Browser zoom via keyboard:

```javascript
await page.keyboard.press('Control+Minus'); // Repeat 3x for 70% zoom
```

**WRONG** - CSS zoom (creates layout issues):

```javascript
document.body.style.zoom = "0.7"; // DON'T USE THIS
```

### Rule 3: Authentication by Environment

| Environment | Auth Method | Notes |
|-------------|-------------|-------|
| TAMICS10_AX1 | Cloud Identities OR Windows | Flexible |
| ACUITY_TST | Cloud Identities ONLY | No Windows auth |
| ACUITY_PRD | Cloud Identities ONLY | No Windows auth |

**Credentials**: Use `Credentials/.env.fsm` and `Credentials/.env.passwords`

### Rule 4: Double-Click for Record Details

**Single-click**: Selects record in list
**Double-click**: Opens record detail view (REQUIRED for PO, invoices, etc.)

```javascript
await page.locator('a[href*="PurchaseOrder"]').dblclick();
```

### Rule 5: Use Search for Comprehensive Lists

**AVOID**: Homepage widgets (show filtered subsets)
**USE**: Search bar → Type business class name → Select ".List" option

```javascript
await page.click('input[placeholder="Search"]');
await page.type('input[placeholder="Search"]', 'PurchaseOrder');
await page.click('text=PurchaseOrder.PurchaseOrderList');
```

## Environment & Authentication

### Environment Hierarchy

```text
ACUITY_PRD (Production)
├── Real business data, live transactions
├── Cloud Identities auth only
└── High security

ACUITY_TRN (Training)
├── Training data for end users
└── Cloud Identities auth only

ACUITY_TST (Test)
├── BEST data quality for testing
├── Real vendors, employees, emails
└── Cloud Identities auth only

TAMICS10_AX1 (Sandbox)
├── Limited/placeholder data
├── Cloud Identities OR Windows auth
└── Development/POC work
```

### Credential Management

**File Structure**:

```text
Credentials/
├── .env.fsm         # URLs, usernames, password variables
├── .env.passwords   # Actual passwords (NEVER commit)
```

**Python Usage**:

```python
from Credentials.fsm_credentials import get_environment_credentials

creds = get_environment_credentials('ACUITY_TST')
# Returns: {'url': '...', 'username': '...', 'password': '...'}
```

**Security**: Both files in `.gitignore`, passwords resolved at runtime

## Browser Automation Patterns

### Playwright MCP Integration

**Configuration**: `.kiro/settings/mcp.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--isolated"],
      "disabled": false
    }
  }
}
```

**Key Tools**:

- `mcp_playwright_browser_navigate` - Navigate to URLs
- `mcp_playwright_browser_snapshot` - Capture accessibility snapshot (better than screenshot for actions)
- `mcp_playwright_browser_click` - Click elements
- `mcp_playwright_browser_type` - Type text
- `mcp_playwright_browser_fill_form` - Fill multiple fields
- `mcp_playwright_browser_take_screenshot` - Capture screenshots

### Standard Automation Sequence

```javascript
// 1. Navigate and authenticate
await page.goto(creds.url);
await page.fill('input[name="username"]', creds.username);
await page.fill('input[name="password"]', creds.password);
await page.click('button[type="submit"]');

// 2. ALWAYS expand sidebar first
await page.click('button[aria-label="Toggle Navigation"]');
await page.waitForTimeout(500);

// 3. Apply browser zoom (70% recommended)
await page.keyboard.press('Control+Minus');
await page.keyboard.press('Control+Minus');
await page.keyboard.press('Control+Minus');

// 4. Navigate to target
await page.click('text=Shared');
await page.click('text=Document Management');

// 5. Hide sidebar for screen space (optional)
await page.click('button[aria-label="Toggle Navigation"]');
```

### Click Handling Strategies

**Standard Click** (try first):

```javascript
await page.click('selector');
```

**JavaScript Evaluation** (fallback for intercepted clicks):

```javascript
await page.evaluate(() => {
    document.querySelector('selector').click();
});
```

**Double-Click** (for record details):

```javascript
await page.locator('a[href*="PurchaseOrder"]').dblclick();
```

### Element Selector Best Practices

**Selector Priority**:

1. `data-automation-id` - Best for automation
2. `aria-label` - Stable, semantic
3. `role` with `name` - Accessible
4. Text content - Last resort

```javascript
// Best
'button[data-automation-id="save-button"]'

// Good
'button[aria-label="Save"]'

// Acceptable
'button[role="button"][name="Save"]'

// Last resort
'button:has-text("Save")'
```

### Interface Optimization

**Optimal Configuration**:

1. Expand sidebar (☰) - **CRITICAL**
2. Apply 70% browser zoom (Ctrl+Minus 3x)
3. Hide sidebar when done (maximize screen space)
4. Use search-based navigation

**Benefits**:

- More fields visible in data grids
- Better data analysis experience
- Professional appearance maintained
- No layout issues

## FSM Navigation Patterns

### Search-Based Navigation (Recommended)

**Why Use Search**:

- Homepage widgets show filtered subsets only
- Search provides comprehensive lists
- Faster than menu navigation

**Pattern**:

```javascript
await page.click('input[placeholder="Search"]');
await page.type('input[placeholder="Search"]', 'PurchaseOrder');
await page.click('text=PurchaseOrder.PurchaseOrderList'); // Look for .List suffix
```

**Business Class Examples**:

- `PurchaseOrder.PurchaseOrderList` - All POs (not just unreleased)
- `PayablesInvoice.PayablesInvoiceList` - All invoices
- `Vendor.VendorList` - All vendors

### Record Access Patterns

**Single-Click**: Selects record (highlights row)
**Double-Click**: Opens record detail view (REQUIRED)

```javascript
// Wrong - only selects
await page.click('a[href*="PurchaseOrder"]');

// Correct - opens detail
await page.locator('a[href*="PurchaseOrder"]').dblclick();
```

### Menu Navigation with Carets

**Expanding Submenus**:

- Click caret/arrow (▶) to expand without navigating
- Click menu text to navigate to default page

```javascript
// Expand Setup menu without navigating
await page.click('button[aria-label="Expand Setup"]');

// Then click submenu
await page.click('text=Invoice Routing Rules');
```

## Common Mistakes to Avoid

### 1. Forgetting to Expand Sidebar

**Problem**: Attempting navigation without clicking hamburger icon (☰)
**Impact**: Navigation fails, menu items hidden, cannot access admin functions
**Solution**: ALWAYS expand sidebar first before any navigation

### 2. Using CSS Zoom Instead of Browser Zoom

**Problem**: `document.body.style.zoom = "0.7"`
**Impact**: Layout breaks, blank spaces, poor UX
**Solution**: Use `page.keyboard.press('Control+Minus')` 3x

### 3. Wrong Authentication Method

**Problem**: Attempting Windows auth on ACUITY_TST/PRD
**Impact**: Login loops, authentication failures
**Solution**: Use Cloud Identities only for ACUITY environments

### 4. Single-Click Instead of Double-Click

**Problem**: Single-clicking records expecting detail view
**Impact**: Only selects record, doesn't open details
**Solution**: Use `.dblclick()` for record details

### 5. Using Homepage Widgets for Comprehensive Data

**Problem**: Relying on filtered widgets (Unreleased POs, etc.)
**Impact**: Missing data, incomplete analysis
**Solution**: Use search → BusinessClass.List for comprehensive views

### 6. Assuming Sandbox Data Quality

**Problem**: Expecting realistic data in TAMICS10_AX1
**Impact**: Limited testing, placeholder data ([Sample Name])
**Solution**: Use ACUITY_TST for realistic testing

## Environment-Specific Data Quality

### TAMICS10_AX1 (Sandbox)

- **Data**: Limited, placeholder ([Sample Name], [sample@email.com])
- **Use For**: POC, basic functionality testing
- **Avoid For**: Realistic testing, UAT

### ACUITY_TST (Test)

- **Data**: Excellent - real vendors (CDW DIRECT), employees (Angela Erdmann), emails (<example@acuity.com>)
- **Use For**: UAT, comprehensive testing, template validation
- **Best Choice**: Most realistic non-production environment

### ACUITY_PRD (Production)

- **Data**: Live business data
- **Use For**: Production operations only
- **Restrictions**: Change control, limited testing access

## Process Server Administrator Navigation

### Overview

The Process Server Administrator role provides access to IPA process management, including process definitions, version control, and scheduling configuration.

### Accessing Process Server Administrator

**Navigation Path:**

1. Login to FSM environment
2. Switch to "Process Server Administrator" role (if not default)
3. Access via hamburger menu (☰) → Configuration or Scheduling sections

**Key Areas:**

- **Configuration > Process Definitions**: View and manage deployed IPAs
- **Scheduling > Process Triggers**: Configure when IPAs run

### Process Definitions Management

#### Process Definition Types

FSM organizes process definitions into three categories:

| Type | Description | Use Case |
|------|-------------|----------|
| **User Defined Processes** | Custom IPAs uploaded from IPD | Client-specific workflows, custom integrations |
| **System Defined Processes** | Out-of-the-box Infor IPAs | Standard Infor automation, pre-built workflows |
| **Application Defined Processes** | Application-specific IPAs | App-specific automation (FSM, GHR, etc.) |

**Navigation:**

```text
Configuration > Process Definitions > User Defined Processes
Configuration > Process Definitions > System Defined Processes
Configuration > Process Definitions > Application Defined Processes
```

#### Process Definition Detail Page

**Accessing Process Details:**

- Double-click any process in the list to open detail page

**Detail Page Features:**

| Tab/Section | Purpose | Key Information |
|-------------|---------|-----------------|
| **General Tab** | Process overview | Process Name, Description, Category |
| **Properties** | Configuration settings | Work Unit Logging, Auto Restart, Timeout |
| **Process Versions** | Version history | Version number, upload date, uploader, comments |
| **Triggers** | Associated triggers | Scheduled triggers for this process |

**Key Properties:**

- **Work Unit Logging**: Enabled/Disabled (controls log generation)
- **Auto Restart**: Enabled/Disabled (controls restart on failure)
- **Process Category**: Classification for filtering and organization

#### Process Version Management

**Version History Tab:**

- Shows all uploaded versions of the IPA
- Displays version number, upload date, uploader name, and comments
- Right-click context menu provides version management options

**Version Management Actions:**

| Action | Purpose | When to Use |
|--------|---------|-------------|
| **Make Current Version** | Set specific version as active | Rollback to previous version, activate tested version |
| **View Details** | See version metadata | Review upload information, comments |
| **Compare Versions** | Compare two versions | Identify changes between versions |
| **Download** | Download LPD file | Backup, offline review, migration |

**Rollback Procedure:**

1. Navigate to Process Versions tab
2. Right-click desired version
3. Select "Make Current Version"
4. Confirm rollback action
5. New work units will use selected version

**Version History Example (BayCare APIA):**

- **Current Version**: 81
- **Total Versions**: 81 versions uploaded
- **Recent Uploaders**: Nikko Carlo Yabut, Carl Herro
- **Version Comments**: Track changes and deployment notes

### Process Scheduling and Triggers

#### Scheduling Navigation

**Two Scheduling Views:**

| View | Purpose | Navigation |
|------|---------|------------|
| **By Service Definition** | Schedule service-based triggers | Scheduling > By Service Definition |
| **By Process Definition** | Schedule process-based triggers | Scheduling > By Process Definition |

**Recommended View**: Use "By Process Definition" for IPA scheduling

#### Process Trigger Management

**Process Trigger Workflow:**

```text
1. Create Trigger (unscheduled)
   ↓
2. Configure Trigger Properties
   ↓
3. Schedule Trigger (set timing)
   ↓
4. Activate Trigger
```

**Creating Process Triggers:**

1. Navigate to Scheduling > By Process Definition
2. Click "Create" icon button (upper right)
3. Select process definition
4. Configure trigger properties
5. Save (trigger is created but NOT scheduled)

**Trigger Context Menu Options:**

| Option | Purpose | When to Use |
|--------|---------|-------------|
| **Schedule** | Set trigger timing | Configure when IPA runs (daily, hourly, etc.) |
| **Start** | Manually run trigger | Test IPA, run on-demand |
| **Edit** | Modify trigger properties | Update configuration, change parameters |
| **Delete** | Remove trigger | Decommission IPA, clean up unused triggers |
| **Disable/Enable** | Toggle trigger active state | Temporarily stop/resume scheduled runs |
| **View History** | See execution history | Review past runs, troubleshoot issues |

**Scheduling a Trigger:**

1. Right-click trigger in list
2. Select "Schedule" from context menu
3. Configure schedule:
   - **Frequency**: Daily, Weekly, Monthly, Hourly, etc.
   - **Start Time**: When to begin execution
   - **Recurrence**: How often to repeat
   - **End Date**: Optional expiration date
4. Save schedule configuration

**Manual Execution:**

1. Right-click trigger in list
2. Select "Start" from context menu
3. Confirm execution
4. Monitor work unit for results

#### Trigger Configuration Best Practices

**Naming Conventions:**

- Use descriptive names: `APIA_InvoiceApproval_Nightly`
- Include frequency indicator: `_Daily`, `_Hourly`, `_Weekly`
- Add environment prefix: `PRD_`, `TST_`, `TRN_`

**Scheduling Considerations:**

- **Off-Peak Hours**: Schedule resource-intensive IPAs during low-usage periods
- **Business Hours**: Schedule user-facing IPAs during business hours
- **Dependencies**: Consider upstream/downstream process timing
- **Timezone**: Verify server timezone for accurate scheduling

**Monitoring:**

- Enable Work Unit Logging for all scheduled IPAs
- Review execution history regularly
- Set up alerts for failures
- Monitor execution duration trends

### FSM Process Management Workflow

**Complete IPA Deployment Workflow:**

```text
IPD (Development)
   ↓ Upload LPD
FSM Process Definition (User Defined)
   ↓ Create Trigger
Process Trigger (Unscheduled)
   ↓ Schedule
Scheduled Trigger (Active)
   ↓ Execution
Work Unit (Log)
```

**Key Checkpoints:**

1. **Upload**: Verify process appears in User Defined Processes
2. **Version**: Confirm correct version is current
3. **Trigger**: Create trigger with proper configuration
4. **Schedule**: Set appropriate timing for business needs
5. **Test**: Manually start trigger to validate
6. **Monitor**: Review work unit logs for successful execution

### Process Definition Filtering and Search

**Filtering Process Lists:**

- Use column filters to find specific processes
- Example: Filter "Process" column with "APIA" to find invoice approval IPAs
- Combine filters for precise results

**Search Best Practices:**

- Use partial names for broader results
- Filter by category for organized views
- Sort by upload date to find recent changes

### Common Process Management Tasks

#### Task 1: Deploy New IPA Version

1. Upload LPD from IPD to FSM
2. Navigate to Configuration > Process Definitions > User Defined Processes
3. Find process in list (filter if needed)
4. Double-click to open detail page
5. Verify new version appears in Process Versions tab
6. Right-click new version → "Make Current Version"
7. Test with manual trigger start

#### Task 2: Rollback to Previous Version

1. Navigate to process detail page
2. Open Process Versions tab
3. Identify stable version to rollback to
4. Right-click version → "Make Current Version"
5. Confirm rollback
6. Test with manual trigger start
7. Monitor work units for successful execution

#### Task 3: Schedule New IPA

1. Navigate to Scheduling > By Process Definition
2. Click "Create" icon button
3. Select process definition
4. Configure trigger properties (name, description)
5. Save trigger (unscheduled)
6. Right-click trigger → "Schedule"
7. Configure schedule (frequency, start time)
8. Save schedule
9. Verify trigger shows as scheduled

#### Task 4: Disable Scheduled IPA

1. Navigate to Scheduling > By Process Definition
2. Find trigger in list
3. Right-click trigger → "Disable"
4. Confirm disable action
5. Trigger remains configured but won't execute

#### Task 5: Review IPA Execution History

1. Navigate to Scheduling > By Process Definition
2. Find trigger in list
3. Right-click trigger → "View History"
4. Review execution dates, statuses, work unit IDs
5. Click work unit ID to view detailed log

### Integration with Work Unit Analysis

**Connecting Process Management to Work Unit Analysis:**

When analyzing work units, reference process management for context:

- **Process Version**: Check which version executed
- **Trigger Configuration**: Review schedule and parameters
- **Execution History**: Compare with previous runs
- **Version Changes**: Identify if issues started after version change

**Work Unit to Process Definition Lookup:**

1. Note process name from work unit log
2. Navigate to Configuration > Process Definitions
3. Filter by process name
4. Review current version and recent changes
5. Check Process Versions tab for deployment history

## Invoice Approval Workflow Example

*Real-world example: BayCare APIA (Invoice Approval Process Automation)*

### Workflow Overview

```text
User Action (Release Invoice)
   ↓
Business Class Action (PayablesInvoice)
   ↓
Service Definition (InvoiceApproval)
   ↓
IPA Execution (InvoiceApproval_APIA_NONPOROUTING)
   ↓
Work Unit Created (1:1 ratio)
```

### Key Components

**1. Service Definition** (InvoiceApproval)

- Triggered by PayablesInvoice.Release action
- NO filtering at this level - all releases trigger service
- Passes to IPA for routing logic

**2. IPA Process** (InvoiceApproval_APIA_NONPOROUTING.lpd)

- Queries invoice details including RoutingCategory field
- Evaluates routing rules based on RoutingCategory value
- Routes to appropriate approval path
- Creates User Actions for approvers
- Sends email notifications

**3. Routing Logic**

- **RoutingCategory = "F"**: Full approval workflow (L1 Coder → L2 Person Responsible → L3+ Management)
- **RoutingCategory ≠ "F"**: Alternative path (auto-approve, different logic, or exit)

**4. Cross-Application Data** (FSM ↔ GHR)

- FSM IPAs query GHR business classes for employee data
- Dynamic dataArea mapping: BAYCAREHS_TRN_FSM → BAYCAREHS_TRN_HCM
- GHR classes used: HROrganizationUnit, Employee, WorkAssignment, Supervisor
- Purpose: Retrieve Person Responsible, supervisor chain, email addresses

### Automated Workflows

**Nightly Release IPA** (InvoiceApproval_APIA_NONPOROUTING_nightly_job_trigger.lpd)

- Scheduled trigger runs nightly
- Queries unreleased invoices
- Programmatically calls Release action
- Each release triggers main approval IPA

**Auto-Reject IPA** (InvoiceApproval_APIA_NONPOROUTING_Reject.lpd)

- Standalone monitoring process (runs daily)
- Queries work units pending > 30 business days
- Auto-rejects stale invoices
- Sends notification emails
- NOT part of main approval workflow

### Key Principles

1. **No Service-Level Filtering**: Service Definition passes ALL releases to IPA
2. **One-to-One Work Units**: One invoice = one work unit (audit trail)
3. **IPA Internal Routing**: All routing logic inside IPA based on rules
4. **Nightly Trigger Optional**: Just automation convenience, not required
5. **Reject IPA Standalone**: Separate monitoring process, not part of approval flow

### Navigation Tips

**Access Invoice Management**:

1. Switch to Payables Manager role
2. Expand sidebar (☰)
3. Click "Manage Invoices"

**Access Routing Rules**:

1. Expand sidebar (☰)
2. Click Setup caret (▶) to expand
3. Click "Invoice Approval Setup" caret
4. Click "Invoice Routing Rules"

**Access Service Definitions**:

1. Switch to Process Server Administrator role
2. Configuration > Service Definitions
3. Search "InvoiceApproval"

---

*This guide provides practical patterns for FSM navigation and browser automation based on real-world experience.*

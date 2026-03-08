# Coding Standards Reference

Complete reference for IPA coding standards rules.

## Naming Standards (1.1.x)

### Rule 1.1.1: Filename Format

**Description**: Filename must match process type pattern

**Patterns**:
- Approval Workflow: `<Prefix>_WF_<Description>.lpd`
- Interface Process: `<Prefix>_INT_<Source>_<Dest>_<Description>.lpd`
- Scheduled Process: `<Prefix>_SCH_<Description>.lpd`

**Severity**: High

### Rule 1.1.2: Node Naming

**Description**: Node captions must be descriptive, not generic

**Examples**:
- Generic (violation): "Assign 1", "Branch 1", "WebRun 1"
- Descriptive (compliant): "Calculate Total Amount", "Route to Manager", "Call Approval API"

**Severity**: Medium

## JavaScript Standards (1.2.x)

### Rule 1.2.1: Process Variables

**Description**: Process variables initialized on Start node (no var keyword)

**Example**:
```javascript
// Start node (compliant)
vApproverList = "";
vTotalAmount = 0;
```

**Severity**: Medium

### Rule 1.2.3: Function Declaration Order

**Description**: Functions declared before use

**Severity**: Low

## Error Handling Standards (1.3.x)

### Rule 1.3.1: OnError Tabs

**Description**: Error-prone activities must have OnError tabs

**Severity**: High

### Rule 1.3.2: GetWorkUnitErrors

**Description**: Process must have GetWorkUnitErrors activity

**Severity**: High

## Configuration Standards (1.4.x)

### Rule 1.4.1: Config Set Naming

**Description**: Config sets must include vendor/system name

**Examples**:
- Generic (violation): "Config", "Settings"
- Vendor-specific (compliant): "Hyland_OnBase_Config", "Infor_FSM_Settings"

**Severity**: Medium

### Rule 1.4.3: Hardcoded Values

**Description**: Use ${ConfigSet.Variable} instead of hardcoded values

**Severity**: Medium

## SQL Standards (1.5.x)

### Rule 1.5.2: Pagination

**Description**: Pagination required for queries returning >100 rows

**Severity**: High

---

For more information, see:
- [`DOMAIN_ANALYSIS_GUIDE.md`](DOMAIN_ANALYSIS_GUIDE.md) - Domain-specific patterns
- [`WORKFLOW_GUIDE.md`](WORKFLOW_GUIDE.md) - Complete workflow

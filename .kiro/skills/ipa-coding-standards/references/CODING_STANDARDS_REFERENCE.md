# Coding Standards Reference

Complete reference for IPA coding standards rules.

## External References

For comprehensive IPA knowledge, consult these steering files:

- **`.kiro/steering/02_IPA_and_IPD_Complete_Guide.md`** - IPA concepts, LPD structure, activity nodes, Start node properties, JavaScript ES5, work units
- **`.kiro/steering/06_Compass_SQL_CheatSheet.md`** - Compass SQL dialect, Data Fabric queries, pagination patterns
- **`.kiro/steering/07_FSM_Business_Classes_and_API.md`** - FSM business classes, Landmark API, RICE methodology
- **`.kiro/steering/04_Process_Patterns_Library.md`** - 450+ analyzed workflows, approval patterns, interface patterns

These steering files contain production-tested knowledge from real implementations.

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

**Description**: Process-level variables must be defined on Start node

**IPA Implementation**: In IPA, Start node variables are defined in the **Properties** tab, NOT as JavaScript code. Each property becomes a global variable accessible throughout the process.

**Example**:
```
Start Node Properties:
- queryID = ""
- auth = ""
- rowCount = 0
- tempCount = 0
```

These properties automatically become global variables (no `var` keyword needed).

**Common Mistake**: Looking for JavaScript code on Start node. Start node rarely has JavaScript - variables are in Properties.

**Reference**: See `.kiro/steering/02_IPA_and_IPD_Complete_Guide.md` for complete IPA variable scoping rules.

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

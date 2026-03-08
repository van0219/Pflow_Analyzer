# Compass SQL Analyzer References

This folder contains detailed documentation for the Compass SQL Analyzer skill.

## Contents

### [analysis-rules.md](analysis-rules.md)

Comprehensive ruleset for analyzing Compass SQL queries:

- **Syntax Validation Rules** (S1-S5): DML/DDL checks, quoting, CAST types, JOIN syntax, reserved words
- **Performance Analysis Rules** (P1-P6): Pagination, CAST safety, Cartesian products, WHERE selectivity, JOIN order, DISTINCT
- **Durability Assessment Rules** (D1-D4): Timeout protection, bounded results, scalable aggregations, memory-intensive operations
- **Flexibility Review Rules** (F1-F4): Parameterization, environment-agnostic names, configuration externalization, reusable structure
- **Best Practices Rules** (B1-B5): NULL safety, defensive programming, formatting, comments, Compass SQL idioms
- **Code Quality Rules** (Q1-Q3): Readable structure, descriptive aliases, modular CTEs

### [example-queries.md](example-queries.md)

Real-world Compass SQL examples with analysis:

- Good examples (production-ready)
- Bad examples (common mistakes)
- Before/after refactoring
- Performance comparisons

### [compass_sql_official_reference.txt](compass_sql_official_reference.txt)

Official Compass SQL documentation extracted from Infor Data Fabric User Guide:

- Chapter 11: Compass SQL Reference (pages 240-271)
- Complete function reference
- Query structure and clauses
- All supported syntax
- Source material for steering file and skill

### [ipa-integration.md](ipa-integration.md)

Patterns for using Compass SQL in IPA processes:

- WebRun activity configuration
- Pagination loops in JavaScript ES5
- Error handling with GetWorkUnitErrors
- Variable substitution patterns
- Performance optimization for IPA

## Quick Links

**Main Skill**: [../SKILL.md](../SKILL.md)  
**Scripts**: [../scripts/](../scripts/)  
**Compass SQL Syntax**: `.kiro/steering/06_Compass_SQL_CheatSheet.md`  
**Data Fabric Guide**: `.kiro/steering/08_Infor_OS_Data_Fabric_Guide.md`

## Usage

These references are automatically loaded when the skill is activated. You can also reference them directly:

```text
Show me examples from references/example-queries.md
Explain rule P2 from references/analysis-rules.md
```

## Contributing

When adding new patterns or rules:

1. Update relevant reference file
2. Add examples with explanations
3. Include before/after code samples
4. Document severity and impact
5. Test with real queries

#!/usr/bin/env python3
"""
Kiro Hook Manager - Comprehensive hook file management and diagnostics

A powerful tool for validating, analyzing, backing up, and repairing hook files.
Provides detailed diagnostics to help AI agents understand hook issues.

Usage:
    python hook_manager.py validate <hook_file>           # Deep validation with diagnostics
    python hook_manager.py validate --all                 # Validate all hooks
    python hook_manager.py backup <hook_file>             # Create timestamped backup
    python hook_manager.py restore <hook_file> <backup>   # Restore from backup
    python hook_manager.py diff <hook1> <hook2>           # Compare two hooks
    python hook_manager.py analyze <hook_file>            # Deep structural analysis
    python hook_manager.py repair <hook_file>             # Attempt automatic repair
    python hook_manager.py export <hook_file> <json>      # Export to clean JSON
    python hook_manager.py update <hook_file> <field=value> ...  # Update hook fields
    python hook_manager.py search <pattern> [search_in]   # Search hooks
    python hook_manager.py lint <hook_file>               # Check for issues
"""

import json
import sys
import glob
import shutil
from pathlib import Path
from datetime import datetime
from difflib import unified_diff
import re

class HookManager:
    """Comprehensive hook file manager"""
    
    def __init__(self):
        self.hooks_dir = Path('.kiro/hooks')
        self.backup_dir = Path('.kiro/hooks/.backups')
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def validate(self, filepath, verbose=True):
        """
        Deep validation with comprehensive diagnostics
        
        Returns: dict with validation results and diagnostics
        """
        result = {
            'valid': False,
            'filepath': str(filepath),
            'errors': [],
            'warnings': [],
            'info': {},
            'structure': {},
            'diagnostics': []
        }
        
        # Check file exists
        if not Path(filepath).exists():
            result['errors'].append(f"File not found: {filepath}")
            return result
        
        # Read file
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                result['info']['file_size'] = len(content)
                result['info']['line_count'] = content.count('\n') + 1
        except UnicodeDecodeError as e:
            result['errors'].append(f"Encoding error: {e}")
            result['diagnostics'].append("File contains non-UTF-8 characters")
            result['diagnostics'].append("Try using repair() to fix encoding issues")
            return result
        except Exception as e:
            result['errors'].append(f"Cannot read file: {e}")
            return result
        
        # Parse JSON
        try:
            data = json.loads(content)
            result['valid'] = True
            result['info']['json_valid'] = True
        except json.JSONDecodeError as e:
            result['errors'].append(f"Invalid JSON at line {e.lineno}, col {e.colno}: {e.msg}")
            result['diagnostics'].append(f"Error position: character {e.pos}")
            
            # Try to identify the problematic area
            lines = content.split('\n')
            if e.lineno <= len(lines):
                problem_line = lines[e.lineno - 1]
                result['diagnostics'].append(f"Problem line {e.lineno}: {problem_line[:100]}")
            
            # Check for common issues
            if '\\n' in content and '\n' in content:
                result['diagnostics'].append("Mixed newline escaping detected")
            
            control_chars = [c for c in content if ord(c) < 32 and c not in '\n\r\t']
            if control_chars:
                result['diagnostics'].append(f"Found {len(control_chars)} control characters")
            
            return result
        
        # Validate structure
        required_fields = ['enabled', 'name', 'when', 'then']
        for field in required_fields:
            if field not in data:
                result['errors'].append(f"Missing required field: {field}")
            else:
                result['structure'][field] = type(data[field]).__name__
        
        # Extract metadata
        result['info']['name'] = data.get('name', 'N/A')
        result['info']['version'] = data.get('version', 'N/A')
        result['info']['enabled'] = data.get('enabled', False)
        result['info']['new_session'] = data.get('newSession', False)
        
        # Validate 'when' structure
        when = data.get('when', {})
        result['structure']['when_type'] = when.get('type', 'N/A')
        if 'patterns' in when:
            result['structure']['when_patterns'] = len(when['patterns'])
        if 'toolTypes' in when:
            result['structure']['when_toolTypes'] = when['toolTypes']
        
        # Validate 'then' structure
        then = data.get('then', {})
        result['structure']['then_type'] = then.get('type', 'N/A')
        
        if 'prompt' in then:
            prompt = then['prompt']
            result['info']['prompt_length'] = len(prompt)
            result['info']['prompt_lines'] = prompt.count('\n') + 1
            
            # Analyze prompt structure
            steps = re.findall(r'STEP \d+:', prompt)
            if steps:
                result['structure']['workflow_steps'] = len(steps)
                result['diagnostics'].append(f"Found {len(steps)} workflow steps")
            
            # Check for subagent invocations
            subagents = re.findall(r'invokeSubAgent\(', prompt)
            if subagents:
                result['structure']['subagent_calls'] = len(subagents)
                result['diagnostics'].append(f"Found {len(subagents)} subagent invocations")
        
        if 'command' in then:
            result['info']['command_length'] = len(then['command'])
        
        # Warnings
        if result['info'].get('prompt_length', 0) > 20000:
            result['warnings'].append("Very large prompt (>20K chars) - may cause performance issues")
        
        if not data.get('enabled', True):
            result['warnings'].append("Hook is disabled")
        
        # Success diagnostics
        if result['valid'] and not result['errors']:
            result['diagnostics'].append("✓ All required fields present")
            result['diagnostics'].append("✓ JSON structure valid")
            result['diagnostics'].append(f"✓ Hook type: {result['structure']['when_type']}")
            result['diagnostics'].append(f"✓ Action type: {result['structure']['then_type']}")
        
        return result
    
    def backup(self, filepath):
        """Create timestamped backup of hook file"""
        if not Path(filepath).exists():
            return {'success': False, 'error': f"File not found: {filepath}"}
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = Path(filepath).name
        backup_path = self.backup_dir / f"{filename}.{timestamp}.backup"
        
        try:
            shutil.copy2(filepath, backup_path)
            return {
                'success': True,
                'backup_path': str(backup_path),
                'timestamp': timestamp,
                'original_size': Path(filepath).stat().st_size,
                'backup_size': backup_path.stat().st_size
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def restore(self, filepath, backup_path):
        """Restore hook from backup"""
        if not Path(backup_path).exists():
            return {'success': False, 'error': f"Backup not found: {backup_path}"}
        
        try:
            # Backup current file first
            current_backup = self.backup(filepath)
            
            # Restore from backup
            shutil.copy2(backup_path, filepath)
            
            return {
                'success': True,
                'restored_from': str(backup_path),
                'current_backup': current_backup.get('backup_path'),
                'restored_size': Path(filepath).stat().st_size
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_backups(self, filepath):
        """List all backups for a hook file"""
        filename = Path(filepath).name
        backups = sorted(self.backup_dir.glob(f"{filename}.*.backup"), reverse=True)
        
        result = []
        for backup in backups:
            timestamp_str = backup.stem.split('.')[-1]
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                result.append({
                    'path': str(backup),
                    'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'size': backup.stat().st_size,
                    'age_hours': (datetime.now() - timestamp).total_seconds() / 3600
                })
            except:
                pass
        
        return result
    
    def diff(self, file1, file2):
        """Compare two hook files"""
        try:
            with open(file1, 'r') as f:
                lines1 = f.readlines()
            with open(file2, 'r') as f:
                lines2 = f.readlines()
            
            diff = list(unified_diff(
                lines1, lines2,
                fromfile=str(file1),
                tofile=str(file2),
                lineterm=''
            ))
            
            return {
                'success': True,
                'diff_lines': len(diff),
                'diff': '\n'.join(diff[:100])  # First 100 lines
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze(self, filepath):
        """Deep structural analysis"""
        validation = self.validate(filepath, verbose=False)
        
        if not validation['valid']:
            return validation
        
        # Load hook data
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        
        analysis = {
            'validation': validation,
            'complexity': {},
            'dependencies': [],
            'recommendations': []
        }
        
        # Complexity analysis
        prompt = data.get('then', {}).get('prompt', '')
        
        analysis['complexity']['prompt_length'] = len(prompt)
        analysis['complexity']['steps'] = len(re.findall(r'STEP \d+:', prompt))
        analysis['complexity']['subagents'] = len(re.findall(r'invokeSubAgent', prompt))
        analysis['complexity']['file_operations'] = len(re.findall(r'(fsWrite|fsAppend|readFile)', prompt))
        analysis['complexity']['shell_commands'] = len(re.findall(r'executePwsh', prompt))
        
        # Calculate complexity score
        score = (
            analysis['complexity']['steps'] * 2 +
            analysis['complexity']['subagents'] * 5 +
            analysis['complexity']['file_operations'] * 1 +
            analysis['complexity']['shell_commands'] * 3
        )
        analysis['complexity']['score'] = score
        analysis['complexity']['rating'] = (
            'Simple' if score < 20 else
            'Moderate' if score < 50 else
            'Complex' if score < 100 else
            'Very Complex'
        )
        
        # Detect dependencies
        if 'readMultipleFiles' in prompt:
            analysis['dependencies'].append('Steering files')
        if 'invokeSubAgent' in prompt:
            subagent_names = re.findall(r'name="([^"]+)"', prompt)
            analysis['dependencies'].extend([f"Subagent: {name}" for name in subagent_names])
        if 'ReusableTools' in prompt:
            tools = re.findall(r'ReusableTools/([^/\s"\']+)', prompt)
            analysis['dependencies'].extend([f"Tool: {tool}" for tool in set(tools)])
        
        # Recommendations (context-aware)
        # Note: Large workflow hooks are INTENTIONAL - they orchestrate complex processes
        # Breaking them would destroy the sequential workflow logic
        
        if analysis['complexity']['subagents'] > 5:
            analysis['recommendations'].append("Many subagents - ensure error handling and graceful degradation")
        
        if len(prompt) > 20000:
            analysis['recommendations'].append("Very large prompt (>20K) - this is acceptable for workflow orchestration hooks")
        
        if analysis['complexity']['shell_commands'] > 20:
            analysis['recommendations'].append("Many shell commands - verify error handling for each")
        
        if analysis['complexity']['file_operations'] > 30:
            analysis['recommendations'].append("Many file operations - consider using file-writer-helper subagent for reliability")
        
        # Positive feedback for well-structured hooks
        if 10 <= analysis['complexity']['steps'] <= 30:
            analysis['recommendations'].append("✓ Good workflow structure with clear steps")
        
        if analysis['complexity']['subagents'] > 0:
            analysis['recommendations'].append("✓ Uses subagents for parallel processing - good architecture")
        
        return analysis
    
    def repair(self, filepath):
        """Attempt automatic repair of hook file"""
        # Backup first
        backup_result = self.backup(filepath)
        if not backup_result['success']:
            return backup_result
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            repairs = []
            
            # Remove control characters
            original_len = len(content)
            content = ''.join(char if ord(char) >= 32 or char in '\n\r\t' else ' ' for char in content)
            if len(content) != original_len:
                repairs.append(f"Removed {original_len - len(content)} control characters")
            
            # Try to parse
            try:
                data = json.loads(content)
                
                # Save repaired version
                with open(filepath, 'w', encoding='utf-8', newline='\n', errors='replace') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                repairs.append("Reformatted JSON with proper indentation")
                
                return {
                    'success': True,
                    'repairs': repairs,
                    'backup': backup_result['backup_path']
                }
            except json.JSONDecodeError as e:
                return {
                    'success': False,
                    'error': f"Cannot repair: {e.msg}",
                    'backup': backup_result['backup_path']
                }
        
        except UnicodeDecodeError as e:
            return {
                'success': False,
                'error': f'Encoding error: {e}',
                'suggestion': 'File has severe encoding issues that cannot be automatically repaired',
                'backup': backup_result['backup_path']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'backup': backup_result['backup_path']
            }
    
    def export(self, filepath, output_path):
        """Export hook to clean JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                data = json.load(f)
            
            with open(output_path, 'w', encoding='utf-8', newline='\n', errors='replace') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'output_path': output_path,
                'size': Path(output_path).stat().st_size
            }
        except UnicodeDecodeError as e:
            return {
                'success': False,
                'error': f'Encoding error: {e}',
                'suggestion': 'File contains non-UTF-8 characters. Try using repair() first.'
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update(self, filepath, updates):
        """
        Safely update hook fields
        
        Parameters:
            filepath: Path to hook file
            updates: Dict of fields to update (e.g., {'version': '2', 'enabled': False})
        
        Returns:
            dict with success, backup_path, changes, validation
        """
        if not Path(filepath).exists():
            return {'success': False, 'error': f"File not found: {filepath}"}
        
        try:
            # Backup first
            backup_result = self.backup(filepath)
            if not backup_result['success']:
                return backup_result
            
            # Load current hook
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                hook = json.load(f)
            
            # Track changes
            changes = []
            
            # Apply updates
            for key, value in updates.items():
                if key in hook:
                    old_value = hook[key]
                    hook[key] = value
                    changes.append({
                        'field': key,
                        'old': old_value,
                        'new': value
                    })
                else:
                    # New field
                    hook[key] = value
                    changes.append({
                        'field': key,
                        'old': None,
                        'new': value
                    })
            
            # Validate updated hook
            temp_path = Path(filepath).parent / f".temp_{Path(filepath).name}"
            with open(temp_path, 'w', encoding='utf-8', newline='\n', errors='replace') as f:
                json.dump(hook, f, indent=2, ensure_ascii=False)
            
            validation = self.validate(str(temp_path), verbose=False)
            
            if validation['valid']:
                # Save updated hook
                shutil.move(str(temp_path), filepath)
                
                return {
                    'success': True,
                    'backup_path': backup_result['backup_path'],
                    'changes': changes,
                    'validation': validation
                }
            else:
                # Validation failed, remove temp file
                temp_path.unlink()
                return {
                    'success': False,
                    'error': 'Updated hook failed validation',
                    'validation_errors': validation['errors'],
                    'backup_path': backup_result['backup_path']
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'backup_path': backup_result.get('backup_path')
            }
    
    def search(self, pattern, search_in='all'):
        """
        Search hooks by name, description, or prompt content
        
        Parameters:
            pattern: Search pattern (case-insensitive)
            search_in: Where to search - 'name', 'description', 'prompt', 'all'
        
        Returns:
            list of matching hooks with details
        """
        hooks = sorted(self.hooks_dir.glob('*.kiro.hook'))
        results = []
        
        pattern_lower = pattern.lower()
        
        for hook_path in hooks:
            try:
                with open(hook_path, 'r', encoding='utf-8', errors='replace') as f:
                    data = json.load(f)
                
                match = False
                match_locations = []
                
                # Search in name
                if search_in in ['name', 'all']:
                    if pattern_lower in data.get('name', '').lower():
                        match = True
                        match_locations.append('name')
                
                # Search in description
                if search_in in ['description', 'all']:
                    if pattern_lower in data.get('description', '').lower():
                        match = True
                        match_locations.append('description')
                
                # Search in prompt
                if search_in in ['prompt', 'all']:
                    prompt = data.get('then', {}).get('prompt', '')
                    if pattern_lower in prompt.lower():
                        match = True
                        match_locations.append('prompt')
                
                if match:
                    results.append({
                        'path': str(hook_path),
                        'name': data.get('name', 'N/A'),
                        'version': data.get('version', 'N/A'),
                        'enabled': data.get('enabled', False),
                        'type': data.get('when', {}).get('type', 'N/A'),
                        'match_locations': match_locations
                    })
            
            except Exception as e:
                results.append({
                    'path': str(hook_path),
                    'error': f'Failed to search: {e}'
                })
        
        return results
    
    def lint(self, filepath):
        """
        Check hook for common issues and suggest improvements
        
        Returns:
            dict with issues, warnings, suggestions
        """
        validation = self.validate(filepath, verbose=False)
        
        if not validation['valid']:
            return {
                'success': False,
                'error': 'Hook failed validation',
                'validation': validation
            }
        
        # Load hook
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        
        issues = []
        warnings = []
        suggestions = []
        
        # Check version field
        if 'version' not in data:
            issues.append("Missing 'version' field")
        
        # Check description
        if 'description' not in data or not data.get('description'):
            warnings.append("Missing or empty 'description' field")
        
        # Check prompt length
        prompt = data.get('then', {}).get('prompt', '')
        if len(prompt) > 30000:
            warnings.append(f"Very large prompt ({len(prompt)} chars) - may cause performance issues")
        elif len(prompt) > 20000:
            suggestions.append(f"Large prompt ({len(prompt)} chars) - consider breaking into smaller hooks if possible")
        
        # Check for common patterns
        if 'fsWrite' in prompt and data.get('when', {}).get('type') in ['preToolUse', 'postToolUse']:
            warnings.append("Hook uses fsWrite in tool-triggered context - may cause infinite loops")
        
        # Check for proper error handling in prompt
        if 'try' not in prompt.lower() and len(prompt) > 1000:
            suggestions.append("Consider adding error handling instructions in prompt")
        
        # Check for step structure
        if 'STEP' in prompt.upper():
            steps = re.findall(r'STEP \d+:', prompt)
            if len(steps) > 20:
                suggestions.append(f"Hook has {len(steps)} steps - consider breaking into smaller workflows")
        
        # Check enabled status
        if not data.get('enabled', True):
            warnings.append("Hook is disabled")
        
        # Check for newSession flag
        if data.get('newSession', False):
            suggestions.append("Hook uses newSession=true - ensure this is intentional as it starts fresh context")
        
        return {
            'success': True,
            'filepath': str(filepath),
            'issues': issues,
            'warnings': warnings,
            'suggestions': suggestions,
            'summary': {
                'total_issues': len(issues),
                'total_warnings': len(warnings),
                'total_suggestions': len(suggestions)
            }
        }

def print_validation_report(result):
    """Print comprehensive validation report"""
    print(f"\n{'='*70}")
    print(f"HOOK VALIDATION REPORT: {result['filepath']}")
    print('='*70)
    
    # Status
    if result['valid'] and not result['errors']:
        print("✓ STATUS: VALID")
    else:
        print("✗ STATUS: INVALID")
    
    # Info
    print(f"\nINFO:")
    for key, value in result['info'].items():
        print(f"  {key}: {value}")
    
    # Structure
    if result['structure']:
        print(f"\nSTRUCTURE:")
        for key, value in result['structure'].items():
            print(f"  {key}: {value}")
    
    # Errors
    if result['errors']:
        print(f"\n✗ ERRORS ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"  - {error}")
    
    # Warnings
    if result['warnings']:
        print(f"\n⚠ WARNINGS ({len(result['warnings'])}):")
        for warning in result['warnings']:
            print(f"  - {warning}")
    
    # Diagnostics
    if result['diagnostics']:
        print(f"\nDIAGNOSTICS:")
        for diag in result['diagnostics']:
            print(f"  {diag}")
    
    print('='*70)

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    manager = HookManager()
    command = sys.argv[1]
    
    if command == 'validate':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py validate <hook_file>")
            print("       python hook_manager.py validate --all")
            sys.exit(1)
        
        if sys.argv[2] == '--all':
            hooks = sorted(glob.glob('.kiro/hooks/*.kiro.hook'))
            for hook in hooks:
                result = manager.validate(hook)
                print_validation_report(result)
        else:
            result = manager.validate(sys.argv[2])
            print_validation_report(result)
    
    elif command == 'backup':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py backup <hook_file>")
            sys.exit(1)
        
        result = manager.backup(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == 'restore':
        if len(sys.argv) < 4:
            print("Usage: python hook_manager.py restore <hook_file> <backup_path>")
            sys.exit(1)
        
        result = manager.restore(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif command == 'list-backups':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py list-backups <hook_file>")
            sys.exit(1)
        
        backups = manager.list_backups(sys.argv[2])
        print(json.dumps(backups, indent=2))
    
    elif command == 'diff':
        if len(sys.argv) < 4:
            print("Usage: python hook_manager.py diff <hook1> <hook2>")
            sys.exit(1)
        
        result = manager.diff(sys.argv[2], sys.argv[3])
        if result['success']:
            print(result['diff'])
        else:
            print(f"Error: {result['error']}")
    
    elif command == 'analyze':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py analyze <hook_file>")
            sys.exit(1)
        
        result = manager.analyze(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == 'repair':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py repair <hook_file>")
            sys.exit(1)
        
        result = manager.repair(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == 'export':
        if len(sys.argv) < 4:
            print("Usage: python hook_manager.py export <hook_file> <output.json>")
            sys.exit(1)
        
        result = manager.export(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Usage: python hook_manager.py update <hook_file> <field=value> [<field=value> ...]")
            print("Example: python hook_manager.py update hook.kiro.hook version=2 enabled=false")
            sys.exit(1)
        
        # Parse field=value pairs
        updates = {}
        for arg in sys.argv[3:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                # Try to parse as JSON value
                try:
                    updates[key] = json.loads(value)
                except:
                    updates[key] = value
        
        result = manager.update(sys.argv[2], updates)
        print(json.dumps(result, indent=2))
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py search <pattern> [search_in]")
            print("  search_in: name, description, prompt, all (default: all)")
            sys.exit(1)
        
        search_in = sys.argv[3] if len(sys.argv) > 3 else 'all'
        results = manager.search(sys.argv[2], search_in)
        print(json.dumps(results, indent=2))
    
    elif command == 'lint':
        if len(sys.argv) < 3:
            print("Usage: python hook_manager.py lint <hook_file>")
            sys.exit(1)
        
        result = manager.lint(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()

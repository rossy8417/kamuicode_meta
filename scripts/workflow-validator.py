#!/usr/bin/env python3
"""
Unified GitHub Actions Workflow Validator and Fixer
Consolidates validation, error detection, and auto-repair functionality.
"""

import sys
import yaml
import re
import json
import os
from pathlib import Path

class WorkflowValidator:
    """
    Comprehensive workflow validation and repair tool.
    Consolidates functionality from multiple scripts.
    """
    
    def __init__(self, workflow_path):
        self.workflow_path = Path(workflow_path)
        self.content = None
        self.yaml_data = None
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        
    def validate_and_fix(self):
        """Main entry point for validation and auto-repair."""
        print(f"🔍 Validating workflow: {self.workflow_path}")
        
        # Read file
        if not self._read_file():
            return False
            
        # Phase 1: Detect and fix critical issues
        if self._detect_critical_issues():
            print("🔧 Critical issues detected, applying fixes...")
            self._apply_fixes()
            
        # Phase 2: Validate fixed content
        validation_passed = self._validate_content()
        
        # Phase 3: Generate report
        self._generate_report()
        
        return validation_passed
        
    def _read_file(self):
        """Read workflow file content."""
        try:
            with open(self.workflow_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            self.errors.append(f"Failed to read file: {e}")
            return False
            
    def _detect_critical_issues(self):
        """Detect issues that prevent workflow execution."""
        issues_found = False
        
        # Check for HEREDOC patterns
        heredoc_pattern = r'cat\s*>\s*[^\s]+\s*<<\s*[\'"]?EOF'
        if re.search(heredoc_pattern, self.content, re.MULTILINE):
            self.errors.append("HEREDOC pattern detected - will cause YAML parsing errors")
            issues_found = True
            
        # Check for local uses references
        local_uses_pattern = r'uses:\s*[\'"]?\./[^\'"\s]+'
        if re.search(local_uses_pattern, self.content):
            self.errors.append("Local 'uses' references detected - not supported in GitHub Actions")
            issues_found = True
            
        # Try YAML parsing
        try:
            yaml.safe_load(self.content)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error: {e}")
            issues_found = True
            
        return issues_found
        
    def _apply_fixes(self):
        """Apply automatic fixes for detected issues."""
        original_content = self.content
        
        # Fix quoted "on" field
        if re.search(r'^"on":', self.content, re.MULTILINE):
            self.content = re.sub(r'^"on":', 'on:', self.content, flags=re.MULTILINE)
            self.fixes_applied.append("Fixed quoted 'on' field")
        
        # Remove invalid matrix references in outputs
        if re.search(r'outputs:.*\$\{\{\s*matrix\.', self.content):
            # Remove lines with matrix references in outputs sections
            lines = self.content.split('\n')
            new_lines = []
            in_outputs = False
            for line in lines:
                if re.match(r'^\s*outputs:', line):
                    in_outputs = True
                elif re.match(r'^\s*steps:', line) or (in_outputs and re.match(r'^\s*\w+:', line) and not re.match(r'^\s+', line)):
                    in_outputs = False
                
                if not (in_outputs and 'matrix.' in line):
                    new_lines.append(line)
            
            self.content = '\n'.join(new_lines)
            self.fixes_applied.append("Removed invalid matrix references in outputs")
        
        # Fix HEREDOC patterns
        self.content = self._fix_heredoc_patterns(self.content)
        if self.content != original_content:
            self.fixes_applied.append("Converted HEREDOC to echo commands")
            
        # Fix local uses references  
        self.content = self._fix_local_uses(self.content)
        
        # Save fixed content
        if self.fixes_applied:
            backup_path = self.workflow_path.with_suffix('.yml.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"📋 Original backed up to: {backup_path}")
            
            with open(self.workflow_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"✅ Fixed workflow saved: {self.workflow_path}")
            
    def _fix_heredoc_patterns(self, content):
        """Convert HEREDOC patterns to echo commands."""
        
        def replace_heredoc(match):
            indent = len(match.group(0)) - len(match.group(0).lstrip())
            spaces = ' ' * indent
            filepath = match.group(1)
            heredoc_content = match.group(2).strip()
            
            lines = heredoc_content.split('\n')
            echo_commands = []
            
            for i, line in enumerate(lines):
                # Escape special characters
                escaped = line.replace('\\', '\\\\').replace('"', '\\"').replace('$', '\\$')
                if i == 0:
                    echo_commands.append(f'{spaces}echo "{escaped}" > {filepath}')
                else:
                    echo_commands.append(f'{spaces}echo "{escaped}" >> {filepath}')
                    
            return '\n'.join(echo_commands)
            
        # Pattern: cat > file << 'EOF' ... EOF
        pattern = r'^(\s*)cat\s*>\s*([^\s]+)\s*<<\s*[\'"]?EOF[\'"]?\n(.*?)\n\1EOF'
        content = re.sub(pattern, replace_heredoc, content, flags=re.MULTILINE | re.DOTALL)
        
        return content
        
    def _fix_local_uses(self, content):
        """Comment out local uses references with explanation."""
        
        def replace_uses(match):
            indent = match.group(1)
            local_path = match.group(2)
            
            replacement = f'{indent}# DISABLED: Local uses not supported\n'
            replacement += f'{indent}# Original: uses: {local_path}\n'
            replacement += f'{indent}# TODO: Inline the implementation from {local_path}\n'
            replacement += f'{indent}run: echo "Placeholder for {local_path}"'
            
            self.fixes_applied.append(f"Disabled local uses: {local_path}")
            return replacement
            
        pattern = r'^(\s*)uses:\s*[\'"]?(\.\/[^\'"\s]+)'
        content = re.sub(pattern, replace_uses, content, flags=re.MULTILINE)
        
        return content
        
    def _validate_content(self):
        """Validate the workflow content."""
        
        # Clear previous validation errors
        self.errors = []
        self.warnings = []
        
        # Check YAML syntax
        try:
            self.yaml_data = yaml.safe_load(self.content)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing failed: {e}")
            return False
            
        # Check required fields
        if not self.yaml_data:
            self.errors.append("Empty YAML file")
            return False
            
        # Special handling for 'on' field (can be parsed as True in YAML 1.1)
        required_fields = ['name', 'jobs']
        for field in required_fields:
            if field not in self.yaml_data:
                self.errors.append(f"Missing required field: '{field}'")
        
        # Check for 'on' field (might be parsed as True)
        if 'on' not in self.yaml_data and True not in self.yaml_data:
            self.errors.append("Missing required field: 'on'")
                
        # Check workflow_dispatch if present
        on_config = self.yaml_data.get('on') or self.yaml_data.get(True)
        if on_config:
            if isinstance(on_config, dict) and 'workflow_dispatch' in on_config:
                dispatch = on_config['workflow_dispatch']
                if dispatch is None:
                    # This is valid - no inputs
                    pass
                elif isinstance(dispatch, dict) and 'inputs' in dispatch:
                    # Validate inputs structure
                    self._validate_inputs(dispatch['inputs'])
                    
        # Check jobs structure
        if 'jobs' in self.yaml_data:
            self._validate_jobs(self.yaml_data['jobs'])
            
        # Check for common issues
        self._check_common_issues()
        
        return len(self.errors) == 0
        
    def _validate_inputs(self, inputs):
        """Validate workflow_dispatch inputs."""
        if not isinstance(inputs, dict):
            self.errors.append("workflow_dispatch inputs must be a dictionary")
            return
            
        for name, config in inputs.items():
            if not isinstance(config, dict):
                self.errors.append(f"Input '{name}' configuration must be a dictionary")
                continue
                
            # Check type field
            if 'type' in config:
                valid_types = ['string', 'choice', 'boolean', 'environment']
                if config['type'] not in valid_types:
                    self.warnings.append(f"Input '{name}' has uncommon type: {config['type']}")
                    
            # Check choice options
            if config.get('type') == 'choice' and 'options' not in config:
                self.errors.append(f"Choice input '{name}' missing 'options'")
                
    def _validate_jobs(self, jobs):
        """Validate jobs structure."""
        if not isinstance(jobs, dict):
            self.errors.append("Jobs must be a dictionary")
            return
            
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                self.errors.append(f"Job '{job_name}' must be a dictionary")
                continue
                
            # Check required job fields
            if 'runs-on' not in job_config:
                self.errors.append(f"Job '{job_name}' missing 'runs-on'")
                
            # Check steps
            if 'steps' in job_config:
                steps = job_config['steps']
                if not isinstance(steps, list):
                    self.errors.append(f"Job '{job_name}' steps must be a list")
                elif len(steps) == 0:
                    self.warnings.append(f"Job '{job_name}' has no steps")
                    
    def _check_common_issues(self):
        """Check for common workflow issues."""
        
        # Check for quoted "on" field (GitHub Actions requires it unquoted)
        if re.search(r'^"on":', self.content, re.MULTILINE):
            self.errors.append('"on" field must not be quoted - GitHub Actions requires: on:')
            
        # Check for matrix references in outputs section
        if re.search(r'outputs:.*\$\{\{\s*matrix\.', self.content):
            self.errors.append('Invalid matrix references in outputs - GitHub Actions does not allow ${{ matrix.* }} in job outputs')
            
        # Check for absolute paths
        if re.search(r'path:\s*[\'"]?/[^$\s\'"]', self.content):
            self.warnings.append("Absolute paths detected - use relative or variable paths")
            
        # Check for PROJECT_DIR without definition
        if '$PROJECT_DIR' in self.content or '${PROJECT_DIR}' in self.content:
            if 'PROJECT_DIR=' not in self.content:
                self.warnings.append("PROJECT_DIR used but not defined")
                
        # Check MCP configuration
        if '--mcp-config' in self.content:
            if '.claude/mcp-kamuicode.json' not in self.content:
                self.warnings.append("Non-standard MCP config file")
                
        # Check for Write tool with MCP image generation
        if 'mcp__t2i' in self.content:
            lines = self.content.split('\n')
            for i, line in enumerate(lines):
                if 'mcp__t2i' in line:
                    # Check nearby lines for Write tool
                    context = '\n'.join(lines[max(0,i-2):min(len(lines),i+3)])
                    if 'Write' not in context:
                        self.warnings.append(f"Line {i+1}: Image generation without Write tool")
                        
    def _generate_report(self):
        """Generate validation report."""
        report = {
            'workflow': str(self.workflow_path),
            'valid': len(self.errors) == 0,
            'can_execute': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'fixes_applied': self.fixes_applied
        }
        
        # Save report
        report_path = self.workflow_path.parent / 'validation_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Print summary
        print("\n" + "="*50)
        print("📊 Validation Report")
        print("="*50)
        
        if self.fixes_applied:
            print(f"\n✅ Fixes Applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
                
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
                
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
                
        if not self.errors and not self.warnings:
            print("\n✅ All checks passed!")
            
        print("\n" + "="*50)
        print(f"Result: {'✅ VALID' if len(self.errors) == 0 else '❌ INVALID'}")
        print(f"Report saved to: {report_path}")
        print("="*50)
        
        return report


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python workflow-validator.py <workflow.yml> [--auto-fix]")
        sys.exit(1)
        
    workflow_path = sys.argv[1]
    auto_fix = '--auto-fix' in sys.argv
    
    # Validate workflow
    validator = WorkflowValidator(workflow_path)
    # Read file first
    if not validator._read_file():
        print("Failed to read workflow file")
        sys.exit(1)
    
    is_valid = validator.validate_and_fix() if auto_fix else validator._validate_content()
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
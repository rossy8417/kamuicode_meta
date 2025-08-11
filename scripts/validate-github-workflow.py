#!/usr/bin/env python3
"""
GitHub Actions Workflow Validation Script
Performs comprehensive validation to prevent common workflow failures.
"""

import sys
import yaml
import re
import json
from pathlib import Path

class WorkflowValidator:
    def __init__(self, workflow_path):
        self.workflow_path = Path(workflow_path)
        self.errors = []
        self.warnings = []
        self.content = None
        self.yaml_data = None
        
    def validate(self):
        """Run all validation checks."""
        print(f"🔍 Validating workflow: {self.workflow_path}")
        
        # Read file content
        if not self._read_file():
            return False
            
        # Run validation checks
        checks = [
            self._check_yaml_syntax,
            self._check_forbidden_patterns,
            self._check_required_structure,
            self._check_trigger_configuration,
            self._check_path_patterns,
            self._check_mcp_configuration,
            self._check_artifact_handling
        ]
        
        all_passed = True
        for check in checks:
            if not check():
                all_passed = False
                
        # Report results
        self._report_results()
        
        return all_passed and len(self.errors) == 0
        
    def _read_file(self):
        """Read workflow file content."""
        try:
            with open(self.workflow_path, 'r') as f:
                self.content = f.read()
            return True
        except Exception as e:
            self.errors.append(f"Failed to read file: {e}")
            return False
            
    def _check_yaml_syntax(self):
        """Check YAML syntax validity."""
        print("  ✓ Checking YAML syntax...")
        try:
            self.yaml_data = yaml.safe_load(self.content)
            if not self.yaml_data:
                self.errors.append("YAML file is empty or invalid")
                return False
            return True
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error: {e}")
            # Try to extract line number from error
            if hasattr(e, 'problem_mark'):
                line = e.problem_mark.line + 1
                self.errors.append(f"  Error at line {line}")
            return False
            
    def _check_forbidden_patterns(self):
        """Check for forbidden patterns that cause GitHub Actions failures."""
        print("  ✓ Checking for forbidden patterns...")
        
        forbidden_patterns = [
            {
                'pattern': r'<<\s*[\'"]?EOF',
                'name': 'HEREDOC',
                'fix': 'Use echo commands instead of HEREDOC'
            },
            {
                'pattern': r'uses:\s*[\'"]?\./[^\'"\s]+',
                'name': 'Local uses reference',
                'fix': 'Inline the implementation instead of using local references'
            },
            {
                'pattern': r'^\s*cat\s+>.*<<',
                'name': 'Cat with HEREDOC',
                'fix': 'Use echo commands for line-by-line generation'
            },
            {
                'pattern': r'python3\s+-c\s+"[^"]*\n[^"]*"',
                'name': 'Multi-line Python',
                'fix': 'Use single-line Python commands or script files'
            }
        ]
        
        found_issues = False
        for pattern_info in forbidden_patterns:
            pattern = pattern_info['pattern']
            matches = re.finditer(pattern, self.content, re.MULTILINE)
            for match in matches:
                line_num = self.content[:match.start()].count('\n') + 1
                self.errors.append(
                    f"Forbidden pattern '{pattern_info['name']}' at line {line_num}: {pattern_info['fix']}"
                )
                found_issues = True
                
        return not found_issues
        
    def _check_required_structure(self):
        """Check for required GitHub Actions structure."""
        print("  ✓ Checking required structure...")
        
        if not self.yaml_data:
            return False
            
        required_fields = ['name', 'on', 'jobs']
        missing_fields = []
        
        for field in required_fields:
            if field not in self.yaml_data:
                missing_fields.append(field)
                
        if missing_fields:
            self.errors.append(f"Missing required fields: {', '.join(missing_fields)}")
            return False
            
        # Check jobs structure
        jobs = self.yaml_data.get('jobs', {})
        if not jobs:
            self.errors.append("No jobs defined")
            return False
            
        for job_name, job_config in jobs.items():
            if not isinstance(job_config, dict):
                self.errors.append(f"Job '{job_name}' has invalid configuration")
                continue
                
            if 'runs-on' not in job_config:
                self.errors.append(f"Job '{job_name}' missing 'runs-on'")
                
            if 'steps' not in job_config:
                self.warnings.append(f"Job '{job_name}' has no steps")
                
        return len([e for e in self.errors if 'Job' in e]) == 0
        
    def _check_trigger_configuration(self):
        """Check workflow trigger configuration."""
        print("  ✓ Checking trigger configuration...")
        
        if not self.yaml_data:
            return False
            
        on_config = self.yaml_data.get('on', {})
        
        # Check for workflow_dispatch
        if 'workflow_dispatch' in on_config:
            dispatch_config = on_config['workflow_dispatch']
            if isinstance(dispatch_config, dict) and 'inputs' in dispatch_config:
                inputs = dispatch_config['inputs']
                if not isinstance(inputs, dict):
                    self.errors.append("workflow_dispatch inputs must be a dictionary")
                    return False
                    
                # Validate each input
                for input_name, input_config in inputs.items():
                    if not isinstance(input_config, dict):
                        self.errors.append(f"Input '{input_name}' has invalid configuration")
                        continue
                        
                    # Check for type field
                    if 'type' in input_config:
                        valid_types = ['string', 'choice', 'boolean', 'environment']
                        if input_config['type'] not in valid_types:
                            self.warnings.append(
                                f"Input '{input_name}' has invalid type: {input_config['type']}"
                            )
                            
        return True
        
    def _check_path_patterns(self):
        """Check for problematic path patterns."""
        print("  ✓ Checking path patterns...")
        
        # Check for absolute paths
        absolute_path_pattern = r'(?:path|file):\s*[\'"]?/[^$\s\'"][^\s\'"]*'
        matches = re.finditer(absolute_path_pattern, self.content)
        
        for match in matches:
            line_num = self.content[:match.start()].count('\n') + 1
            self.warnings.append(f"Absolute path detected at line {line_num}: Use relative or variable paths")
            
        # Check for PROJECT_DIR usage
        if '$PROJECT_DIR' in self.content or '${PROJECT_DIR}' in self.content:
            if 'PROJECT_DIR=' not in self.content:
                self.warnings.append("PROJECT_DIR used but not defined")
                
        return True
        
    def _check_mcp_configuration(self):
        """Check MCP tool configuration."""
        print("  ✓ Checking MCP configuration...")
        
        if '--mcp-config' in self.content:
            # Check if config file is specified
            if '.claude/mcp-kamuicode.json' not in self.content:
                self.warnings.append("Non-standard MCP config file used")
                
            # Check for allowedTools
            mcp_pattern = r'--allowedTools\s+[\'"]([^\'"]*)[\'"]]'
            matches = re.finditer(mcp_pattern, self.content)
            
            for match in matches:
                tools = match.group(1)
                if 'Write' not in tools and 'mcp__t2i' in tools:
                    line_num = self.content[:match.start()].count('\n') + 1
                    self.warnings.append(
                        f"Line {line_num}: Image generation without Write tool - files may not be saved"
                    )
                    
        return True
        
    def _check_artifact_handling(self):
        """Check artifact upload/download patterns."""
        print("  ✓ Checking artifact handling...")
        
        upload_count = self.content.count('actions/upload-artifact@')
        download_count = self.content.count('actions/download-artifact@')
        
        if upload_count > 0 and download_count == 0:
            self.warnings.append("Artifacts uploaded but never downloaded - possible data sharing issue")
            
        # Check for merge-multiple in download
        if 'download-artifact@v4' in self.content and 'merge-multiple: true' in self.content:
            self.warnings.append("Using merge-multiple may cause file conflicts")
            
        return True
        
    def _report_results(self):
        """Report validation results."""
        print("\n📊 Validation Results:")
        print("=" * 50)
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  • {error}")
                
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
                
        if not self.errors and not self.warnings:
            print("\n✅ All validation checks passed!")
            
        print("\n" + "=" * 50)
        
    def get_validation_result(self):
        """Return validation result as dictionary."""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'can_execute': len(self.errors) == 0
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-github-workflow.py <workflow.yml>")
        sys.exit(1)
        
    workflow_path = sys.argv[1]
    validator = WorkflowValidator(workflow_path)
    
    is_valid = validator.validate()
    result = validator.get_validation_result()
    
    # Write result to JSON for integration
    result_file = Path(workflow_path).parent / 'validation_result.json'
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📝 Results saved to: {result_file}")
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
import re

# Read the log file
with open('/tmp/workflow-log.txt', 'r') as f:
    content = f.read()

# Find the workflow content section
match = re.search(r'Generated Workflow Content:\s*\n=+\s*\n(.*?)\n=+', content, re.DOTALL)
if match:
    workflow_content = match.group(1)
    
    # Clean up the log prefixes
    lines = workflow_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove the timestamp and log prefix
        clean_match = re.search(r'Z\s+(.*)$', line)
        if clean_match:
            cleaned_lines.append(clean_match.group(1))
    
    # Write the cleaned workflow
    with open('projects/meta-workflow-v10-analysis/generated-workflow-clean.yml', 'w') as f:
        f.write('\n'.join(cleaned_lines))
    
    print("✅ Workflow extracted successfully")
else:
    print("❌ Could not find workflow content")

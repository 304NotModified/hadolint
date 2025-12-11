#!/usr/bin/env python3
"""
Generate wiki pages from Hadolint rule source files with improved formatting.
"""
import os
import re
from pathlib import Path

def clean_message(message):
    """Clean up message text by removing escape characters and formatting."""
    if not message:
        return message
    # Remove backslash escapes for newlines and quotes
    message = message.replace('\\n', ' ')
    message = message.replace('\\      \\', ' ')
    message = message.replace('\\       \\', ' ')
    message = message.replace('\\', '')
    # Clean up multiple spaces
    message = re.sub(r'\s+', ' ', message)
    message = message.strip()
    return message

def extract_rule_info(file_path):
    """Extract rule code, severity, and message from a Haskell rule file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract code
    code_match = re.search(r'code = "([^"]+)"', content)
    code = code_match.group(1) if code_match else None
    
    # Extract severity
    severity_match = re.search(r'severity = (DL\w+)', content)
    severity_raw = severity_match.group(1) if severity_match else None
    
    # Map severity to readable form
    severity_map = {
        'DLErrorC': 'Error',
        'DLWarningC': 'Warning',
        'DLInfoC': 'Info',
        'DLStyleC': 'Style',
        'DLIgnoreC': 'Ignore'
    }
    severity = severity_map.get(severity_raw, severity_raw)
    
    # Extract message - try to find the complete message including multi-line
    message = None
    
    # First try simple single-line message
    message_match = re.search(r'message\s*=\s*"([^"]+)"', content)
    if message_match:
        message = message_match.group(1)
    else:
        # Try multi-line message pattern
        lines = content.split('\n')
        in_message = False
        message_parts = []
        
        for i, line in enumerate(lines):
            if 'message =' in line or 'message=' in line:
                in_message = True
                # Extract the part after =
                match = re.search(r'message\s*=\s*"(.+)', line)
                if match:
                    message_parts.append(match.group(1))
                continue
            
            if in_message:
                # Check if line has continuation
                if line.strip().startswith('"'):
                    # Remove leading quote and backslash
                    part = line.strip()
                    if part.startswith('"'):
                        part = part[1:]
                    if part.endswith('"'):
                        part = part[:-1]
                        message_parts.append(part)
                        break
                    message_parts.append(part)
                elif not line.strip().startswith('\\'):
                    break
        
        if message_parts:
            message = ' '.join(message_parts)
            # Clean up escape sequences
            message = clean_message(message)
    
    return {
        'code': code,
        'severity': severity,
        'message': message,
        'content': content
    }

def extract_readme_rules(readme_path):
    """Extract rule descriptions from README.md."""
    rules = {}
    try:
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Find all rule entries in README table
        pattern = r'\|\s*\[([^\]]+)\]\([^\)]+\)\s*\|\s*[^\|]+\|\s*([^\|]+)\|'
        matches = re.findall(pattern, content)
        
        for code, description in matches:
            code = code.strip()
            description = description.strip()
            rules[code] = description
    except Exception as e:
        print(f"Warning: Could not extract rules from README: {e}")
    
    return rules

def get_rule_examples(code, message, readme_desc):
    """Generate specific examples for each rule based on its code and message."""
    examples = {
        'bad': f'# Example that violates {code}',
        'good': f'# Example that follows {code}'
    }
    
    # Specific examples based on rule patterns
    if code == 'DL3000':
        examples['bad'] = 'WORKDIR relative/path'
        examples['good'] = 'WORKDIR /absolute/path'
    elif code == 'DL3001':
        examples['bad'] = 'RUN ssh user@host'
        examples['good'] = 'RUN echo "Use appropriate tools for containers"'
    elif code == 'DL3002':
        examples['bad'] = 'USER root'
        examples['good'] = 'USER nonrootuser'
    elif code == 'DL3003':
        examples['bad'] = 'RUN cd /tmp && command'
        examples['good'] = 'WORKDIR /tmp\nRUN command'
    elif code == 'DL3004':
        examples['bad'] = 'RUN sudo apt-get update'
        examples['good'] = 'RUN apt-get update'
    elif code == 'DL3006':
        examples['bad'] = 'FROM ubuntu'
        examples['good'] = 'FROM ubuntu:20.04'
    elif code == 'DL3007':
        examples['bad'] = 'FROM ubuntu:latest'
        examples['good'] = 'FROM ubuntu:20.04'
    elif code == 'DL3008':
        examples['bad'] = 'RUN apt-get install -y nginx'
        examples['good'] = 'RUN apt-get install -y nginx=1.18.0-0ubuntu1'
    elif code == 'DL3009':
        examples['bad'] = 'RUN apt-get update && apt-get install -y nginx'
        examples['good'] = 'RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*'
    elif code == 'DL3013':
        examples['bad'] = 'RUN pip install flask'
        examples['good'] = 'RUN pip install flask==2.0.1'
    elif code == 'DL3016':
        examples['bad'] = 'RUN npm install express'
        examples['good'] = 'RUN npm install express@4.17.1'
    elif code == 'DL3018':
        examples['bad'] = 'RUN apk add nginx'
        examples['good'] = 'RUN apk add nginx=1.20.1-r3'
    elif code == 'DL3020':
        examples['bad'] = 'ADD file.txt /app/'
        examples['good'] = 'COPY file.txt /app/'
    elif code == 'DL3025':
        examples['bad'] = 'CMD command arg1 arg2'
        examples['good'] = 'CMD ["command", "arg1", "arg2"]'
    
    return examples

def is_message_incomplete(message):
    """Check if a message is incomplete or truncated.
    
    Returns True if the message appears incomplete, which can happen when:
    - The message is empty or very short (less than 10 characters)
    - The message ends with special characters like backtick or angle bracket,
      indicating Haskell string concatenation that wasn't fully parsed
    """
    MIN_MESSAGE_LENGTH = 10
    INCOMPLETE_INDICATORS = ('`', '<')
    
    if not message or len(message) < MIN_MESSAGE_LENGTH:
        return True
    
    return any(message.endswith(indicator) for indicator in INCOMPLETE_INDICATORS)

def generate_wiki_page(rule_info, readme_data):
    """Generate markdown content for a wiki page."""
    code = rule_info['code']
    severity = rule_info['severity']
    message = rule_info['message']
    
    # Clean the message first
    if message:
        message = clean_message(message)
    
    # Try to get the message from README if incomplete in source
    if is_message_incomplete(message) and readme_data and code in readme_data:
        message = readme_data[code]
    
    if not message:
        message = f"Rule {code}"
    
    # Get examples
    examples = get_rule_examples(code, message, readme_data.get(code, ''))
    
    wiki_content = f"""# {code}

**Severity:** {severity}

## Description

{message}

## Rationale

This rule helps ensure Dockerfile best practices and avoid common mistakes that can lead to:
- Security vulnerabilities
- Larger image sizes
- Unpredictable behavior
- Maintenance difficulties

## Examples

### Bad

```dockerfile
{examples['bad']}
```

### Good

```dockerfile
{examples['good']}
```

## Configuration

To ignore this rule, add it to your `.hadolint.yaml`:

```yaml
ignored:
  - {code}
```

Or use inline ignoring:

```dockerfile
# hadolint ignore={code}
FROM image
```

## See Also

- [Hadolint Rules](https://github.com/hadolint/hadolint#rules)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Main Hadolint Repository](https://github.com/hadolint/hadolint)
"""
    
    return wiki_content

def main():
    # Determine paths based on script location
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    src_dir = repo_root / 'src' / 'Hadolint' / 'Rule'
    wiki_dir = repo_root / 'wiki'
    readme_path = repo_root / 'README.md'
    
    # Create wiki directory if it doesn't exist
    wiki_dir.mkdir(exist_ok=True)
    
    # Extract rule descriptions from README
    readme_rules = extract_readme_rules(readme_path)
    
    # Get all rule files
    rule_files = sorted(src_dir.glob('DL*.hs'))
    
    rules_generated = []
    
    for rule_file in rule_files:
        print(f"Processing {rule_file.name}...")
        
        rule_info = extract_rule_info(rule_file)
        code = rule_info['code']
        
        if code:
            wiki_content = generate_wiki_page(rule_info, readme_rules)
            wiki_file = wiki_dir / f"{code}.md"
            
            with open(wiki_file, 'w') as f:
                f.write(wiki_content)
            
            # Get message with same logic as wiki page generation
            message = rule_info['message']
            if message:
                message = clean_message(message)
            
            # Use README message if incomplete
            if is_message_incomplete(message) and code in readme_rules:
                message = readme_rules[code]
            
            if not message:
                message = f"Rule {code}"
            
            rules_generated.append({
                'code': code,
                'severity': rule_info['severity'],
                'message': message
            })
            print(f"  Created {wiki_file.name}")
    
    # Generate Home page
    home_content = """# Hadolint Rules Wiki

Welcome to the Hadolint rules documentation. This wiki provides detailed information about each linting rule.

## About Hadolint

Hadolint is a Dockerfile linter that helps you build best practice Docker images. It parses the Dockerfile into an AST and performs rules on top of the AST.

## Quick Links

- [Main Repository](https://github.com/hadolint/hadolint)
- [Installation Guide](https://github.com/hadolint/hadolint#install)
- [Configuration Options](https://github.com/hadolint/hadolint#configure)
- [Integration Guide](https://github.com/hadolint/hadolint/blob/master/docs/INTEGRATION.md)

## Rules by Category

### DL1xxx - Ignore Rules

These rules relate to the use of ignore pragmas.

"""
    
    # Group rules by category
    dl1_rules = [r for r in rules_generated if r['code'].startswith('DL1')]
    dl3_rules = [r for r in rules_generated if r['code'].startswith('DL3')]
    dl4_rules = [r for r in rules_generated if r['code'].startswith('DL4')]
    
    for rule in dl1_rules:
        home_content += f"- **[{rule['code']}]({rule['code']})** ({rule['severity']}): {rule['message']}\n"
    
    home_content += "\n### DL3xxx - Dockerfile Rules\n\n"
    home_content += "These rules help enforce best practices when writing Dockerfiles.\n\n"
    
    for rule in dl3_rules:
        home_content += f"- **[{rule['code']}]({rule['code']})** ({rule['severity']}): {rule['message']}\n"
    
    home_content += "\n### DL4xxx - Maintainer Rules\n\n"
    home_content += "These rules relate to MAINTAINER instructions and deprecated syntax.\n\n"
    
    for rule in dl4_rules:
        home_content += f"- **[{rule['code']}]({rule['code']})** ({rule['severity']}): {rule['message']}\n"
    
    home_content += """
## Severity Levels

- **Error**: Critical issues that should always be fixed
- **Warning**: Important issues that should typically be addressed
- **Info**: Informational suggestions for improvement
- **Style**: Code style recommendations

## Configuration

See the [configuration documentation](https://github.com/hadolint/hadolint#configure) for information on how to:
- Ignore specific rules globally or inline
- Override rule severities
- Set failure thresholds
- Configure trusted registries

## Contributing

If you find issues or want to improve these documentation pages, please contribute to the [Hadolint project](https://github.com/hadolint/hadolint).

## License

Hadolint is licensed under GPL-3.0. See the [LICENSE](https://github.com/hadolint/hadolint/blob/master/LICENSE) file for details.
"""
    
    home_file = wiki_dir / "Home.md"
    with open(home_file, 'w') as f:
        f.write(home_content)
    
    print(f"\n✓ Generated {len(rules_generated)} wiki pages")
    print(f"✓ Created Home.md with index of all rules")
    print(f"\nRules by category:")
    print(f"  - DL1xxx (Ignore): {len(dl1_rules)}")
    print(f"  - DL3xxx (Dockerfile): {len(dl3_rules)}")
    print(f"  - DL4xxx (Maintainer): {len(dl4_rules)}")
    print(f"\nWiki pages are ready in: {wiki_dir}")

if __name__ == '__main__':
    main()

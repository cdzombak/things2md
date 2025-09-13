# things2md

Export Things 3 projects and all their tasks to well-formatted Markdown. Captures project details, task information, notes, tags, due dates, and completion status with proper formatting.

## Requirements

- macOS with Things 3 installed
- Python 3 (built into modern macOS)

## Installation

```bash
# Download the single file
curl -O https://raw.githubusercontent.com/your-repo/things2md.py
chmod +x things2md.py
```

## Usage

```bash
# Export to stdout
./things2md.py "My Project Name"

# Export to file
./things2md.py "My Project Name" > project.md

# Export and copy to clipboard
./things2md.py "My Project Name" | pbcopy

# Show help
./things2md.py --help
```



## Output Format

The generated Markdown follows this structure:

```markdown
# Project Name
**Tags:** tag1, tag2
**Due Date:** 2024-12-31

## Project Notes
Project description and notes go here.

## Tasks

- Task Name *(tag1, tag2)*
  Task notes with proper indentation
  Multiple lines are handled correctly
  
  Even with empty lines between

- Another Task
  More notes here
```


## Examples

```bash
# Export multiple projects
for project in "Project A" "Project B" "Project C"; do
    ./things2md.py "$project" > "${project// /_}.md"
done

# Convert to PDF using pandoc
./things2md.py "Project Name" | pandoc -o project.pdf

# View in your markdown editor
./things2md.py "Project Name" | open -f -a "Typora"
```

## Troubleshooting

**Project Not Found**: Check the exact project name in Things 3.

**Permission Errors**: Allow access when macOS prompts for Things 3 permissions.

**Empty Output**: Ensure the project contains tasks.
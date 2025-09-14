# things2md

Export [Things](https://culturedcode.com/things/) projects and all their tasks to well-formatted Markdown. Captures project details, task information, notes, tags, due dates, and completion status with proper formatting.

## Requirements

- macOS with Things 3 installed
- Python 3 (built into modern macOS)

## Installation

### macOS via Homebrew

```shell
brew install cdzombak/oss/things2md
```

### Manual download from this repo

```bash
curl -O https://raw.githubusercontent.com/cdzombak/things2md/things2md.py
chmod +x things2md.py
```

## Usage

```bash
# Export to stdout
./things2md "My Project Name"

# Export to file
./things2md "My Project Name" > project.md

# Export and copy to clipboard
./things2md "My Project Name" | pbcopy

# Show help
./things2md --help
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
    ./things2md "$project" > "${project// /_}.md"
done

# Convert to PDF using pandoc
./things2md "Project Name" | pandoc -o project.pdf

# View in your markdown editor
./things2md "Project Name" | open -f -a "Typora"
```

## Troubleshooting

**Project Not Found**: Check the exact project name in Things 3.

**Permission Errors**: Allow access when macOS prompts for Things 3 permissions.

**Empty Output**: Ensure the project contains tasks.

## License

GNU GPL v3; see [LICENSE](LICENSE) in this repo.

## Author

[Chris Dzombak](https://www.dzombak.com) ([GitHub: @cdzombak](https://www.github.com/cdzombak))

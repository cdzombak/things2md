#!/usr/bin/env python3
"""
things2md - Export Things 3 projects to Markdown
Single-file deployment with embedded AppleScript.
"""

import sys
import subprocess
import tempfile
import os

__THINGS2MD_VERSION__ = "<dev>"


# Embedded AppleScript
APPLESCRIPT_CODE = '''
-- Things 3 to Markdown Export Script
-- Usage: osascript things2md.applescript "Project Name" --stdout

on run argv
	try
		-- Validate Things 3 is available
		if not isThingsAvailable() then
			error "Things 3 is not running or not installed. Please open Things 3 and try again."
		end if

		-- Require project name argument
		if (count of argv) < 1 then
			error "Project name is required."
		end if

		set projectName to item 1 of argv

		-- Validate project name is not empty
		if projectName is "" then
			error "Project name cannot be empty."
		end if

		set markdownContent to exportProjectToMarkdown(projectName)

		-- Always output to stdout (via log which goes to stderr)
		log markdownContent

	on error errMsg
		log "Error: " & errMsg
	end try
end run

-- Main export function
on exportProjectToMarkdown(projectName)
	tell application "Things3"
		set targetProject to project projectName

		set markdownContent to ""

		-- Project header
		set markdownContent to markdownContent & "# " & (name of targetProject) & "\\n\\n"

		-- Project tags
		set projectTags to tag names of targetProject
		if projectTags is not "" then
			set markdownContent to markdownContent & "**Tags:** " & projectTags & "\\n\\n"
		end if

		-- Project due date
		set projectDueDate to due date of targetProject
		if projectDueDate is not missing value then
			set markdownContent to markdownContent & "**Due Date:** " & formatDate(projectDueDate) & "\\n\\n"
		end if

		-- Project notes
		set projectNotes to notes of targetProject
		if projectNotes is not "" then
			set markdownContent to markdownContent & "## Project Notes\\n\\n" & projectNotes & "\\n\\n"
		end if

		-- Tasks section
		set markdownContent to markdownContent & "## Tasks\\n\\n"

		-- Get all to-dos in the project
		try
			set projectTodos to to dos of targetProject

			repeat with currentTodo in projectTodos
				try
					set taskName to name of currentTodo

					-- Get task tags if they exist
					try
						set taskTags to tag names of currentTodo
						if taskTags is not "" and taskTags is not missing value then
							set markdownContent to markdownContent & "- " & taskName & " *(" & taskTags & ")*\\n"
						else
							set markdownContent to markdownContent & "- " & taskName & "\\n"
						end if
					on error
						-- If tags can't be read, just use the task name
						set markdownContent to markdownContent & "- " & taskName & "\\n"
					end try

					-- Get task notes if they exist
					try
						set taskNotes to notes of currentTodo
						if taskNotes is not "" and taskNotes is not missing value then
							-- Just add notes with initial indentation
							set markdownContent to markdownContent & "  " & taskNotes & "\\n"
						end if
					on error
						-- Skip notes if there's an error reading them
					end try

				on error
					set markdownContent to markdownContent & "- [Error reading task]\\n"
				end try
			end repeat
		on error
			set markdownContent to markdownContent & "\\nNo tasks found or error reading tasks\\n\\n"
		end try

		return markdownContent
	end tell
end exportProjectToMarkdown

-- Format individual task as markdown
on formatTaskAsMarkdown(currentTodo)
	tell application "Things3"
		try
			set taskContent to ""
			set taskName to name of currentTodo

			-- Just get basic task info for now
			set taskContent to taskContent & "### " & taskName & "\\n\\n"

			-- Try to get status
			try
				set taskStatus to status of currentTodo
				set taskContent to taskContent & "**Status:** " & taskStatus & "\\n"
			end try

			-- Try to get notes
			try
				set taskNotes to notes of currentTodo
				if taskNotes is not "" then
					set taskContent to taskContent & "\\n" & taskNotes & "\\n"
				end if
			end try

			-- Add spacing between tasks
			set taskContent to taskContent & "\\n---\\n\\n"

			return taskContent
		on error errMsg
			return "### Error processing task: " & errMsg & "\\n\\n---\\n\\n"
		end try
	end tell
end formatTaskAsMarkdown

-- Format date for display
on formatDate(dateValue)
	if dateValue is missing value then
		return ""
	end if

	try
		-- Extract date components for better formatting
		set dateString to dateValue as string

		-- Try to format as YYYY-MM-DD
		set theYear to year of dateValue
		set theMonth to month of dateValue as integer
		set theDay to day of dateValue

		-- Pad single digits with zeros
		set monthStr to theMonth as string
		if theMonth < 10 then set monthStr to "0" & monthStr

		set dayStr to theDay as string
		if theDay < 10 then set dayStr to "0" & dayStr

		return (theYear as string) & "-" & monthStr & "-" & dayStr
	on error
		-- Fallback to default string representation
		return dateValue as string
	end try
end formatDate

-- Check if Things 3 is available and running
on isThingsAvailable()
	try
		tell application "System Events"
			set thingsRunning to (name of processes) contains "Things3"
		end tell

		if not thingsRunning then
			-- Try to check if Things is installed
			try
				tell application "Finder"
					set thingsExists to exists application file id "com.culturedcode.ThingsMac"
				end tell
				return thingsExists
			on error
				return false
			end try
		end if

		return true
	on error
		return false
	end try
end isThingsAvailable
'''


def show_usage():
    """Display usage information."""
    script_name = os.path.basename(sys.argv[0])
    print(f"""{script_name.replace('.py', '')}

Export Things 3 projects to Markdown format.

Usage:
  {script_name} "Project Name"                    # Export to stdout
  {script_name} --help                           # Show help

Examples:
  {script_name} "Work Projects" > project.md
  {script_name} "Home Renovation" > renovation.md
  {script_name} "Meeting Notes" | pbcopy
""")


def fix_note_indentation(text):
    """Fix multiline note indentation in the exported text."""
    lines = text.split('\n')
    result = []
    in_note = False

    for line in lines:
        if line.startswith('- ') or line.startswith('#'):
            in_note = False
            result.append(line)
        elif line.startswith('  '):
            in_note = True
            result.append(line)
        elif line == '':
            result.append(line)  # Keep empty lines as-is, don't change note state
        elif in_note and not line.startswith(' '):
            result.append('  ' + line)
        else:
            in_note = False
            result.append(line)

    return '\n'.join(result)


def main():
    """Main function."""
    if len(sys.argv) == 1 or sys.argv[1] in ['--help', '-h']:
        show_usage()
        sys.exit(0)

    if sys.argv[1] in ['--version', '-v']:
        print(f"{os.path.basename(sys.argv[0])} version {__THINGS2MD_VERSION__}")
        sys.exit(0)

    # Get the project name
    if len(sys.argv) < 2:
        print("Error: Project name is required", file=sys.stderr)
        show_usage()
        sys.exit(1)

    project_name = sys.argv[1]

    try:
        # Create a temporary file with the embedded AppleScript
        with tempfile.NamedTemporaryFile(mode='w', suffix='.applescript', delete=False) as f:
            f.write(APPLESCRIPT_CODE)
            temp_script_path = f.name

        try:
            # Run the AppleScript
            result = subprocess.run([
                'osascript', temp_script_path, project_name, '--stdout'
            ], capture_output=True, text=True, check=True)

            # The AppleScript outputs to stderr, so get the output from there
            raw_output = result.stderr if result.stderr else result.stdout

            # Fix the note indentation
            fixed_output = fix_note_indentation(raw_output)

            # Output to stdout
            print(fixed_output)

        finally:
            # Clean up the temporary file
            os.unlink(temp_script_path)

    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

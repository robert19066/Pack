

![logo](https://i.postimg.cc/7LMDYCL6/project-pack-logo.png)

Pack, is a Python-based "packlet" (workflow) manager that allows users to create, store, and execute custom shell command sequences with various execution modes and privilege configurations. The project provides both a CLI interface for creating packlets and an execution engine for running them.

Dev note: Trust me, it's really [![awesome](https://awesome.re/badge.svg)](https://awesome.re)

## Core Architecture

The codebase is organized around four main components:

### Main Components
- **`mainShell.py`**: The user-facing CLI application with a rich terminal interface including colored banners, menus, loading bars, and wizards for packlet creation and execution
- **`mainCompile.py`**: The core execution engine (`Main` class) that parses packlet files and executes shell commands with different execution strategies
- **`helper_functions.py`**: Parser utilities (`HelperFunctions` class) for extracting configuration from packlet files
- **`createFile.py`**: File creation utility for generating new packlet files with proper formatting

### Packlet File Format
Packlets are custom configuration files with specific extensions and structure:
- **`.paklt`**: Standard packlets (default execution mode - stops on errors)
- **`.fopak`**: Bulldozer packlets (continues execution despite errors)

**Packlet file structure:**
```
$type=<shell>          # Shell to use (bash, zsh, fish, etc.)
$excmeth:<method>      # Execution method (default/bulldozer)
$isudo=<true/false>    # Whether sudo privileges are required

<command1>
<command2>
...
---
```

### Execution Modes
- **Default Mode**: Stops execution immediately when any command fails
- **Bulldozer Mode**: Continues executing all commands even when some fail, providing a summary of failed commands at the end

## Common Development Tasks

### Running the Application
```bash
python mainShell.py
```

### Testing Packlet Execution
```bash
# Create a simple test packlet
echo -e '$type=bash\n$excmeth:default\n$isudo=false\n\necho "Hello World"\nls -la\n---' > test.paklt

# Test execution programmatically
python -c "
from mainCompile import Main
main = Main('test.paklt')
results = main.run(['test.paklt'])
print(results)
"
```

### Creating Packlets Programmatically
```bash
python -c "
import createFile
createFile.create_packlet_file('default', 'bash', False, ['echo \"test\"', 'pwd'], 'example.paklt')
"
```

## File Structure
```
/
├── mainShell.py          # Main CLI application with UI
├── mainCompile.py        # Core execution engine
├── helper_functions.py   # Packlet file parsers
├── createFile.py         # File creation utilities
├── packlets/             # Directory for storing packlets (created automatically)
└── __pycache__/          # Python bytecode cache
```

## Development Notes

### Error Handling
The codebase implements two distinct error handling strategies:
- **Default execution**: Uses `subprocess.run()` with `check=True` to raise exceptions on command failure
- **Bulldozer execution**: Uses `subprocess.run()` with `check=False` and manually tracks failed commands

### UI Framework
The CLI uses ANSI color codes extensively through the `Colors` class for terminal styling. Key UI components include:
- Dynamic menu boxes with perfect alignment
- Progress indicators (loading bars and spinners)
- Step-by-step wizards for packlet creation
- Colored success/error/warning messages

### Dependencies
- **pyparsing**: Used in helper_functions.py (imported but not actively used in current implementation)
- **subprocess**: Core dependency for shell command execution
- **os**: For file system operations and screen clearing
- **sys**: For application exit handling
- **time**: For UI animations and delays
- **random**: For randomized loading animations

### Packlet Storage
All created packlets are stored in the `packlets/` directory, which is automatically created if it doesn't exist. The directory structure is flat with no subdirectories.

## Security Considerations
- Sudo execution is configurable per packlet via the `$isudo` parameter
- Commands are executed through shell subprocess calls, so standard shell injection precautions apply
- Bulldozer mode can potentially mask security-relevant command failures

# Generous people ❤️

...nothing here,yet!

## Credits

- robert19066 -> Main developer
- (Your name could be here! The first step is to get in the generous people section!)

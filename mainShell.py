from mainCompile import Main
import time
import random
import createFile
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

# ANSI Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    PURPLE = '\033[35m'
    ORANGE = '\033[38;5;208m'
    WHITE = '\033[97m'

def print_banner():
    banner_width = 67
    title = "✨ The Ultimate Packlet Manager ✨"
    title_padding = (banner_width - len(title)) // 2
    
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔{'═' * banner_width}╗
║{' ' * banner_width}║
║  ██████╗  █████╗  ██████╗██╗  ██╗    ██╗   ██╗ ██╗{' ' * (banner_width - 59)}║
║  ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝    ██║   ██║███║{' ' * (banner_width - 59)}║
║  ██████╔╝███████║██║     █████╔╝     ██║   ██║╚██║{' ' * (banner_width - 59)}║
║  ██╔═══╝ ██╔══██║██║     ██╔═██╗     ╚██╗ ██╔╝ ██║{' ' * (banner_width - 59)}║
║  ██║     ██║  ██║╚██████╗██║  ██╗     ╚████╔╝  ██║{' ' * (banner_width - 59)}║
║  ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝      ╚═══╝   ╚═╝{' ' * (banner_width - 59)}║
║{' ' * banner_width}║
║{' ' * title_padding}{Colors.YELLOW}{title}{Colors.CYAN}{' ' * (banner_width - title_padding - len(title))}║
╚{'═' * banner_width}╝
{Colors.RESET}"""
    print(banner)

def print_loading_bar(text, duration=2):
    """Animated loading bar"""
    print(f"\n{Colors.YELLOW}{text}{Colors.RESET}")
    bar_length = 40
    for i in range(bar_length + 1):
        time.sleep(duration / bar_length)
        percent = (i / bar_length) * 100
        filled = '█' * i
        empty = '░' * (bar_length - i)
        print(f"\r{Colors.GREEN}[{filled}{empty}] {percent:.1f}%{Colors.RESET}", end='', flush=True)
    print()

def print_spinner(text, duration=1):
    """Animated spinner"""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    print(f"\n{Colors.PURPLE}{text}{Colors.RESET} ", end='')
    while time.time() < end_time:
        print(f"\r{Colors.PURPLE}{text}{Colors.RESET} {Colors.CYAN}{spinner_chars[i % len(spinner_chars)]}{Colors.RESET}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{Colors.PURPLE}{text}{Colors.RESET} {Colors.GREEN}✓{Colors.RESET}")

def create_menu_box(title, items, width=62):
    """Create a dynamic menu box with perfect alignment"""
    # Create top border
    top_border = f"{Colors.BOLD}{Colors.BLUE}╭─ {title} {'─' * (width - len(title) - 4)}╮{Colors.RESET}"
    bottom_border = f"{Colors.BOLD}{Colors.BLUE}╰{'─' * width}╯{Colors.RESET}"
    
    # Create menu content
    menu_lines = [top_border]
    menu_lines.append(f"{Colors.BLUE}│{' ' * width}{Colors.BLUE}│{Colors.RESET}")
    
    for item in items:
        # Remove ANSI codes for length calculation
        import re
        clean_icon_text = re.sub(r'\x1b\[[0-9;]*m', '', item['icon_text'])
        clean_description = re.sub(r'\x1b\[[0-9;]*m', '', item['description'])
        
        # Calculate padding for perfect alignment
        content_padding = width - len(clean_icon_text) - 2
        line = f"{Colors.BLUE}│{Colors.RESET}  {item['icon_text']}{' ' * content_padding}{Colors.BLUE}│{Colors.RESET}"
        menu_lines.append(line)
        
        # Add description line
        desc_padding = width - len(clean_description) - 6
        desc_line = f"{Colors.BLUE}│{Colors.RESET}      {item['description']}{' ' * desc_padding}{Colors.BLUE}│{Colors.RESET}"
        menu_lines.append(desc_line)
        
        # Add spacing
        menu_lines.append(f"{Colors.BLUE}│{' ' * width}{Colors.BLUE}│{Colors.RESET}")
    
    menu_lines.append(bottom_border)
    return '\n'.join(menu_lines)

def print_menu():
    """Display the main menu with dynamic spacing"""
    menu_items = [
        {
            'icon_text': f"{Colors.GREEN}🚀 1.{Colors.RESET} {Colors.BOLD}Run a packlet{Colors.RESET}",
            'description': "Execute your packlet(workflow) files with style"
        },
        {
            'icon_text': f"{Colors.YELLOW}📦 2.{Colors.RESET} {Colors.BOLD}Create a packlet{Colors.RESET}",
            'description': "Build new packlets(workflows) with the wizard"
        },
        {
            'icon_text': f"{Colors.RED}❌ 3.{Colors.RESET} {Colors.BOLD}Exit{Colors.RESET}",
            'description': "Quit the application"
        }
    ]
    
    menu = create_menu_box("Main Menu", menu_items)
    print(f"\n{menu}\n")

def get_input(prompt, color=Colors.CYAN):
    """Enhanced input function with colors"""
    return input(f"{color}➤ {prompt}{Colors.RESET}")

def print_success(message):
    print(f"\n{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message):
    print(f"\n{Colors.RED}❌ {message}{Colors.RESET}")

def print_info(message):
    print(f"\n{Colors.BLUE}ℹ️  {message}{Colors.RESET}")

def create_step_header(step_num, total_steps, title, width=50):
    """Create a dynamic step header with progress indicator"""
    progress = f"Step {step_num}/{total_steps}"
    header = f"{Colors.YELLOW}📝 {progress}: {title}{Colors.RESET}"
    border = f"{Colors.BLUE}{'─' * width}{Colors.RESET}"
    return f"\n{header}\n{border}"

def print_warning(message):
   print(f"\\n{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def create_info_box(title, content_dict, width=60):
    """Create a dynamic info box with perfect alignment"""
    top_border = f"{Colors.BOLD}{Colors.GREEN}╔{'═' * (width + 2)}╗{Colors.RESET}"
    bottom_border = f"{Colors.BOLD}{Colors.GREEN}╚{'═' * (width + 2)}╝{Colors.RESET}"
    
    lines = [top_border]
    
    # Title line
    title_padding = (width - len(title)) // 2
    title_line = f"{Colors.BOLD}{Colors.GREEN}║{' ' * title_padding}{Colors.WHITE}{title}{Colors.GREEN}{' ' * (width - title_padding - len(title) + 2)}║{Colors.RESET}"
    lines.append(title_line)
    
    # Empty line
    lines.append(f"{Colors.GREEN}║{' ' * (width + 2)}║{Colors.RESET}")
    
    # Content lines
    for key, value in content_dict.items():
        content = f"  {key}: {value}"
        padding = width - len(content)
        content_line = f"{Colors.GREEN}║{Colors.RESET} {content}{' ' * padding} {Colors.GREEN}║{Colors.RESET}"
        lines.append(content_line)
    
    # Empty line
    lines.append(f"{Colors.GREEN}║{' ' * (width + 2)}║{Colors.RESET}")
    
    # Footer
    footer_text = "Ready to execute with Pack V1! 🚀"
    footer_padding = (width - len(footer_text)) // 2
    footer_line = f"{Colors.GREEN}║{' ' * footer_padding}{Colors.BOLD}{Colors.YELLOW}{footer_text}{Colors.GREEN}{' ' * (width - footer_padding - len(footer_text) + 2)}║{Colors.RESET}"
    lines.append(footer_line)
    
    lines.append(bottom_border)
    return '\n'.join(lines)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_packlet():
    """Enhanced packlet runner"""
    header_box = create_menu_box("Packlet Runner", [], 40)
    print(f"\n{header_box}")
    
    packlet_path = get_input("Enter the path to the packlet: ", Colors.GREEN)
    
    print_spinner("Loading packlet configuration...", 1)
    
    try:
        if packlet_path.endswith(".orgc"):
            with open(packlet_path, 'r') as f:
                packlet_paths = [line.strip() for line in f if line.strip()]
        else:
            packlet_paths = [packlet_path]
        
        print_info(f"Found {len(packlet_paths)} packlet(s) to execute")
        
        print_loading_bar("Initializing execution environment...", 2)
        
        main = Main(packlet_paths[0])
        results = main.run(packlet_paths)
        
        # Create results box
        results_width = 50
        print(f"\n{Colors.BOLD}{Colors.GREEN}╭─ Execution Results {'─' * (results_width - 20)}╮{Colors.RESET}")
        
        for path, status in results:
            path_display = path if len(path) <= 30 else f"...{path[-27:]}"
            if "success" in status.lower() or "completed" in status.lower():
                content = f"✅ {path_display}: {status}"
                padding = results_width - len(f"✅ {path_display}: {status}")
                print(f"{Colors.GREEN}│{Colors.RESET} {content}{' ' * max(0, padding - 1)} {Colors.GREEN}│{Colors.RESET}")
            else:
                content = f"❌ {path_display}: {status}"  
                padding = results_width - len(f"❌ {path_display}: {status}")
                print(f"{Colors.GREEN}│{Colors.RESET} {content}{' ' * max(0, padding - 1)} {Colors.GREEN}│{Colors.RESET}")
        
        print(f"{Colors.BOLD}{Colors.GREEN}╰{'─' * results_width}╯{Colors.RESET}")
                
    except FileNotFoundError:
        print_error("Packlet file not found!")
    except Exception as e:
        print_error(f"Error running packlet: {str(e)}")

def create_packlet():
    """Enhanced packlet creator with wizard interface"""
    wizard_header = create_menu_box("Packlet Creation Wizard", [], 50)
    print(f"\n{wizard_header}")
    
    wizard_banner = f"""
{Colors.PURPLE}    🧙‍♂️ Welcome to the Packlet Creator Wizard! 🧙‍♂️
    
{Colors.CYAN}Follow the steps below to create your custom packlet.
Each step is important for the final configuration.{Colors.RESET}
    """
    print(wizard_banner)
    
    total_steps = 5
    
    # Step 1: Name
    print(create_step_header(1, total_steps, "Packlet Identity"))
    name = get_input("Enter the name of your packlet: ", Colors.GREEN).strip()
    if not name:
        print_warning("Using default name: 'MyPacklet'")
        name = "MyPacklet"
    
    # Step 2: Execution Method
    print(create_step_header(2, total_steps, "Execution Method"))
    print(f"{Colors.CYAN}Available methods:")
    print(f"  • {Colors.GREEN}bulldozer{Colors.CYAN}: Bulldozer execution: The execution won't be interrupted by errors (.fopak)")
    print(f"  • {Colors.BLUE}default{Colors.CYAN}: Standard execution: The execution will be interrupted by errors (.paklt){Colors.RESET}")
    
    execMeth = get_input("Choose execution method (bulldozer/default): ", Colors.GREEN).strip().lower()
    
    if execMeth == "bulldozer":
        extension = ".fopak"
        print_success("Selected: Bulldozer mode 🚜")
    elif execMeth == "default":
        extension = ".paklt" 
        print_success("Selected: Default mode 📦")
    else:
        print_warning("Invalid method. Defaulting to 'default'")
        execMeth = "default"
        extension = ".paklt"
    
    # Step 3: Shell
    print(create_step_header(3, total_steps, "Shell Configuration"))
    print(f"{Colors.CYAN}Popular shells: bash, zsh, fish, sh, dash{Colors.RESET}")
    shell = get_input("Enter shell to use: ", Colors.GREEN).strip()
    if not shell:
        shell = "bash"
        print_warning("Using default shell: bash")
    
    # Step 4: Sudo
    print(create_step_header(4, total_steps, "Privileges"))
    sudo_input = get_input("Require sudo privileges? (true/false): ", Colors.GREEN).strip().lower()
    isudo = sudo_input == "true"
    
    if isudo:
        print_warning("⚠️  Sudo privileges enabled - use with caution!")
    else:
        print_info("Running with standard user privileges")
    
    # Step 5: Commands
    print(create_step_header(5, total_steps, "Command Configuration"))
    try:
        number_of_cmds = int(get_input("How many commands will there be? ", Colors.GREEN).strip())
    except ValueError:
        print_error("Invalid number. Setting to 1 command.")
        number_of_cmds = 1
    
    cmds = []
    print(f"\n{Colors.CYAN}Enter your commands (press Enter after each):{Colors.RESET}")
    
    for i in range(number_of_cmds):
        cmd = get_input(f"Command #{i + 1}: ", Colors.PURPLE).strip()
        cmds.append(cmd)
        print(f"{Colors.GREEN}  ✓ Added: {cmd}{Colors.RESET}")
    
    # Creation process
    print(f"\n{Colors.BOLD}{Colors.PURPLE}🛠️  Creating Your Packlet...{Colors.RESET}")
    
    creation_steps = [
        "Validating configuration...",
        "Generating packlet structure...", 
        "Writing command sequences...",
        "Applying security settings...",
        "Finalizing packlet..."
    ]
    
    for step in creation_steps:
        print_spinner(step, random.uniform(0.8, 2.0))
    
    print_loading_bar("Saving to disk...", 2)
    
    try:
        filename = f"{name}{extension}"
        createFile.create_packlet_file(execMeth, shell, isudo, cmds, filename)
        
        # Success info box
        packlet_info = {
            f"📁 File": filename,
            f"⚙️ Method": execMeth,
            f"🐚 Shell": shell,
            f"🔒 Sudo needed": str(isudo),
            f"📋 Commands": str(number_of_cmds)
        }
        
        success_box = create_info_box("🎉 SUCCESS! 🎉", packlet_info, 50)
        print(f"\n{success_box}")
        
    except Exception as e:
        print_error(f"Failed to create packlet: {str(e)}")

def main():
    """Main application loop with enhanced UI"""
    clear_screen()
    print_banner()
    
    while True:
        print_menu()
        
        option = get_input("Select an option (1-3): ", Colors.BOLD)
        
        if option == "1":
            run_packlet()
        elif option == "2":
            create_packlet()
        elif option == "3":
            print(f"\n{Colors.CYAN}Thanks for using Pack V1! 👋{Colors.RESET}")
            print(f"{Colors.YELLOW}Stay awesome and keep packing! 📦✨{Colors.RESET}\n")
            sys.exit(0)
        else:
            print_error("Invalid option. Please select 1, 2, or 3.")
        
        # Ask to continue
        print(f"\n{Colors.BLUE}{'─' * 60}{Colors.RESET}")
        continue_prompt = get_input("Press Enter to return to main menu, or 'q' to quit: ", Colors.CYAN)
        if continue_prompt.lower() == 'q':
            print(f"\n{Colors.CYAN}Goodbye! 👋{Colors.RESET}\n")
            break
        clear_screen()
        print_banner()

if __name__ == "__main__":
    main()
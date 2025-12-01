#!/usr/bin/env python3
# type: ignore
"""
Shared utilities for bin scripts
Modern TUI with rich library - battle-tested, beautiful, maintainable
"""

import os
import platform
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from rich import box as rich_box
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.text import Text

    console = Console()
    RICH_AVAILABLE = True

except ModuleNotFoundError:
    # Clean fallback that strips rich markup when rich isn't installed
    RICH_AVAILABLE = False

    def _strip_markup(text: str) -> str:
        """Remove rich markup like [bold], [cyan], etc."""
        return re.sub(r"\[/?[^\]]+\]", "", str(text))

    class _FallbackPanel:
        """Simple panel that just prints the content with borders"""

        def __init__(self, content, box=None, border_style=None, padding=None, **kwargs):
            self.content = _strip_markup(content)

        def __str__(self):
            return f"\n{'═' * 60}\n{self.content}\n{'═' * 60}\n"

    class _FallbackTable:
        """Simple table that prints rows"""

        def __init__(self, show_header=True, box=None, border_style=None, **kwargs):
            self.rows = []
            self.show_header = show_header

        def add_column(self, *args, **kwargs):
            """No-op for compatibility"""
            pass

        def add_row(self, *items, **kwargs):
            """Add a row of items"""
            clean_items = [_strip_markup(item) for item in items]
            self.rows.append(" | ".join(clean_items))

        def __str__(self):
            return "\n".join(self.rows)

    class _FallbackProgress:
        """Simple progress that just prints task descriptions"""

        def __init__(self, *args, **kwargs):
            """Accept any arguments for compatibility"""
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def add_task(self, description: str = "", total: int | None = None):
            """Print task description and return dummy task ID"""
            print(_strip_markup(description))
            return 0

        def update(self, task_id: int, advance: int = 1, description: str | None = None):
            """Print update if description provided"""
            if description:
                print(_strip_markup(description))

    class _FallbackText(str):
        """Text class that just behaves like a string"""

        def __new__(cls, text="", style=None):
            """Create a new Text object, ignoring style in fallback mode"""
            return str.__new__(cls, text)

    class _FallbackConsole:
        """Minimal console that strips markup and prints plain text"""

        def print(self, *args, style=None, justify=None, **kwargs):
            """Print with markup stripped"""
            clean_args = []
            for arg in args:
                # Handle Panel and Table objects
                if isinstance(arg, _FallbackPanel | _FallbackTable):
                    clean_args.append(str(arg))
                else:
                    clean_args.append(_strip_markup(arg))
            print(*clean_args)

        def rule(self, text: str = "", style=None, **kwargs):
            """Print a simple horizontal rule"""
            print(f"\n{'─' * 60}")
            if text:
                print(_strip_markup(text))
            print("─" * 60)

    class _FallbackBox:
        """Box styles - all None since we're not using them"""

        DOUBLE = ROUNDED = SIMPLE = None

    # Assign fallback implementations
    console = _FallbackConsole()

    def Panel(content, **kwargs):  # noqa: N802
        return _FallbackPanel(content, **kwargs)

    Table = _FallbackTable
    Progress = _FallbackProgress
    Text = _FallbackText
    rich_box = _FallbackBox()

    # These are only used in helper functions, provide dummy classes
    class SpinnerColumn:
        """Dummy spinner column for compatibility"""

        pass

    class TextColumn:
        """Dummy text column for compatibility"""

        def __init__(self, *args, **kwargs):
            pass

    # Inform user about fallback mode
    print(
        "ℹ️  rich not installed yet - using plain output\n"
        "   Install dependencies to enable beautiful formatting:\n"
        "   pip install -r requirements.txt -r requirements-dev.txt\n"
    )


class Art:
    """Demoscene-style ASCII art - keeping the fun underground aesthetic"""

    LOGO_CRACKTRO = """
    ┌─────────────────────────────────────────────────┐
    │ ██▄ ▄██  ▄██▄  █▀▀▀  ▄▄▄   ▄▄▄▄               │
    │ █ █▄█ █ █▄▄▄█ █▄▄▄  █   █ █▄▄▄    v1.94       │
    │ █  █  █ █   █ █     █▄▄▄█     █ ────────────  │
    │ █     █ █   █ █     █   █ ████   БАЛКАН BBS  │
    │                                   est. 1994    │
    └─────────────────────────────────────────────────┘
    """

    LOGO_CYRILLIC = """
    ╔════════════════════════════════════════════╗
    ║ ██▄  ███  █▀▀▄   ▄▄▄   ▄▄▄▄               ║
    ║ █ █  █ █  █▀▀█  █   █ █▄▄▄                ║
    ║ ██▀  ███  █  █  █▄▄▄█     █  [БАЛКАН·94] ║
    ╚════════════════════════════════════════════╝
    """

    LOGO_ANSI = """
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    ░ #####   ###   #####    ###   ####        ░
    ░ ##  ##  ###   ## ##   ## ## ##           ░
    ░ #####  ## ##  ####   ##   ##  ###        ░
    ░ ##  ## #####  ## ##  ##   ##    ##       ░
    ░ #####  ## ##  #   #   ## ##  ####        ░
    ░                                           ░
    ░    -= underground venue tools 1994 =-    ░
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """

    LOGO_ASCII = """
    ╔══════════════════════════════════════════╗
    ║  ___  __  ___    __  ___               ║
    ║ |  _ |__||  _   |  ||__ \\             ║
    ║ | |_|||  || |    |  | __| |    [1994]  ║
    ║ |____||__||_|     |__||___/             ║
    ║                                          ║
    ║    venue management * никада не умире   ║
    ╚══════════════════════════════════════════╝
    """

    LOGO_MINIMAL = """
    ┌────────────────────────────────────┐
    │  ~*~ BAR/OS v0.94 ~*~             │
    │  underground venue tools           │
    └────────────────────────────────────┘
    """

    TAGLINE = [
        "No corporate bullshit. Just tools that work.",
        "Built by people who actually run venues.",
        "Because juggling 20 different apps sucks.",
        "For anarchists, artists, and everyone in between.",
        "Punk rock infrastructure for real spaces.",
        "Underground venue tools since 1994.",
        "Made for squats, clubs & DIY spaces.",
        "Fuck spreadsheets. Code is freedom.",
    ]

    @classmethod
    def random_logo(cls) -> str:
        """Get a random logo variant"""
        return random.choice(
            [cls.LOGO_CRACKTRO, cls.LOGO_CYRILLIC, cls.LOGO_ANSI, cls.LOGO_ASCII, cls.LOGO_MINIMAL]
        )

    @classmethod
    def random_tagline(cls) -> str:
        """Get a random tagline"""
        return random.choice(cls.TAGLINE)


def print_header(message: str, subtitle: str = ""):
    """Print a fancy header with a panel"""
    if subtitle:
        text = f"[bold]{message}[/bold]\n[dim]{subtitle}[/dim]"
    else:
        text = f"[bold]{message}[/bold]"

    console.print(Panel(text, box=rich_box.DOUBLE, border_style="cyan", padding=(1, 2)))


def print_success(message: str):
    """Print success message with checkmark"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str):
    """Print error message with X"""
    console.print(f"[red]✗[/red] {message}", style="red")


def print_warning(message: str):
    """Print warning with warning symbol"""
    console.print(f"[yellow]⚠[/yellow] {message}", style="yellow")


def print_info(message: str):
    """Print info message with arrow"""
    console.print(f"[cyan]→[/cyan] {message}")


def print_step(step: int, total: int, message: str):
    """Print a step in a multi-step process"""
    console.print(f"[magenta bold][{step}/{total}][/magenta bold] {message}")


def print_section(title: str):
    """Print a section divider"""
    console.print()
    console.rule(f"[bold cyan]{title}[/bold cyan]", style="cyan")
    console.print()


def show_demoscene_intro(show_tagline: bool = True):
    """Show a demoscene-style intro with random logo"""
    logo = Art.random_logo()

    # Create gradient effect for the logo
    console.print(logo, style="bold cyan", justify="left")

    if show_tagline:
        tagline = Art.random_tagline()
        console.print(f"\n    [bold magenta]{tagline}[/bold magenta]\n")
    else:
        console.print()


def show_banner(message: str, style: str = "green"):
    """Show a banner message"""
    console.print(
        Panel(f"[bold]{message}[/bold]", box=rich_box.DOUBLE, border_style=style, padding=(1, 4))
    )


def get_project_root() -> Path:
    """Get the project root directory"""
    start_dir = Path(__file__).resolve().parent
    fallback_root = start_dir.parent
    markers = ("pyproject.toml", "manage.py", ".git")

    for directory in (start_dir, *start_dir.parents):
        if any((directory / marker).exists() for marker in markers):
            return directory

    return fallback_root.resolve()


def get_venv_python() -> Path:
    """Get the Python executable inside the virtual environment"""
    venv_path = get_project_root() / ".venv"

    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"

    return python_exe


def get_venv_path() -> Path:
    """Get the virtual environment path"""
    return get_project_root() / ".venv"


def get_venv_pip() -> Path:
    """Get the pip executable inside the virtual environment"""
    venv_path = get_venv_path()

    if platform.system() == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"


def check_virtualenv() -> bool:
    """Check if virtual environment exists"""
    venv_python = get_venv_python()

    if not venv_python.exists():
        print_error("Virtual environment not found!")
        print_info("Please run setup first:")

        if platform.system() == "Windows":
            console.print("  [bold]python bin\\setup[/bold]")
        else:
            console.print("  [bold]./bin/setup[/bold]")

        return False

    return True


def run_command(
    cmd: list[str],
    description: str | None = None,
    check: bool = True,
    env: dict | None = None,
    capture_output: bool = False,
    error_message: str | None = None,
) -> subprocess.CompletedProcess:
    """Run a command with nice output"""
    if description:
        print_info(description)

    # Merge environment variables
    command_env = os.environ.copy()
    if env:
        command_env.update(env)

    try:
        kwargs: dict[str, Any] = {"check": check, "env": command_env, "cwd": get_project_root()}

        if capture_output:
            kwargs["capture_output"] = True
            kwargs["text"] = True

        result = subprocess.run(cmd, **kwargs)
        return result
    except subprocess.CalledProcessError as e:
        if error_message:
            print_error(error_message)
        print_error(f"Command failed with exit code {e.returncode}")
        if check:
            sys.exit(e.returncode)
        return e
    except FileNotFoundError as e:
        if error_message:
            print_error(error_message)
        print_error(f"Command not found: {cmd[0]}")
        if check:
            sys.exit(1)
        return e


def run_django_command(command: list[str], description: str | None = None):
    """Run a Django management command using venv Python"""
    if not check_virtualenv():
        sys.exit(1)

    venv_python = get_venv_python()
    manage_py = get_project_root() / "manage.py"

    cmd = [str(venv_python), str(manage_py)] + command
    return run_command(cmd, description)


def create_status_table(results: dict[str, bool]) -> Table:
    """Create a beautiful status table"""
    table = Table(show_header=False, box=rich_box.ROUNDED, border_style="cyan")
    table.add_column("Status", width=3)
    table.add_column("Check", style="cyan")
    table.add_column("Result", justify="right")

    for check_name, passed in results.items():
        if passed:
            status = "[green]✓[/green]"
            result = "[green]PASS[/green]"
        else:
            status = "[red]✗[/red]"
            result = "[red]FAIL[/red]"

        table.add_row(status, check_name.title(), result)

    return table


def with_progress(description: str = "Working..."):
    """
    Context manager for long-running operations with a spinner.

    Example:
        with with_progress("Installing dependencies..."):
            # Your long-running operation here
            time.sleep(5)
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    )


def print_styled(text: str, style: str = ""):
    """
    Print text with rich styling.

    Args:
        text: Text to print
        style: Rich style string (e.g., "bold cyan", "red on white")

    Example:
        print_styled("Important!", "bold red")
        print_styled("Success", "green")
    """
    styled_text = Text(text, style=style) if style else Text(text)
    console.print(styled_text)

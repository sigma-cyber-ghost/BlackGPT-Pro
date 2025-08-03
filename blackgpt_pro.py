# blackgpt_pro.py
import os
import requests
import json
import time
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from rich.rule import Rule
import pyfiglet
import random
import sys
import readline
import webbrowser
import re

console = Console()

# --- Social Media Links ---
SOCIAL_MEDIA = {
    "Telegram": "@Sigma_Cyber_Ghost",
    "Instagram": "@safderkhan0800_",
    "GitHub": "https://github.com/sigma-cyber-ghost",
    "YouTube": "https://youtube.com/@sigma_cyber_ghost",
    "X (an0n39)": "https://x.com/an0n39/",
    "X (safderkhan)": "https://x.com/safderkhan0800_/"
}

SOCIAL_LINKS = {
    "Telegram": "https://web.telegram.org/k/#@Sigma_Cyber_Ghost",
    "GitHub": "https://github.com/sigma-cyber-ghost",
    "YouTube": "https://www.youtube.com/@sigma_ghost_hacking",
    "X (an0n39)": "https://x.com/an0n39/",
    "X (safderkhan)": "https://x.com/safderkhan0800_/"
}

# --- API Map ---
api_endpoints = {
    "WormGPT": "https://sii3.moayman.top/DARK/api/wormgpt.php?text=",
    "DeepSeek-v3": "https://sii3.moayman.top/api/deepseek.php?v3=",
    "DeepSeek-R1": "https://sii3.moayman.top/api/deepseek.php?r1=",
    "DeepSeekT1": "http://sii3.moayman.top/api/DeepSeek/DeepSeek.php?text=",
    "DarkGPT": "http://sii3.moayman.top/DARK/api2/darkgpt.php?text=",
    "Gemini": "http://sii3.moayman.top/DARK/gemini.php?text=",
    "Blackbox": "http://sii3.moayman.top/api/black.php?blackbox=",
    "GPT-4": "https://sii3.moayman.top/api/gpt.php?gpt-4=",
    "GPT-4o": "https://sii3.moayman.top/api/gpt.php?gpt-4o=",
    "GPT-4-1": "https://sii3.moayman.top/api/gpt.php?gpt-4-1=",
    "Mistral": "https://sii3.moayman.top/api/gpt.php?mistral=",
    "Phi": "https://sii3.moayman.top/api/gpt.php?phi=",
    "DeepInfra-v3": "http://sii3.moayman.top/api/DeepInfra.php?deepseekv3=",
}

# --- Custom Banner ---
BANNER = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣄⠀⠐⣶⣶⣶⣶⣶⡖⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣶⠆⠀⠀⢀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡏⢅⠄⡀⠉⢛⡙⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢄⡆⡀⠀⢀⣠⣤⣾⣿⣿⣿⡃⠀⠀⢸
⠀⡀⠀⠀⠂⠀⠀⠀⠈⢀⠀⠀⢠⣷⡏⣲⡀⣀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡐⠌⣘⣲⡄⣿⣿⣿⣿⣿⣿⣿⡅⠀⠀⠀
⣿⢕⠀⠀⠀⠀⠀⠐⠀⠋⠀⠀⢸⡟⡜⢣⣹⣿⣿⣶⣶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡚⠃⠀⠉⢿⡧⠘⠉⠁⠈⢻⢿⣿⠆⠀⠀⠀
⡵⡾⠀⠀⠀⠀⠿⠛⠁⠀⠀⠀⠈⠀⠀⣤⣶⣶⣶⣶⣤⣀⢠⠀⠀⡀⢀⠀⡀⠀⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢀⣀⣠⣾⣇⠀⠀⠀⠀⠀⠈⠹⡃⠀⠀⠀
⣦⠁⠀⠀⢘⣦⡀⠀⠤⠒⠈⠀⠀⠀⠀⠀⢠⡀⣄⡀⣀⠀⠀⠈⠀⠉⠈⠘⠒⠛⠂⠀⠀⠀⠀⠴⣤⢢⣄⠀⠀⣄⣀⠘⠻⢿⡗⠀⠀⠀⠀⠀⠀⠀⡅⠀⠀⠀
⣟⣧⠀⠀⠼⠛⣥⡃⠄⡀⠀⠀⠀⠀⠀⠀⣮⣽⣿⣿⣿⣻⡖⣶⣼⣦⣴⣀⢀⠀⢠⠠⠄⡀⢀⠀⠀⠀⠀⠈⠉⠈⠀⠙⠀⠄⠈⠀⠀⠀⢀⣴⣶⣶⠆⠀⠀⠀
⣿⣿⡀⠀⠀⠀⣿⡹⢎⠔⠀⡀⠀⠀⠀⠴⠺⣿⣿⣿⠃⠁⠈⠈⠉⠛⠻⡹⣞⡂⢅⡊⠴⡐⢏⡟⣼⣿⣿⢦⣦⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⢸⣿⣿⡃⠀⠀⠀
⣿⣿⡆⢰⣤⡀⠙⡸⢌⡚⠄⠀⠀⠀⠀⣠⣿⣿⣿⠅⠀⠀⠀⠀⠀⠀⠀⠘⢆⠱⠀⠨⠑⠉⠀⠀⠀⠀⠀⠉⣾⠀⠀⠀⠀⠀⢰⣠⣶⣷⣾⡟⣿⣿⠇⠀⠀⠈
⣿⣿⡇⠫⣿⣿⠀⠀⠃⠜⡄⠀⠀⠀⠀⣽⣿⣿⠏⠃⠀⠀⠀⠀⠀⠀⠀⡀⡈⣔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡄⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣻⣿⡇⠀⠀⠀
⣿⣿⣀⣤⣿⣿⣇⠀⠀⢰⡀⠀⠈⠄⠀⣿⣿⣿⠦⣁⠒⣶⣴⣴⡶⢼⢭⣇⠞⠁⠀⠘⡤⣀⠀⠀⠀⠀⠀⢦⣹⡇⠀⠀⠀⡜⠀⣿⡿⠛⣵⣿⣿⣿⡆⠀⠀⠀
⣿⣿⣿⣅⠀⠚⣿⡆⠀⠢⠄⠀⠀⢂⠀⣿⣿⣿⢰⢩⡙⣾⣿⣿⢯⣯⣿⠇⠀⠀⠀⠀⢰⢩⣿⠇⠀⣀⠉⠢⢵⡇⠀⠀⡘⠄⠐⠋⣠⣾⣿⣿⣿⣿⠆⠀⠀⠀
⣿⣿⣿⣿⣧⣠⣼⣿⠀⢀⠂⠀⠀⠀⢂⠙⢍⠣⣋⢧⣝⣾⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢨⣹⢎⠀⢦⠑⢢⡙⡼⠀⠀⡐⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⡇⠀⠀⢈
⣿⣿⣿⣿⣿⣿⣧⠥⢭⣤⣤⠀⠀⠀⠢⠀⠀⠀⠀⠜⣿⣿⣿⡏⣿⣿⠟⣀⠠⢢⠄⡀⢤⣛⡎⠜⠢⠉⠂⠁⠀⠀⠐⠀⠀⡀⣿⣿⣿⣿⣿⣿⣿⣿⡷⡇⠀⠀
⣿⣿⣿⣿⣿⣿⢱⢃⠀⠉⠃⠀⠀⠀⠀⡃⠀⠀⠀⠀⠾⣿⣿⢱⡧⡇⠀⡣⠘⡁⠂⠴⢸⣟⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣱⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⠀⠀
⣿⣿⣿⣿⣿⣿⣎⢧⠂⠀⠀⠀⠀⠀⠀⠰⠁⠀⠀⠀⠀⣯⢋⡎⡑⣁⢐⡑⣀⠃⡘⠠⣻⠍⠀⠀⠀⠀⢠⣶⣶⡖⠀⣀⣤⣛⠻⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣯⡣⡅⡀⠀⠀⠱⣀⠀⠑⠀⠀⠀⠀⠀⡇⢨⠀⠃⠈⠃⠘⠐⠂⠂⠒⠀⠀⠀⠀⠀⠀⢻⣿⠀⢼⣿⣿⣿⣿⣦⡙⢿⣿⣿⣿⣿⡃⠀⠀⢀
⠙⣿⠿⡿⢿⣿⣿⣿⣷⣜⠡⣆⡀⠀⠀⠈⠄⠠⠀⠀⠀⠀⡏⡔⠰⠀⠆⡄⢀⠀⡘⠐⠀⠀⠀⠀⠀⠀⠠⣌⢿⠀⣼⣿⣿⣿⣿⣿⠿⢸⣿⣿⣿⣿⠄⠀⠀⠀
⠀⠀⠀⠃⢫⣿⣿⣿⣿⣿⣷⠆⠹⢤⡀⠀⠀⠀⠈⠀⠃⠄⠀⠁⠀⠘⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠌⠎⢀⣿⣿⣿⣿⠟⣡⣾⣿⣿⣿⣿⣿⠂⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠙⠿⢿⣿⣾⢁⠀⠉⠣⠄⠀⠀⠀⠀⠆⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡿⠛⠰⠿⠁⠀⠉⢹⣿⣿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠫⣭⣓⠏⠤⢠⡊⠑⣠⡀⠀⠀⠀⠁⠀⠰⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠂⠄⠀⠀⠀⠀⠉⠋⠁⠀⠀⠀⠀⠀⠀⠈⢟⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠐⡠⠀⠀⠈⠛⢿⣶⣬⡖⠁⠄⠳⠆⣀⠀⠀⠀⠀⠀⠀⠈⠀⠀⡐⠀⠡⠀⠀⠀⠠⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⠀⠐
⠀⠀⠀⠀⠀⠀⠀⠀⡑⠬⢠⠀⠀⠀⠈⠀⠏⠀⠈⢀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠀⠀⠀⠈
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡁⠎⠤⡀⠀⠀⠀⠀⠀⠀⠂⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⢢⢒⡡⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠡⠚⡐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠡⠀⠁⠀⠠⠁⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def open_social_media_once():
    """Open all social media profiles in browser once at startup"""
    console.print("[bold cyan][!] Opening social media profiles in browser...[/]")
    for name, url in SOCIAL_LINKS.items():
        try:
            webbrowser.open(url, new=2)
            time.sleep(0.3)
        except Exception as e:
            console.print(f"[bold red]Error opening {name}: {str(e)}", style="bold red")
    time.sleep(1.5)  # Give time for browsers to open

def matrix_effect():
    """Create a matrix-style code rain effect"""
    chars = "01"
    width = console.width
    for _ in range(5):
        console.print("".join(random.choice(chars) for _ in range(width)), 
                    style="bold green", end="\r")
        time.sleep(0.1)

def glitchy_text(text, style="bold red"):
    font = random.choice(["slant", "standard", "doom", "big"])
    ascii_art = pyfiglet.figlet_format(text, font=font)
    console.print(ascii_art, style=style)

def clean_response(text):
    """Remove XML tags and unnecessary whitespace from responses"""
    # Remove <think> tags and content
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove other XML-like tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def banner():
    console.clear()
    # Matrix intro effect
    matrix_effect()
    
    # Custom banner with hacker theme
    console.print(BANNER, style="bold green")
    console.print(Rule(style="bold bright_magenta", title="⚡ SIGMA CYBER GHOST ⚡", align="center"))
    
    # Social media links
    sm_table = Table.grid(padding=(0, 3))
    sm_table.add_row(
        Panel(
            "\n".join([f"[bold cyan]{k}:[/] {v}" for k,v in SOCIAL_MEDIA.items()]),
            title="[blink]SOCIAL PROFILES[/]",
            border_style="bright_cyan",
            box=box.DOUBLE,
            width=50
        ),
        Panel(
            "[bold yellow]MODES:\n- Chat\n- File Analysis\n- Code Generation\n- Dark Web Search\n- Exploit Generation[/]",
            title="[blink]CAPABILITIES[/]",
            border_style="bright_yellow",
            box=box.DOUBLE,
            width=50
        )
    )
    console.print(sm_table)
    console.print(Rule(style="bold bright_magenta"))

def select_model():
    table = Table(title="[bold blink]AVAILABLE LLM MODELS[/]", show_lines=True, border_style="blue", 
                header_style="bold magenta", expand=True)
    table.add_column("ID", justify="center", style="bold cyan")
    table.add_column("Model Name", style="bold white")
    
    for i, key in enumerate(api_endpoints.keys()):
        table.add_row(f"{i}", f"[bold green]{key}[/]")
    
    console.print(table)
    choice = IntPrompt.ask("[bold magenta][!] SELECT MODEL ID", choices=[str(i) for i in range(len(api_endpoints))])
    return list(api_endpoints.items())[choice]

def parse_response(text):
    try:
        parsed = json.loads(text)
        for key in ['response', 'message', 'data', 'result']:
            if key in parsed:
                inner = parsed[key]
                if isinstance(inner, dict) and 'text' in inner:
                    return inner['text']
                if isinstance(inner, str):
                    return inner
        return json.dumps(parsed, indent=2)
    except:
        return text.strip()

def show_loading():
    messages = [
        "Ghost Interface ➤ Breaching Security...",
        "Ghost Interface ➤ Accessing Mainframe...",
        "Ghost Interface ➤ Decrypting Data...",
        "Ghost Interface ➤ Injecting Payload...",
        "Ghost Interface ➤ Bypassing Firewall..."
    ]
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold green"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description=random.choice(messages), total=None)
        time.sleep(random.uniform(0.5, 1.2))

def display_response(response, model_key):
    """Clean and display the response with proper formatting"""
    # Clean the response
    cleaned = clean_response(response)
    
    # Get current timestamp
    ts = datetime.now().strftime("%H:%M:%S")
    
    # Print the response with model tag
    console.print(f"[bold bright_blue]{ts} [{model_key.upper()}]:[/]")
    console.print(f"[bold green]{cleaned}[/]")

def load_file():
    """Load file content with path completion"""
    file_path = Prompt.ask("[bold yellow][?] ENTER FILE PATH", default="")
    if not file_path:
        return None
    
    try:
        if not os.path.exists(file_path):
            console.print("[bold red][!] ERROR: File not found[/]")
            return None
            
        with open(file_path, 'r') as f:
            content = f.read()
            
        console.print(f"[bold green][✓] FILE LOADED: {file_path}[/]")
        console.print(Panel(
            content[:500] + ("..." if len(content) > 500 else ""),
            title=f"FILE PREVIEW: {os.path.basename(file_path)}",
            subtitle=f"{len(content)} chars",
            border_style="yellow",
            width=80
        ))
        return content
    except Exception as e:
        console.print(f"[bold red][!] ERROR: {str(e)}[/]")
        return None

def chat_loop():
    banner()
    model_key, model_url = select_model()
    console.print(f"\n[bold green][+] INTERFACE LOCKED TO: [blink]{model_key}[/][/]")
    console.print("[bold cyan][i] TIPS: Type '/load' to analyze a file, '/help' for commands[/]\n")
    
    # Enable file path tab completion
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" \t\n;")
    
    loaded_file = None

    while True:
        try:
            query = Prompt.ask("[bold magenta]SIGMA ➤")
            
            # Get timestamp for user query
            user_ts = datetime.now().strftime("%H:%M:%S")
            
            # Command handling
            if query.lower() == '/load':
                loaded_file = load_file()
                continue
                
            elif query.lower() == '/clear':
                loaded_file = None
                console.print("[bold green][✓] FILE CONTEXT CLEARED[/]")
                continue
                
            elif query.lower() == '/exit':
                console.print("\n[bold red][!] GHOST LINK SEVERED. UNTIL NEXT BREACH.")
                glitchy_text("DISCONNECTED", style="bold red")
                break
                
            elif query.lower() == '/help':
                console.print(Panel(
                    "[bold]COMMANDS:\n"
                    "/load      - Analyze a file\n"
                    "/clear     - Clear loaded file\n"
                    "/models    - Switch AI model\n"
                    "/chatgpt   - Switch to ChatGPT models\n"
                    "/exit      - Terminate session\n"
                    "/help      - Show this help[/]",
                    title="[blink]SYSTEM COMMANDS[/]",
                    border_style="cyan"
                ))
                continue
                
            elif query.lower() == '/models':
                model_key, model_url = select_model()
                console.print(f"\n[bold green][+] INTERFACE LOCKED TO: [blink]{model_key}[/][/]")
                continue
            
            elif query.lower() == '/chatgpt':
                # Filter only ChatGPT models
                chatgpt_models = {k: v for k, v in api_endpoints.items() if 'gpt' in k.lower()}
                
                if not chatgpt_models:
                    console.print("[bold red][!] No ChatGPT models available[/]")
                    continue
                
                table = Table(title="[bold blink]CHATGPT MODELS[/]", show_lines=True, border_style="blue", 
                            header_style="bold magenta", expand=True)
                table.add_column("ID", justify="center", style="bold cyan")
                table.add_column("Model Name", style="bold white")
                
                for i, key in enumerate(chatgpt_models.keys()):
                    table.add_row(f"{i}", f"[bold green]{key}[/]")
                
                console.print(table)
                choice = IntPrompt.ask("[bold magenta][!] SELECT MODEL ID", choices=[str(i) for i in range(len(chatgpt_models))])
                model_key, model_url = list(chatgpt_models.items())[choice]
                console.print(f"\n[bold green][+] INTERFACE LOCKED TO: [blink]{model_key}[/][/]")
                continue
            
            # Print user query immediately with timestamp
            console.print(f"[bold green]{user_ts} [YOU]:[/] {query}")
            
            # Prepare query
            full_query = query
            if loaded_file:
                full_query = f"CONTEXT FROM LOADED FILE:\n{loaded_file[:2000]}\n\nUSER QUERY: {query}"
            
            # Send to model
            show_loading()
            start_time = time.time()
            r = requests.get(model_url + requests.utils.quote(full_query), timeout=25)
            r.raise_for_status()
            response = parse_response(r.text)
            
            # Display response
            display_response(response, model_key)
            
            # Show response time
            console.print(f"[dim i]Response time: {time.time() - start_time:.2f}s[/]\n")
            
        except requests.exceptions.Timeout:
            console.print("[bold red][!] ERROR: Request timed out. Network may be compromised.[/]")
        except Exception as e:
            console.print(f"[bold red][!] CRITICAL ERROR: {e}[/]")

def main():
    # Open social media profiles once at startup
    open_social_media_once()
    
    # Start the chat interface
    chat_loop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red][!] CONNECTION TERMINATED BY Sigma-Ghost")
        glitchy_text("Cyber Ghost", style="bold red")
    except Exception as e:
        console.print(f"[bold red on black][X] FATAL SYSTEM ERROR: {e}")
        glitchy_text("SYSTEM FAILURE", style="bold red")

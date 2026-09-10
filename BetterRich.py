from rich.console import Console 

console = Console()

def bold(text):
    console.print(text, style="bold")

def red(text):
    console.print(text, style="red")

def green(text):
    console.print(text, style="green")

def warn(text):
    console.print(text, style="bold red")

def good(text):
    console.print(text, style="bold green")
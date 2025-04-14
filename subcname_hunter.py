import subprocess
import sys
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeElapsedColumn, SpinnerColumn
from rich.table import Table
from time import sleep

console = Console()

def show_banner():
    banner = r"""
                     __         ______                                              
                    /  |       /      \                                             
  _______  __    __ $$ |____  /$$$$$$  | _______    ______   _____  ____    ______  
 /       |/  |  /  |$$      \ $$ |  $$/ /       \  /      \ /     \/    \  /      \ 
/$$$$$$$/ $$ |  $$ |$$$$$$$  |$$ |      $$$$$$$  | $$$$$$  |$$$$$$ $$$$  |/$$$$$$  |
$$      \ $$ |  $$ |$$ |  $$ |$$ |   __ $$ |  $$ | /    $$ |$$ | $$ | $$ |$$    $$ |
 $$$$$$  |$$ \__$$ |$$ |__$$ |$$ \__/  |$$ |  $$ |/$$$$$$$ |$$ | $$ | $$ |$$$$$$$$/ 
/     $$/ $$    $$/ $$    $$/ $$    $$/ $$ |  $$ |$$    $$ |$$ | $$ | $$ |$$       |
$$$$$$$/   $$$$$$/  $$$$$$$/   $$$$$$/  $$/   $$/  $$$$$$$/ $$/  $$/  $$/  $$$$$$$/ 
                                                                                                                                                                                                                                                           
                       Created by [ ghost4ft ]
"""
    console.print(banner, style="bold green")

def run_subfinder(domain):
    result = subprocess.run(
        ["subfinder", "-silent", "-d", domain],
        capture_output=True, text=True
    )
    return result.stdout.strip().splitlines()

def dig_cname(domain):
    result = subprocess.run(
        ["dig", "+short", "CNAME", domain],
        capture_output=True, text=True
    )
    return result.stdout.strip() or None

def check_alive(urls):
    process = subprocess.Popen(
        ["httpx", "-silent"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    joined_input = "\n".join(urls)
    out, err = process.communicate(input=joined_input)
    return set(out.strip().splitlines())

def save_to_file(success_list, filename="cname_results.txt"):
    with open(filename, "w") as f:
        for domain, full_url in success_list:
            f.write(f"{domain} --> {full_url}\n")

def save_subdomains_to_file(subdomains, filename="subdomains.txt"):
    with open(filename, "w") as f:
        for subdomain in subdomains:
            f.write(f"{subdomain}\n")

def print_tables(alive, not_alive):
    
    if alive:
        table1 = Table(title="🟢 Alive Domains", style="green")
        table1.add_column("Domain")
        table1.add_column("CNAME")
        for domain, url in alive:
            table1.add_row(domain, url)
        console.print(table1)

   
    if not_alive:
        table2 = Table(title="🔴 Not Alive Domains", style="red")
        table2.add_column("Domain")
        table2.add_column("CNAME")
        for domain, url in not_alive:
            table2.add_row(domain, url)
        console.print(table2)

def main():
    domain = sys.argv[1]  
    show_banner()
    
    console.print(f"[bold cyan]🔍 Running subfinder for:[/] {domain}")
    subdomains = run_subfinder(domain)

    if not subdomains:
        console.print("[bold red]No subdomains found![/bold red]")
        return

   
    save_subdomains_to_file(subdomains, filename="subdomains.txt")
    console.print(f"[bold yellow]✔ Saved {len(subdomains)} subdomains to subdomains.txt[/bold yellow]")

    success_list = []
    total = len(subdomains)

    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Checking CNAMEs...", total=total)

        for sub in subdomains:
            cname = dig_cname(sub)
            if cname:
                success_list.append((sub, f"http://{cname}"))
            progress.advance(task)
            sleep(0.01)


    save_to_file(success_list, filename="cname_results.txt")
    console.print(f"\n[bold green]✔ Saved {len(success_list)} results to cname_results.txt[/bold green]")

    if not success_list:
        console.print("[bold red]No CNAME records found.[/bold red]")
        return

    urls = [url for _, url in success_list]
    alive_urls = check_alive(urls)

    alive = []
    not_alive = []
    for domain, url in success_list:
        if url in alive_urls:
            alive.append((domain, url))
        else:
            not_alive.append((domain, url))

    console.print(f"\n[bold cyan]🌐 HTTPX Result:[/] {len(alive)} alive / {len(not_alive)} not alive\n")
    print_tables(alive, not_alive)

if __name__ == "__main__":
    main()
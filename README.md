# Savage PUBLIC 0.1
![Web Interace](https://i.imgur.com/HSDKx4R.png)<div style="page-break-after: always;"></div>
![Command-line interface](https://i.imgur.com/NDwXPXI.png)<div style="page-break-after: always;"></div>


&nbsp;
## Features

*   Create & exfiltrate a fileless screenshot
*   NEW! Web interface built w/ Flask
*   Leverages Dropbox API

&nbsp;
## Instructions

*	Create a Dropbox app & generate an `Access Token` with all permissions for `Individual Scopes`.

		https://www.dropbox.com/developers/reference/getting-started

&nbsp;
### **Server**:		

*	Modify `access_token` variable in `Server.py` and `Implant.py` to reflect newly obtained `Access Token`.
*	Compile `Implant.py` to EXE with PyInstaller, utilizing `--noconsole` and `--onefile` flags.

&nbsp;
### **Client**:
*	Create `~.tmp` in `%TEMP%` containing a UUID :

		python3 -c "import uuid;print(uuid.uuid4())" > %TEMP%/~.tmp
* Copy `Implant.exe` to `%TEMP%`.
* Create a scheduled task to run `Implant.exe` every 10 minutes:

		schtasks.exe /sc minute /mo 10 /create /TN "Savage-Public-0.1" /TR "%TEMP%\Implant.exe"

&nbsp;

## Screenshots

![Help menu](https://i.imgur.com/IyNHyeF.png)


![List clients](https://i.imgur.com/6JiEOqS.png)


![Send command to client](https://i.imgur.com/uLJHFEA.png)<div style="page-break-after: always;"></div>


![Fetch files from client](https://i.imgur.com/9lhL7rx.png)<div style="page-break-after: always;"></div>

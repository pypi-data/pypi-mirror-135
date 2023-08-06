# FTPX

A lib to send a file e create folder in a FTP Server.

## How to install

```bash
pip install ftpx
```
## How to Use
```pyhton
from ftpx.ftpx import FTPService

ftp_server = "127.0.0.1"
ftp_login = "xxxx"
ftp_password = "yyyyy"

ftp_service = FTPService(ftp_server, ftp_login, ftp_password)

ftpX.list_files()

filename = "32210406067119000753550010000124561329097173.xml"
local_filename = "/home/user/Documentos/testes/ftp/"+filename
remote_directory = "/user/2022/01/21"


ftpX.create_directory_tree(remote_directory)

ftpX.send_file(local_filename, ftp_file_path)

```

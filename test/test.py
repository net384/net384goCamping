import socket
from pathlib import Path



hostname = socket.gethostname()
filename = (Path(__file__).stem)


##날짜 입력으로 seq 값 확인\\\
DAYFILE_LIVE = '/root/script/'+filename+'.in'
DAYFILE_DEV = filename+'.in'
hostname = socket.gethostname()

if hostname == 'instance-20191108-1623-2388':
    DAYFILE = DAYFILE_LIVE
else:
    DAYFILE = DAYFILE_DEV
    
print(DAYFILE)

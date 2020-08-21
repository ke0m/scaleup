import numpy as np
import zmq
from server.distribute import dstr_collect, dstr_sum
from client.slurmworkers import launch_slurmworkers, kill_slurmworkers
from comm.sendrecv import recv_zipped_pickle, send_next_chunk
import time

def generate_chunks(n):
  i = 0
  while i < n:
    mydict = {}
    mydict['dat'] = np.zeros([6000000],dtype='float32') + 20
    mydict['scale'] = i+1
    mydict['ntry'] = 100000
    mydict['nthrds'] = 40
    yield mydict
    i += 1

# Start workers
cfile = "/home/joseph29/projects/distrmq/bench/zeromqex/ompclient.py"
logpath = "./log"
wrkrs,status = launch_slurmworkers(cfile,nworkers=20,queues=['twohour'],
                                   logpath=logpath,slpbtw=0.5,chkrnng=True)

print(status)

# Create the chunks
nimg = status.count('R')
chunks = generate_chunks(nimg)

# Bind to socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:5555")

okeys = ['result','scale']
output = dstr_collect(okeys,nimg,chunks,socket)
#output = dstr_sum('scale','result',nimg,chunks,socket,6000000)

print(output['scale'])
for k in range(len(output['result'])):
  print(output['result'][k])
#print(output)

kill_slurmworkers(wrkrs)

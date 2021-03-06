"""
Functions for creating workers on a SSH cluster

@author: Joseph Jennings
@version: 2020.08.16
"""
import subprocess
import time
import itertools

def launch_sshworkers(wrkfile,hosts,pyexec=None,sleep=1,status=False,verb=1,clean=False):
  """
  Creates workers (specified by the wrkfile) on
  specified hosts

  Parameters:
    wrkfile - the .py file that describes the worker
    hosts   - a list of host names on which to start the workers
    pyexec  - path to the python executable to start the
              worker (default is /sep/joseph29/anaconda3/envs/py37/bin/python)
    sleep   - sleep for sleep seconds [1] so workers can get started
    status  - get status of started worker [False]
    verb    - verbosity flag [0 nothing, 1 print basic, 2 print command]
    clean   - remove all dangling clients before launching [False]

  Return (potentially, it would be good to return the status of the worker)
  """
  if(pyexec is None):
    pyexec = '/sep/joseph29/anaconda3/envs/py37/bin/python'
  if(clean):
    uhosts = list(set(hosts))
    kill_sshworkers(wrkfile,uhosts,pyexec,verb=False)
    time.sleep(2)
  for ihost in hosts:
    cmd = """ssh -n -f %s "sh -c '%s %s'" """%(ihost,pyexec,wrkfile)
    if(verb):
      if(verb == 1):
        print("Launching on %s"%(ihost))
      elif(verb == 2):
        print("Launching on %s"%(ihost))
        print(cmd)
    sp = subprocess.check_call(cmd,shell=True)
    #if(status):
      #TODO: get and return status
  # Sleep to allow workers to start
  time.sleep(sleep)

def create_host_list(hosts,wph=None):
  """
  Repeats the host name based on number of workers
  per host specified

  Parameters:
    hosts - list of host names
    wph   - number of times to launch worker on the host (one per host)
  """
  if(wph is None):
    wph = np.ones(len(hosts),dtype='int32')
  k = 0; olist = []
  for host in hosts:
    tlist = list(itertools.chain.from_iterable(itertools.repeat(x,wph[k]) for x in [host]))
    olist += tlist
    k += 1

  return olist

def kill_sshworkers(wrkfile,hosts,pyexec=None,status=False,verb=False):
  """
  Kills the started workers on specified hosts

  Parameters:
    wrkfile - the .py file that describes the worker
    hosts   - the hosts on which the worker is running
    pyexec  - path to the python executable that started the worker
    status  - return the status of the workers [False]
    verb    - verbosity flag [False]

  Return (potentially the status of each worker)
  """
  if(pyexec is None):
    pyexec = '/sep/joseph29/anaconda3/envs/py37/bin/python'
  for ihost in hosts:
    kill = """ ssh -n -f %s "sh -c \\"pkill -f \\"%s %s\\"\\"" """%(ihost,pyexec,wrkfile)
    if(verb): print(kill)
    sp = subprocess.check_call(kill,shell=True)
    #if(status):
      #TODO: get and return status


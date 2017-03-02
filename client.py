#Copyright 2006 Ingo R. Keck
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
import string
import time
import sys

def find_job():
   # find open jobs
   # get list of current files
   filelist=os.listdir(os.curdir)
   for filename in filelist:
      # is it a job-file like jxxxx.m?
      filename=string.strip(filename)
      if filename[-2:]==".py" and filename[0]=="j":
         # look for a log-file with the same name
         logname=filename[:-2]
         logname=logname + ".log"
         if os.path.exists(logname)==False:
            # ok, no flag file, so lets try to create one
            try:
               joblog=open(logname,'w')
               joblog.write("Log started at "+time.ctime(time.time())+"\n")
               joblog.close()
               # ok, thats it, we got a job
               return filename                            
            except:
               data=time.ctime(time.time())+": could not open flagfile "\
                  +logname+"\n"
               sys.stdout.write(data)
               # try another job
               continue
         # try the next name in the list
   return

def start_job(jobname):
   # start ocatve with job
   sys.stdout.write(time.ctime(time.time())+": started job "+jobname+"\n")
   jobresult=os.system("octave '"+jobname+"'")
   # the job is finished, but we have to report this as jobname.fin
   finname=jobname[:-2]+".fin"
   try:
      finlog=open(finname,'w')
      finlog.write(time.ctime(time.time())+": finished job with result ")
      finlog.write(str(jobresult))
      finlog.close()
   except:
      data=time.ctime(time.time())+": could not open finished-file "\
                  +finname+"\n"
      sys.stdout.write(data)
   sys.stdout.write(time.ctime(time.time())+": finished job with result ")
   sys.stdout.write(str(jobresult))
   sys.stdout.write("\n")
   return
   
def main():
   while 1==1:
      # search for jobs
      jobname=None
      while jobname==None:
         jobname=find_job() 
         if jobname==None:
            time.sleep(66) # sleep 66 seconds
      # now we have a job in jobname
      start_job(jobname)
   return 1

main()
   
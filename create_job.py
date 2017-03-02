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
import sys
import shutil
import time
import copy

def usage():
   sys.stdout.write("create_job version 0.1 \n")
   sys.stdout.write("Usage: create_job.python [-v][-d job_directory][-i jobsfile] jobname\n")
   sys.stdout.write("\n")
   exit(0)

class programm_options:
   path=os.getcwd()
   files=[]
   jobs={}
   verbose=0

def define_options(options):
   i=1 # i=0 is the name of the executable
   while i < len(sys.argv):  
      if sys.argv[i] == '-d':  #set the directory
         if i+1 < len(sys.argv):
            options.path=sys.argv[i+1]
            i=i+1
         else:  # the user forgot to give the directory
            print "no directory given"
            usage()   
      elif sys.argv[i]=='-i':
         # load the jobs from a file
         if i+1 < len(sys.argv):
            try:
               jobfile=open(sys.argv[i+1],'r')
            except:
               print "Error opening jobfile ",str(sys.argv[i+1])
               usage()
            try:
               while True: # get all lines, deleting the endline character
                 text = jobfile.readline()
                 if text == "":
                    break
                 options.files.append(text[:-1])
            except:
               print "Error reading jobfile ",str(sys.argv[i+1])
               usage()
            i=i+1
         else:
            print "no file for jobs given"
            usage()
      elif sys.argv[i]=='-v':
         options.verbose=1
         print 'verbose mode on'
      elif sys.argv[i]=='--help':
         usage()
      elif sys.argv[i].startswith('-'):
         sys.stdout.write("Commandline argument "+sys.argv[i]+" unknown.\n")
         usage()
      else:
         # must be the jobs
         options.files.append(sys.argv[i])
      i=i+1
      
def copy_jobs(options):
   # first get a list of all jobs in the directory so that we don't get double names
   templist=os.listdir(options.path)
   # trow out all that is no job
   filelist=[]
   for i in templist:
      if i.startswith('j'):
         filelist.append(i)
   #find maximal number
   if len(filelist)==0:
      jobmax=0
   else:
      tempmax=max(filelist)
      jobmax=abs(int(filter( lambda x: x.isdigit(), tempmax)))
   jobnumber=jobmax+1
   for i in options.files:
      fileextention=i.split('.')[-1] #keep the extention for futur releases
      jobname='j'+str(jobnumber)+'.'+fileextention
      if len(filelist)!=0:
         while jobname in filelist: # just to make shure we do not have double names
            jobnumber=jobnumber+1
            jobname='j'+str(jobnumber)+'.'+fileextention
      jobnumber=jobnumber+1
      try:
         shutil.copyfile(i, os.path.join(options.path,jobname)) # copy the job to the jobdirectory
         options.jobs[jobname]=i # put it in the job list
         if options.verbose>0:
            print 'created job ', jobname, ' from file ', i
      except:
         print "could not copy job", i, "to the jobdirectory",options.path

def observe_jobs(options):
   # we will observe all jobs until they are finished
   jobs_to_finish=copy.copy(options.jobs)
   while len(jobs_to_finish)!=0:
      # get all files from the job directory
      templist=os.listdir(options.path)
      jobs_old=copy.copy(jobs_to_finish)
      for i in jobs_old:
         # look for the .fin files
         finname=str(i).split('.')[0]+'.fin'
         if finname in templist:
            # the job is finished, remove it from the list
            del jobs_to_finish[i]
            if options.verbose>0:
               print 'job finished: ',i,options.jobs[i]
      # sleep 30 seconds
      if len(jobs_to_finish)!=0:
         time.sleep(30)
   
      
def main():
   options=programm_options()
   print options.path
   define_options(options)
   copy_jobs(options)
   observe_jobs(options)
   return 1

if __name__ == "__main__":
    main()
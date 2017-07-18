#!/usr/bin/python

# This script generates templates for level 1 analysis performed after ICA-AROMA. Adapted from Jeanette Mumford.

import os, zipfile
import glob

# Set this to the directory all of the sub### directories live in
studydir = 'D:/'
extension = ".zip"

os.chdir(studydir) # change directory from working dir to dir with files

#Unzips all of the zipped files in the directory
for item in os.listdir(studydir): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(studydir) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file

# Set this to the directory where you'll dump all the fsf files
# May want to make it a separate directory, because you can delete them all once Feat runs
os.system('mkdir %s/fsf_1stLev'%(studydir))
fsfdir='/Desktop/lev1_fsf'

# Get all the paths!  Note, this won't do anything special to omit bad subjects
subdirs=glob.glob("%s/*/*[LR][RL]/ICA*"%(studydir))

for dir in list(subdirs):
	splitdir = dir.split('/')
	# YOU WILL NEED TO EDIT THIS TO GRAB sub001
	splitdir_sub = splitdir[4]
	subnum=splitdir_sub[:]
	#  YOU WILL ALSO NEED TO EDIT THIS TO GRAB THE PART WITH THE RUNNUM
	splitdir_encoding = splitdir[5]
	encoding=splitdir_encoding[15:]
	splitdir_list = splitdir[9]
	print(subnum)

	#targetPath = '%s/D:\SUBJECTNUMBER_3T_rfMRI_REST1_fixextended.zip\SUBJECTNUMBER\MNINonLinear\Results\rfMRI_REST1_LR'%(dir)
	#if not os.path.isfile(targetPath):
	#targetPath = '%s/D:\SUBJECTNUMBER_3T_rfMRI_REST1_fixextended.zip\SUBJECTNUMBER\MNINonLinear\Results\rfMRI_REST1_LR'%(dir)
  	ntime = os.popen('fslnvols %s/denoised_func_data_nonaggr.nii.gz'%(dir)).read().rstrip()
  	replacements = {'SUBNUM':subnum, 'NTPTS':ntime, 'ENCODING':encoding}
  	with open(#"/Users/edobryakova/Documents/HCPgambling_templates/lev1_template.fsf") as infile:
    		with open("%s/lev1_ER_%s_%s.fsf"%(fsfdir, subnum, splitdir_encoding), 'w') as outfile:
        		for line in infile:
          			for src, target in replacements.items():
            				line = line.replace(src, target)
         			outfile.write(line)
  	#this will launch all feats at once
	os.system("feat %s/preprocER_%s_%s.fsf"%(fsfdir, subnum, splitdir_encoding))

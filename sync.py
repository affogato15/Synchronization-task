import os
from os import walk
import shutil
from distutils.dir_util import copy_tree
import datetime
import time
import filecmp

# Input of synchronization parameters

s=str(input('Path to the source folder: ')) # path to the source folder
r=str(input('Path to the replica folder: ')) # path to the replica folder
sessions=int(input('Number of sessions= ')) # number of sessions
interval=float(input('Interval of sync in seconds= '))

# Function, which returnes content of the folder

def folder_content(folder):
    folder=os.walk(folder)
    for path, dirs, file in folder:
        content=[path, dirs, file]
        break
    
    return content 

# Function, which copies files and folders from source directory to target one

def folder_transfer(source_path, dest_path):
    source=folder_content(source_path)
    dest=folder_content(dest_path)
 
    # Files copying 
    
    for file in source[2]:
        if file not in dest[2]:   # copies files if it are not present in a replica folder
            
            item_to_copy = r'{0}/{1}'.format(source[0], file)
            dest_path = r'{0}'.format(dest[0])
            shutil.copy(item_to_copy, dest_path)
            log.write(f'\n file "{file}" is copied to {dest[0]}')
            print(f'\n {file} is copied to {dest[0]}')
            
            
        else:                    # if files are already presented in a replica folder, it compares the content between source and replica files
                                 # and replace replica one by source one in case of non-identity
                
            source_item = ('{0}\{1}'.format(source[0], file))
            replica_item = ('{0}\{1}'.format(dest[0], file))
            
            if filecmp.cmp(source_item, replica_item, shallow=False)==False:
                
                item_to_copy = r'{0}\{1}'.format(source[0], file)
                dest_path = r'{0}'.format(dest[0])
                shutil.copy(item_to_copy, dest_path)
                log.write(f'\n file "{file}" in {dest[0]} is replaced')
                print(f'\n {file} in {dest[0]} is replaced')
    
    # Files deleting
    
    for file in dest[2]:
        if file not in source[2]:
            
            item_to_delete = ('{0}/{1}'.format(dest[0],file))
            os.remove(item_to_delete)
            print('\n {0}/{1} deleted'.format(dest[0],file))
            log.write('\n {0}/{1} deleted'.format(dest[0],file))
     
    # Folders deleting
    
    for fold in dest[1]:
        if fold not in source[1]:
            
            item_to_delete = ('{0}/{1}'.format(dest[0], fold))
            shutil.rmtree(item_to_delete)
            print('\n {0}/{1} deleted'.format(dest[0],fold))
            log.write('\n {0}/{1} deleted'.format(dest[0],fold))
    
    # Folders copying
 
    if source[1]!=[]:
        matching_folders=[]
        for folder in source[1]:
            if folder not in dest[1]:
                
                os.mkdir('{0}/{1}'.format(dest[0], folder))
                print(f'\n {folder} is copied to {dest[0]}')
                item_to_copy = r'{0}/{1}'.format(source[0], folder)
                dest_path = r'{0}/{1}'.format(dest[0], folder)
                copy_tree(item_to_copy, dest_path)
                print(f'\n everything from {item_to_copy} is copied to {dest_path}')
                log.write(f'\n folder "{folder}" is copied to {dest[0]}')
            
            # recursive part which goes deeper along directory tree and repeats itself (copies)
            
            else:
                
                lvl_down_source = str('{0}/{1}'.format(source[0],folder))
                lvl_down_dest = str('{0}/{1}'.format(dest[0],folder))
                
                folder_transfer(lvl_down_source, lvl_down_dest)

# Function which supplies repetition with specified interval                
                
def sync(source_path,dest_path, sessions, interval):
    i=1
    
    while i<=sessions:
        
        print('\n session ', i)
        log.write(f'\n session  {i}')
        
        folder_transfer(source_path,dest_path)
        i+=1
        time.sleep(interval)
        

# Creation of log file in the same directory, where script exist
        
log=open(f'{os.path.realpath(os.path.dirname(__file__))}/log.txt', 'w+')
log.write(str(datetime.datetime.now()))
log.close()

# Writing of operations into log-file 

log=open(f'{os.path.realpath(os.path.dirname(__file__))}/log.txt', 'a+')


sync(s,r,sessions,interval)

log.close()


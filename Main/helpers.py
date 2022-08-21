import os
import subprocess
import time
import sys
import re

from constants import *

def check_python_compatibility():
    
    current_python_version = sys.version_info[0]

    if current_python_version != 2:
        print("\nThis script works on Python 2\n")
        exit()

def input_blob_path(NEXUS_BLOB_PATH):

    while True:
        nexus_blob_path_input = raw_input('Please enter NXRM Blobs full path (Default ' + NEXUS_BLOB_PATH + '):')
        if ("y" == nexus_blob_path_input) or ("yes" == nexus_blob_path_input) or ("" == nexus_blob_path_input): 
            
            nexus_blob_path_input = NEXUS_BLOB_PATH

            if os.path.isdir(nexus_blob_path_input):
                break

        elif os.path.isdir(nexus_blob_path_input):
            break
        else:
            print(nexus_blob_path_input + " path does not exists.\n")
            
    return nexus_blob_path_input


def input_size(SIZE_BYTES):

    while True:
        size_input = raw_input('Please enter size in MB to show files greater than it (Default 4KB):')
        if ("y" == size_input) or ("yes" == size_input) or ("" == size_input): 
            size_input = SIZE_BYTES
            break
        try:
            float(size_input)
        except:
            print('Please enter valid input.')
            continue
        if (isinstance(float(size_input), (int, float))):
            size_input = float(size_input)*1024*1024
            break

    return size_input

def input_others():

    while True:
        blob_storage_name_input = raw_input('Please enter BLOB-STORAGE-NAME Filter (Default *):')
        if ("y" == blob_storage_name_input) or ("yes" == blob_storage_name_input) or ("" == blob_storage_name_input): 
            blob_storage_name_input = BLOB_STORAGE_NAME_FILTER
            break
        else:
            break

    while True:
        reponame_input = raw_input('Please enter REPOSITORY-NAME Filter (Default *):')
        if ("y" == reponame_input) or ("yes" == reponame_input) or ("" == reponame_input): 
            reponame_input = REPONAME_FILTER
            break
        else:
            break

    while True:
        blobname_input = raw_input('Please enter BLOB-NAME Filter (Default *):')
        if ("y" == blobname_input) or ("yes" == blobname_input) or ("" == blobname_input): 
            blobname_input = BLOBNAME_FILTER
            break
        else:
            break
    
    while True:
        contenttype_input = raw_input('Please enter CONTENT-TYPE Filter (Default *):')
        if ("y" == contenttype_input) or ("yes" == contenttype_input) or ("" == contenttype_input): 
            contenttype_input = CONTENTTYPE_FILTER
            break
        else:
            break

    while True:
        createdby_input = raw_input('Please enter CREATED-BY Filter (Default *):')
        if ("y" == createdby_input) or ("yes" == createdby_input) or ("" == createdby_input): 
            createdby_input = CREATEDBY_FILTER
            break
        else:
            break

    while True:
        creationtime_input = raw_input('Please enter CREATION-TIME Filter (Default *):')
        if ("y" == creationtime_input) or ("yes" == creationtime_input) or ("" == creationtime_input): 
            creationtime_input = CREATIONTIME_FILTER
            break
        else:
            break

    while True:
        createdbyip_input = raw_input('Please enter CREATED-BY-IP Filter (Default *):')
        if ("y" == createdbyip_input) or ("yes" == createdbyip_input) or ("" == createdbyip_input): 
            createdbyip_input = CREATEDBYIP_FILTER
            break
        else:
            break
        
    return blob_storage_name_input, reponame_input, blobname_input, contenttype_input, createdby_input, creationtime_input, createdbyip_input

def get_bytes_filepaths_with_size(nexus_blob_path, size_bytes):
    """ Return list of file paths in blob directory by file size(bytes) and size filter"""
    
    # Get list of files with size
    filepaths = []
    filepaths_bytes = []
    global size
    
    # Iterate overl all the files r = root, d = directories, f = files
    for r, d, f in os.walk(nexus_blob_path):
        for file in f:
                filepaths.append(os.path.join(r, file))

    # Re-populate list with filename, size tuples
    for i in xrange(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i]))
    
    # Filter list to get only bytes files with size    
    for i in xrange(len(filepaths)):
        file_size = float(str(filepaths[i]).split(' ')[1].replace(')',''))
        
        ### Filter only bytes file and files with size greater than equal to size_bytes
        if ("bytes" in str(filepaths[i])) and (size_bytes <= file_size) and (file_size!="") : 
            filepaths_bytes.append(filepaths[i])
            #print "\nFile Size", file_size
    
    # Delete the temporary filepaths list
    del filepaths

    #print filepaths_bytes
    return filepaths_bytes

def get_files_with_properties(filepaths_bytes):
    """ Return list of file paths in blob directory with properties """
    
    # Get list of files with properties
    filepaths_properties = []
    
    # Add headers to list
    filepaths_properties.append("BlobStorageName,"+"RepoName,"+"BlobName,"+"ContentType,"+"Size(MB),"+"CreatedBy,"+"CreationTime,"+"CreatedByIp")
    
    createdBy = ""
    size = ""
    repoName = ""
    creationTime = ""
    createdByIp = ""
    contentType = ""
    blobName = ""
    
    #Filter list to get only bytes files with size    
    for i in xrange(len(filepaths_bytes)):
        property_file_name = str(filepaths_bytes[i]).split(",")[0].replace('\'','').replace('(','').replace('bytes','properties')
        #print property_file_name

        with open(property_file_name, 'r') as file:
            
            #print(file.read())
        
            for line in file.readlines():
                #print line
                
                blob_storage_name = property_file_name.split('blobs')[1].split('/')[1]
 
                if 'repo-name=' in line:
                    repoName = line.split('=')[1].replace('\n','')                    

                if 'blob-name=' in line:
                    blobName = line.split('=')[1].replace('\n','')

                if 'content-type=' in line:
                    contentType = line.split('=')[1].replace('\n','')
                    
                if 'size=' in line:
                    size = "{:.2f}".format((float(line.split('=')[1].replace('\n',''))/1024/1024))
                    #size = line.split('=')[1].replace('\n','')
                    
                if 'created-by=' in line:
                    createdBy = line.split('=')[1].replace('\n','')
                    
                if 'creationTime=' in line:
                    creationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(str(line.split('=')[1].replace('\n',''))[:-3])))
                    
                if 'created-by-ip=' in line:
                    createdByIp = line.split('=')[1].replace('\n','')
                
            #print(blob_storage_name+","+repoName+","+blobName+","+contentType+","+str(size)+","+createdBy+","+creationTime+","+createdByIp)
                
            filepaths_properties.append(str(blob_storage_name+","+repoName+","+blobName+","+contentType+","+str(size)+","+createdBy+","+creationTime+","+createdByIp))

    return filepaths_properties

def get_filter_files_with_properties(filepaths_properties,search_blob_storage_name, search_repoName,search_blobName,search_contentType,search_createdBy,search_creationTime,search_createdByIp):

    # Get list of files with properties
    filtered_filepaths_properties = []
    
    # Add headers to list
    filtered_filepaths_properties.append(str("BlobStorageName,"+"RepoName,"+"BlobName,"+"ContentType,"+"Size,"+"CreatedBy,"+"CreationTime,"+"CreatedByIp"))
    

    for i in range(1, len(filepaths_properties)):

        blob_storage_name_filepaths_properties = filepaths_properties[i].split(',')[0]
        repoName_filepaths_properties = filepaths_properties[i].split(',')[1]
        blobName_filepaths_properties = filepaths_properties[i].split(',')[2]
        contentType_filepaths_properties = filepaths_properties[i].split(',')[3]
        size_filepaths_properties = filepaths_properties[i].split(',')[4]
        createdBy_filepaths_properties = filepaths_properties[i].split(',')[5]
        creationTime_filepaths_properties = filepaths_properties[i].split(',')[6]
        createdByIp_filepaths_properties = filepaths_properties[i].split(',')[7]

        print("Filter: Repo: \""+repoName_filepaths_properties+"\"")

        if re.search(search_blob_storage_name, blob_storage_name_filepaths_properties, re.IGNORECASE) and re.search(search_repoName, repoName_filepaths_properties, re.IGNORECASE) and re.search(search_blobName, blobName_filepaths_properties, re.IGNORECASE) and re.search(search_contentType, contentType_filepaths_properties, re.IGNORECASE) and re.search(search_createdBy, createdBy_filepaths_properties, re.IGNORECASE) and re.search(search_creationTime, creationTime_filepaths_properties, re.IGNORECASE) and re.search(search_createdByIp, createdByIp_filepaths_properties, re.IGNORECASE):
            filtered_filepaths_properties.append(blob_storage_name_filepaths_properties+","+repoName_filepaths_properties+","+blobName_filepaths_properties+","+contentType_filepaths_properties+","+size_filepaths_properties+","+createdBy_filepaths_properties+","+creationTime_filepaths_properties+","+createdByIp_filepaths_properties)

    return filtered_filepaths_properties

def generate_csv_file(blob_files_list_with_properties, OUTPUT_FILE_PATH):

    output_file_path = OUTPUT_FILE_PATH

    #Overwrite file to make it empty
    open(OUTPUT_FILE_PATH, 'w').close()

    #Opening a file in append mode to write to it all the o/p data as csv
    f = open(output_file_path, "a")

    for i in xrange(len(blob_files_list_with_properties)):

        #print blob_files_list_with_properties[i] 
        f.write(blob_files_list_with_properties[i]+"\n")
        
    f.close()

def pretty_print_output(OUTPUT_FILE_PATH):
    output_file_path = OUTPUT_FILE_PATH

    print("\n")

    #Write output on console in pretty format
    subprocess.call(["column", "-s,", "-t", output_file_path])
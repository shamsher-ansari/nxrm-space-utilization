__author__     = "Shamsher Ansari"
__version__    = "1.0"
__maintainer__ = "Shamsher Ansari"
__email__      = "shamsher.ansari5637@gmail.com"
__status__     = "Production"


"""
This Python script can be used to get Nexus Repository size utlization report.
Provides details like Blob_Storage_Name, Repository_Name, Blob_Name, Size(MB), etc.
User can also filter the output based on some criteria.
I have developed this script to simplify the Nexus Repository space utilization management.
Please feel free to reach out to me for any query/suggestion. 
"""

#Importing functions from other files
from helpers import *
from constants import *

#To avoid Broken Pipe Error
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL) 

#Check python compaitibility
check_python_compatibility()

print("")

#Accept inputs from a user.
nexus_blob_path_input = input_blob_path(NEXUS_BLOB_PATH)
size_input = input_size(SIZE_BYTES)
blob_storage_name_filter, reponame_filter, blobname_filter, contenttype_filter, createdby_filter, creationtime_filter, createdbyip_filter = input_others()

#Running the code
filepaths_bytes = get_bytes_filepaths_with_size(nexus_blob_path_input, size_input)
filepaths_with_properties = get_files_with_properties(filepaths_bytes)

#Filter the output for next steps
filter_files_with_properties = get_filter_files_with_properties(filepaths_with_properties, blob_storage_name_filter, reponame_filter, blobname_filter, contenttype_filter, createdby_filter, creationtime_filter, createdbyip_filter )

#Generate output
generate_csv_file(filter_files_with_properties, OUTPUT_FILE_PATH)

#Pretty print output report
pretty_print_output(OUTPUT_FILE_PATH)


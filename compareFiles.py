import os

#########################################################################################################
# Inputs
#########################################################################################################
rootPath_1 = r"C:\Users\m0pxnn\Desktop\visualassistant"
rootPath_2 = r"\\PNI6W11901\visualassistantcontent"


# Keep this as blank to search in all the Directories within rootPath
#foldersToCompare = ["ModlAeroUI_AeroRib"]
foldersToCompare = []

# This is the file which needs to be compared
fileToCompare = "plm_properties.json"

# Set it to false if you don't wan't to see files not having any difference
displayBinaryEqualFiles = False

#########################################################################################################
# Stores file content in a list
#########################################################################################################
def LoadFileContentInList(file):
    fileContent = []
    try:
        fileHandle = open(file)
    except:
        print ("File [%s] not found!" % file)
        return fileContent
        
    for line in fileHandle:
        fileContent.append(line)
        
    return fileContent

#########################################################################################################
# Stores full path of all files with name specified in fileToCompare and present in 
# directory rootPath + folderToCompare
#########################################################################################################
def FetchFilepathsFromDir(rootPath, folderToCompare):
    filepathsToCompare = []
    walkPath = os.path.join(rootPath, folderToCompare)
    
    for root, dirs, files in os.walk(walkPath):   
        for file in files:
            if (file == fileToCompare):
                completeFilePath = os.path.join(root, file)
                filepathsToCompare.append(completeFilePath)

    return filepathsToCompare

#########################################################################################################
# Displays the difference in the 2 files content. If there are no differences, then false is returned
#########################################################################################################
def ShowDifferences(file1, lines1, file2, lines2):
    diffFound = False
    i = 0
    
    # lines1 has fewer lines
    for line2 in lines2:
        if (i < len(lines1)):
            line1 = lines1[i]
        else:
            line1 = "<NO CONTENT>"
        
        if (line1 != line2):
            diffFound = True
            print ("File 1>> %s:%d" % (file1, i+1))
            print (line1)
            print ("File 2>> %s:%d" % (file2, i+1))
            print (line2)           
            print ("---------------------------------------------------------------------------------------")    
        i = i + 1

    return diffFound
        

#########################################################################################################
# Find out common files in the list of the 2 files provided and determine differences in content of
# the corresponding files. returns a stat of files compared, same files and different files.
#########################################################################################################
def OperateOnCommonFiles(files1, files2):
    count_sameFiles = []
    count_diffFiles = []
    count_filesCompared = []

    for file1 in files1:
        # Determine the relative file path 
        relativeFilePath1_list = file1.split('\\')
        relativeFilePath1_list = relativeFilePath1_list[-3:]
        relativeFilePath1 = '\\'
        relativeFilePath1 = relativeFilePath1.join(relativeFilePath1_list)
        
        for file2 in files2:
            # Determine the relative file path 
            relativeFilePath2_list = file2.split('\\')
            relativeFilePath2_list = relativeFilePath2_list[-3:]
            relativeFilePath2 = '\\'
            relativeFilePath2 = relativeFilePath2.join(relativeFilePath2_list)
            
            if (relativeFilePath1 == relativeFilePath2):
                lines1 = LoadFileContentInList(file1)
                lines2 = LoadFileContentInList(file2)
                count_filesCompared.append(relativeFilePath1)
                
                if (len(lines1) and len(lines2)):
                    # Now compare content of these 2 files
                    if len(lines1) < len(lines2):
                        diffFound = ShowDifferences(file1, lines1, file2, lines2)
                    else:    
                        diffFound = ShowDifferences(file2, lines2, file1, lines1)

                    if (not diffFound):
                        count_sameFiles.append(relativeFilePath1)
                        if (displayBinaryEqualFiles):
                            print ("\nComparing...\n%s and \n%s"%(file1, file2))
                            print ("**** NO DIFF FOUND ***")
                    else:
                        count_diffFiles.append(relativeFilePath1)

    return count_filesCompared, count_sameFiles, count_diffFiles

#########################################################################################################
# Compare folders
#########################################################################################################
def CompareFolders(rootPath_1, rootPath_2, folderToCompare):
    filepaths1 = FetchFilepathsFromDir(rootPath_1, folderToCompare)
    filepaths2 = FetchFilepathsFromDir(rootPath_2, folderToCompare)
    return filepaths1, filepaths2

#########################################################################################################
# M A I N
#########################################################################################################
filepathsToCompare1 = []
filepathsToCompare2 = []

if len(foldersToCompare):
    # Check in specified folders only
    print ("*** Checking in folders:")
    print (*foldersToCompare, sep='\n')
    for folderToCompare in foldersToCompare:
        filepaths1, filepaths2 = CompareFolders(rootPath_1, rootPath_2, folderToCompare)       
        filepathsToCompare1 = filepathsToCompare1 + filepaths1
        filepathsToCompare2 = filepathsToCompare2 + filepaths2    
else:
    # If no folder is specified, then check in all subfolders
    print ("*** Checking in all sub-directories within root directories:\n%s and\n%s\n" % (rootPath_1, rootPath_2))  
    folderToCompare = ""
    filepathsToCompare1, filepathsToCompare2 = CompareFolders(rootPath_1, rootPath_2, folderToCompare)


# Prepare a list of files which are common in both rootPaths
if len(filepathsToCompare1) < len(filepathsToCompare2):
    count_filesCompared, count_sameFiles, count_diffFiles = OperateOnCommonFiles(filepathsToCompare1, filepathsToCompare2)
else:
    count_filesCompared, count_sameFiles, count_diffFiles = OperateOnCommonFiles(filepathsToCompare2, filepathsToCompare1)
    
print ()    
print ("+--------------------------------------------------------------------------------------------+")
print ("|                               Comparison Details                                           |")    
print ("+--------------------------------------------------------------------------------------------+")
print ("| Files compared     : ", len(count_filesCompared))
print ("| Binary equal files : ", len(count_sameFiles))
print ("| Files having diff  : ", len(count_diffFiles))
print('\n'.join('|   {}) {}'.format(*k) for k in enumerate(count_diffFiles)))
print ("+--------------------------------------------------------------------------------------------+")



The script which executes synchronization of source and replica folders.
Inputs are pathes to source and replica folders, number of sync. sessions and interval between sessions.
Script scans replica folder and compare list of names of files and folders inside, copies files and folders if they are absent in destination folder and delete it if some are not present in source folder.
In case of the the same file name it checks whether the content is the same. If not, it replaces files with ones from the source.
There is recursive algorithm implemented, which allows to scan subfolders in case of the same name and execute mentioned operations to them. 
Output is log.txt file, which contains time of the script run, numbers of sessions and corresponding operations on files and folders with its pathes.

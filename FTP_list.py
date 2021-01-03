import ftplib
import sys
import os
import io

#------------constants------------------

sites=[]

sites.append(['192.168.100.2','nicolas','nicolas'])

selected_site_index=0

site= sites[selected_site_index]

sub_dir= '' # '/sub-directory



file_report= "report.txt"



#-end------------constants---------------



site_url= site[0]

site_user= site[1]

site_pass= site[2]

report= os.path.join(os.path.curdir , file_report)



ftp = ftplib.FTP(site_url)

ftp.login(site_user, site_pass)





def clear_file_report():

    if os.path.exists (report):

        print("Removing the old report file")

        os.remove(report)

    else:

        print("Creating a new report file")



    append("FILE LIST") 



def append(text, ):

    if os.path.exists (report):

        f = open(report, "a")

    else:

        f = open(report, "w")

    f.write ("%s\b"%text)

    f.close()

  

def list_all_ftp_files(ftp, dir):
        print("hey")
        
        stream = io.StringIO()
        sys.stdout = stream
        print("hey")
        ftp.nlst(dir)
        streamed_result = stream.getvalue()
        non_dirs = []
        dirs = []
        reduced = [x for x in streamed_result.split(' ') if x != '']
        reduced = [x.split('\n')[0] for x in reduced]
        indexes = [ix + 1 for ix,x in enumerate(reduced) if x == '<DIR>']
        folders = [reduced[ix] for ix in indexes]
        #files = ftp.mlsd(sub_dir)
        if dir == '/':
            non_folders = [x for x in ftp.nlst() if x not in folders]
        else:
            non_folders = [x for x in ftp.nlst(dir) if x not in folders]
            non_folders = [dir + '/' + x for x in non_folders]
            folders = [dir + '/' + x for x in folders]
          
        if dirs == []:
            dirs.extend(folders)
        if non_dirs == []:
            non_dirs.extend(non_folders)
  
        if len(folders) > 0:
            for sub_folder in sorted(folders):
                result = list_all_ftp_files(ftp, sub_folder)
                dirs.extend(result[0])
                non_dirs.extend(result[1])
        return non_dirs          

def process():
    files = []
    clear_file_report()
    files = list_all_ftp_files(ftp , sub_dir)
    
    for f in files:

       print("Writing:%s" % f)
       append(f)

if __name__ == "__main__":

    process()
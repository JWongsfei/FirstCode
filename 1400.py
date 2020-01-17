from ftplib import FTP
import re
import datetime


class MyFTP(FTP):
    encoding = "gbk"
    def getSubdir(ftp):
        cmd = 'LIST'
        files = []
        ftp.retrlines(cmd, files.append)
        return files

    def getdirs(ftp, dirname=None):
        if dirname != None:
            ftp.cwd(dirname)
        files = ftp.getSubdir()
        r_files = [file.split(" ")[-1] for file in files]
        return [file for file in r_files if file != "." and file !=".."]

    def FtpConnect(ftp, HOST, PORT, USER, PASSWORD):
        print("FTP connection...")
        try:
            #ftp = FTP()
            ftp.connect(HOST,PORT)
        except (socket.error, socket.gaierror) as e:
            print('Error, cannot reach ' + HOST)
            return
        else:
            print('Connect To Host Success...')
        try:
            ftp.login(USER,PASSWORD)
        except Exception as e:
            print('Username or Password Error')
            ftp.quit()
            return
        else:
            print('Login Success')
        return ftp

    def FtpUpload(ftp, remotepath, localpath):
        tag = False
        ftp.cwd('/booking/')
        data1 = ftp.getdirs('/booking/')
        for i in data1:
            match2 = re.search(r'.*20200113-20200117.*', i)
            if match2:
                date = match2.group(0)
                ftp.cwd(date)
                data3 = ftp.getdirs()
                for i in data3:
                    match3 = re.search(r'.*TEM-1400.*', i)
                    if match3:
                        equipment = match3.group(0)
                        ftp.cwd(equipment)
                        data4 = ftp.getdirs()
                        for i in data4:
                            match4 = re.search(r'.*3_0830-1130.*', i)
                            if match4:
                                time = match4.group(0)
                                ftp.cwd(time)
                                ftp.storbinary('STOR %s' % remotepath, open(localpath, 'rb'))
                                ftp.quit()
                                print('3_0800-1200 Upload Success...')
                                tag = True
                                break
                        break
                break
        if tag:
            return True

if __name__== "__main__":
    starttime = datetime.datetime.now()
    HOST = 'xxx'
    PORT = xx
    USER = 'xxx'
    PASSWORD = 'xxx'
    ftp = MyFTP()
    remotepath = 'FTP FILENAME'
    localpath = 'LOCAL PATH'
    connect = 0
    TotalTag = False
    while True:
        connect = connect+1
        print('连接ftp第%d次' %connect)
        ftp.FtpConnect(HOST, PORT, USER, PASSWORD)
        for j in range(100):
            j = j+1
            print('第%d次查找' %j)
            if (ftp.FtpUpload(remotepath, localpath)):
                TotalTag = True
                break
        if TotalTag:
            break
    endtime = datetime.datetime.now()
    totaltime = (endtime - starttime).seconds * 1000000 + (endtime - starttime).microseconds
    print('time = %s 微秒' %totaltime)

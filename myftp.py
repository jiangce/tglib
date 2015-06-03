# -*- coding: utf-8 -*-

import ftplib
import os
from socket import _GLOBAL_DEFAULT_TIMEOUT


class MyFTP(object):
    def __init__(self, ip='localhost', port=0, name='', password='',
                 encoding='utf-8', timeout=_GLOBAL_DEFAULT_TIMEOUT):
        """用于下载或上传FTP服务器文件的类"""
        self._ip = ip
        self._port = port
        self._name = name
        self._password = password
        self._encoding = encoding
        self._timeout = timeout

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """关闭ftp连接"""
        if '_ftp' not in self.__dict__.keys():
            return
        try:
            self._ftp.quit()
        except:
            pass
        finally:
            self._ftp.close()
            del self._ftp

    def connect(self):
        """连接并登陆ftp服务器"""
        self.close()
        self._ftp = ftplib.FTP()
        self._ftp.encoding = self._encoding
        self._ftp.connect(self._ip, self._port, self._timeout)
        self._ftp.login(self._name, self._password)

    def dir(self):
        """返回ftp服务器当前目录的文件和文件夹列表"""
        buffer = []
        self._ftp.dir(buffer.append)
        return [('d' if i.startswith('d') else 'f', i[49:]) for i in buffer]

    def getdirs(self):
        """返回ftp服务器当前目录下所有文件夹名称"""
        return [i[-1] for i in self.dir() if i[0] == 'd']

    def getfiles(self):
        """返回ftp服务器当前目录下所有文件名称"""
        return [i[-1] for i in self.dir() if i[0] == 'f']

    def cd(self, path):
        """改变ftp服务器当前目录"""
        self._ftp.cwd(path)

    def download(self, filename, localpath, newname=None):
        """下载ftp服务器当前目录下指定文件到本地目录"""
        newname = newname or filename
        if not os.path.isdir(localpath):
            if os.path.exists(localpath):
                raise Exception('目标已存在，但并非目录')
            else:
                os.mkdir(localpath)
        fullname = os.path.join(localpath, newname)
        tmpname = fullname + '.tmp'
        if os.path.exists(fullname):
            os.remove(fullname)
        try:
            with open(tmpname, 'ab') as _downloadfile:
                def _downloadcallback(data):
                    _downloadfile.write(data)

                self._ftp.retrbinary('RETR %s' % filename, _downloadcallback)
            os.rename(tmpname, fullname)
        except:
            if os.path.exists(tmpname):
                os.remove(tmpname)
            raise

    def delfile(self, filename):
        """删除ftp服务器当前目录下的指定文件"""
        self._ftp.delete(filename)

    def rename(self, oldname, newname):
        """将ftp服务器当前目录下的文件更名"""
        self._ftp.rename(oldname, newname)

    def upload(self, fullname, newname=None):
        """向ftp服务器的当前目录传送文件"""
        if not (os.path.exists(fullname) and os.path.isfile(fullname)):
            raise Exception('文件不存在或不是文件')
        filename = newname or os.path.basename(fullname)
        tmpname = filename + '.tmp'
        if filename in self.getfiles():
            self.delfile(filename)
        with open(fullname, 'rb') as _uploadfile:
            self._ftp.storbinary(r'STOR %s' % tmpname, _uploadfile)
        self.rename(tmpname, filename)
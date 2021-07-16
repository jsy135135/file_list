from flask import Flask, render_template, send_from_directory
import os
import time

from werkzeug.utils import redirect
app = Flask(__name__)

dirpath = 'list'


def size_format(size):
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size/1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size/1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size/1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size/1000000000000) + 'TB'

@app.route("/",methods=['GET'])
def index():
    return redirect('/list')

@app.route("/list", methods=['GET'])
def list():
    filelist = os.listdir(dirpath)
    new_filelist = []
    for i in filelist:
        filepath = os.path.join(dirpath, i)
        fileinfo = os.stat(filepath)
        filedict = {}
        filedict['filename'] = i
        filedict['mtime'] = time.ctime(fileinfo.st_mtime)
        filedict['filepath'] = filepath
        if os.path.isdir(filepath):
            filedict['size'] = '-'
        else:
            filedict['size'] = size_format(fileinfo.st_size)
        new_filelist.append(filedict)
    return render_template('list.html', filedata=new_filelist, current_path=dirpath,parent_path=dirpath)


@app.route("/list/<path:filename>", methods=['GET'])
def getfile(filename):
    if os.path.isdir(os.path.join(dirpath, filename)):
        new_dirpath = os.path.join(dirpath, filename)
        filelist = os.listdir(new_dirpath)
        new_filelist = []
        for i in filelist:
            filepath = os.path.join(new_dirpath, i)
            fileinfo = os.stat(filepath)
            filedict = {}
            filedict['filename'] = i
            filedict['mtime'] = time.ctime(fileinfo.st_mtime)
            filedict['filepath'] = filepath
            if os.path.isdir(filepath):
                filedict['size'] = '-'
            else:
                filedict['size'] = size_format(fileinfo.st_size)
            new_filelist.append(filedict)
        return render_template('list.html', filedata=new_filelist, current_path=new_dirpath.replace('\\', '/'), parent_path=os.path.dirname(new_dirpath).replace('\\', '/'))
    else:
        print('='*20)
        print(dirpath,filename)
        return send_from_directory(dirpath,'', filename=filename)

if __name__ == '__main__':
    print(app.url_map)
    app.run("0.0.0.0", port=8000, debug=True)

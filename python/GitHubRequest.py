import urllib.request
import base64
import sys
import os

def GitHubRequest(repository, credentials, url, data=None, datatype=None, useRawURL=False ):
    if isinstance(credentials,str):
        credentials = bytes(credentials,'UTF-8')
    if useRawURL == True:
        requesturl = url
    else:
        requesturl = "https://api.github.com/repos/%s/%s" % (repository, url)
    
    print("request: %s" % requesturl)
    #GET request
    if data==None:
        req = urllib.request.Request(requesturl)
    else: #PUT request
        if datatype==None:#JSON POST request
            req = urllib.request.Request(requesturl, data=bytes(data,'UTF-8'))
        else: #File POST request
            filehandle = open(data,'rb')
            req = urllib.request.Request(requesturl, data=filehandle)
            filesize = os.path.getsize(data)
            req.add_header("Content-Length", "%d" % filesize)
            if isinstance(datatype,str):
                req.add_header("Content-Type", datatype)
            else:
                req.add_header("Content-Type", "application/octet-stream")
    if credentials!=None:
        base64str = base64.b64encode(credentials)
        req.add_header("Authorization", "Basic %s" % base64str.decode("utf-8"))
    
    try:
        handle = urllib.request.urlopen(req)
    except IOError as e:
        code = -1
        if hasattr(e,'code'):
            code = e.code
        message = str()
        if hasattr(e,'fp'):
            message = e.fp.read()
        if 'filehandle' in locals():
            filehandle.close()
        return message, code
    response = handle.read()
    if 'filehandle' in locals():
        filehandle.close()
    return response, handle.getcode()
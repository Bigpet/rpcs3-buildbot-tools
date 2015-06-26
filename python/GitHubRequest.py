import urllib.request
import base64
import sys
import os

def GitHubRequest(repository, credentials, url, data=None, datatype=None, useRawURL=False ):
    """ GitHubRequest(repository, credentials, url, data=None, datatype=None, useRawURL=False ) -> response, returncode
    
    This function is thoroughly unpythonic and you should probably just use it
    as a starting point.
    It dispatches a request to the GitHub API (written with v3 in mind).
    A GET request if data is not specified, a POST request with the string in
    data if datatype is not specified and a POST request with the contents of
    the filename in data if datatype is specified.
    
    Arguments:
        repository  - GitHub with in the format 'User/Repository'
        credentials - GitHub username and personal access token in the format
                      'username:accesstoken'
        url         - the GitHub API url, for example 'issues/3' or a complete
                      url if useRawURL is set to True
        data        - string specifying the data to be send, if datatype is
                      None the string is send, otherwise a file with the name
                      is opened and sent
        datatype    - the type of data to be, if it's a str it will be used as
                      MIME type for the POST request, if it't not a str or 
                      NoneType then the MIME type will be 'application/octet-stream'
        useRawURL   - specify whether the url is the full request URL (when
                      True) or just a partial url to append to 'apiurl/repo/'
    """
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
    else: #POST request
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
#!/usr/bin/env python

from GitHubRequest import GitHubRequest
import urllib.request
import base64
import sys
import os
import json

def main():
    if len(sys.argv) < 4:
        print("usage: python upload_release_asset.py repository file releasename [commitish]")
        print(" ")
        print(' repository : GitHub repository link in the format "user/repository" (without quotes)')
        print(' file : file in the working directory')
        print(' releasename : name for the release tag')
        print(' commitish : (optional) commitish for the release to create')
        sys.exit(1)
    repository  = sys.argv[1]
    filename    = sys.argv[2]
    releasename = sys.argv[3]
    if len(sys.argv) >= 5:
        commitish = sys.argv[4]
    else:
        commitish = None
    
    #repo = "Bigpet/rpcs3-buildbot-tools"
    credentials = bytes(os.environ['GITHUB_CREDENTIALS'],'UTF-8')
    
    #Check if the tag already exists
    response, code = GitHubRequest(repository,credentials,"releases/tags/%s"%releasename)
    print("code: %d"%code)
    if code == 200: #already a release with this tag there
        #expected
        code = 200 #do nothing
    elif code == 404: #no release with this tag yet
        #Create release
        requestdict = {'tag_name': releasename, 'prerelease': True}
        if commitish != None:
            requestdict['target_commitish'] = commitish
        response, code = GitHubRequest(repository,credentials,'releases',json.dumps(requestdict))
        if code != 201:
            print("got unexpected return code %d while creating a release: %s"%(code,response),file=sys.stderr)
            sys.exit(1)
    else:
        print("got unexpected return code %d while looking for release: %s"%(code,response),file=sys.stderr)
        sys.exit(1)
    
    #Get upload_url
    resdict = json.loads(response.decode('utf-8'))
    upload_url = resdict['upload_url']
    upload_url = upload_url.replace('{?name}',"?name=%s"%filename)
    
    assets = resdict['assets']
    for asset in assets:
        if asset["name"]==filename:
            print("File %s already exists in tag %s"%(filename,releasename),file=sys.stderr)
            sys.exit(1)
    
    #consider just using "application/octet-stream" for generic files
    response, code = GitHubRequest(repository,credentials,upload_url,filename,"application/zip",True)
    if code != 201:
        print("got unexpected return code %d while trying to upload asset to release: %s"%(code,response),file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

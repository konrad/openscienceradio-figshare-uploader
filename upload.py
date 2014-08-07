#!/usr/bin/python3

"""
Copyright (c) 2014, Konrad Foerstner <konrad@foerstner.org>

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

"""

__description__ = ""
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2014 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = ""

import requests
from requests_oauthlib import OAuth1
import json

def main():
    # SOME TEST DATA
    title = "OSR test"
    description = "Very long OSR Newdump"
    links = ["http://openscienceradio.de/666", "http://www.archive.org/666"]
    tags = ["Open Science", "Podcast"]

    osr_figshare_uploader = OSRFigsharUploader("client_auth_etc.json")
    osr_figshare_uploader.create_article(title, description, "dataset")
    osr_figshare_uploader.upload_file(title, description)
    osr_figshare_uploader.add_links(links)
    osr_figshare_uploader.add_tags(tags)
    osr_figshare_uploader.write_article_info()

class OSRFigsharUploader():

    """
    The credential file must be in JSON and look like this:
      {"client_key": "BLA",
       "client_secret": "BLUB",
       "token_key": "BOING",
       "token_secret": "ZOFF"}
    """

    def __init__(self, creditial_file, shutup=False):
        creditials = json.load(open(creditial_file))
        self._oauth = OAuth1(client_key=creditials["client_key"], 
                       client_secret=creditials["client_secret"],
                       resource_owner_key=creditials["token_key"], 
                       resource_owner_secret=creditials["token_secret"],
                       signature_type = 'auth_header')
        self._client = requests.session()
        self._article_id = None
        self._shutup = shutup

    def create_article(self, title, description, defined_type):
        """Create new draft article 
        
        It won't be listed in the dashboard until a file is uploaded!
        
        """

        body = {'title' : title,'description' : description, 
                'defined_type' : defined_type}
        headers = {'content-type':'application/json'}
        response = self._client.post(
            'http://api.figshare.com/v1/my_data/articles', auth=self._oauth,
            data=json.dumps(body), headers=headers)
        results = response.json()
        self._article_id = results["article_id"]
        if not self._shutup:
            print(results)

    def upload_file(self, title, description):
        file_name = "%s.txt" % (title.replace(" ", "_"))
        file_content = "%s\n%s" % (title, description)
        files = {'filedata':(file_name, file_content)}
        response = self._client.put(
            'http://api.figshare.com/v1/my_data/articles/%s/files' 
            % self._article_id, auth=self._oauth, files=files)
        results = response.json()
        if not self._shutup:
            print(results)

    def add_links(self, links):
        for link in links:
            body = {'link' : link}
            headers = {'content-type':'application/json'}
            response = self._client.put(
                'http://api.figshare.com/v1/my_data/articles/%s/links' % 
                self._article_id, auth=self._oauth, data=json.dumps(body), 
                headers=headers)
            results = response.json()
            if not self._shutup:
                print(results)

    def add_tags(self, tags):
        for tag in tags:
            body = {'tag_name' : tag}
            headers = {'content-type':'application/json'}
            response = self._client.put(
                'http://api.figshare.com/v1/my_data/articles/%s/tags' % 
                self._article_id, auth=self._oauth, data=json.dumps(body), 
                headers=headers)
            results = response.json()
            if not self._shutup:
                print(results)

    def write_article_info(self, article_id=None):
        if article_id is None:
            article_id = self._article_id
        response = self._client.get(
            'http://api.figshare.com/v1/my_data/articles/%s' % article_id, 
            auth=self._oauth)
        results = response.json()
        print(results)
                
if __name__ == "__main__": 
    main()

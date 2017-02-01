#!/usr/bin/env python
#
# Copyright 2017 The Fuchsia Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# A script to fetch missing LICENSE files when building a vendored repo

# Should be run from top-level of third_party/rust-crates repository.

import os
import re
import sys
import urllib2

repo_re = re.compile('\s*repository\s*=\s*"(.*)"\s*$')

def die(reason):
    sys.stderr.write(reason + '\n')
    sys.exit(1)

def get_repo_path(subdir):
    # TODO: workarounds for missing repo; delete when crate is updated
    if subdir == 'xi-core-lib-0.1.0': return 'https://github.com/google/xi-editor'
    for line in open(os.path.join(subdir, 'Cargo.toml')):
        m = repo_re.match(line)
        if m:
            return m.group(1)

def find_github_blob_path(path):
    s = path.split('/')
    if s[2] == 'github.com':
        s[2] = 'raw.githubusercontent.com'
    else:
        die("don't know raw content path for " + path)
    if s[-2] == 'tree':
        del s[-2]
    else:
        s.append('master')
    return '/'.join(s)

def fetch_license(subdir):
    repo_path = get_repo_path(subdir)
    print 'fetching license for ' + subdir + ': ' + repo_path
    if repo_path is None: die("can't find repo path for " + subdir)
    baseurl = find_github_blob_path(repo_path)
    text = []
    for license_filename in ('LICENSE', 'LICENSE-APACHE', 'LICENSE-MIT'):
        url = '/'.join((baseurl, license_filename))
        try:
            resp = urllib2.urlopen(url)
            contents = resp.read()
            if text: text.append('=' * 40 + '\n')
            text.append(url + ':\n\n')
            text.append(contents)
        except urllib2.HTTPError:
            pass
    if not text:
        die('no licenses found under ' + baseurl)
    else:
        license_out = open(os.path.join(subdir, 'LICENSE'), 'w')
        license_out.write(''.join(text))

def main():
    for subdir in os.listdir(os.getcwd()):
        if subdir.startswith('.') or not os.path.isdir(subdir): continue
        license_files = [file for file in os.listdir(subdir) if file.startswith('LICENSE')]
        if not license_files:
            fetch_license(subdir)

if __name__ == '__main__':
    main()

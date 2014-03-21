#!/usr/bin/env python

from optparse import OptionParser
import os.path
import subprocess
import hglib

def run_conversions(repos_txt, source, target, shas, force=False):
    repos = filter(None, open(repos_txt).read().split())
    for repo in repos:
        convert(repo, source, target, shas, force=force)


def convert(repo_path, source, target, shas, force=False):
    source_repo_p = os.path.join(source, repo_path)
    target_repo_p = os.path.join(target, repo_path)
    try:
        client = hglib.open(source_repo_p)
    except hglib.error.ServerError:
        client = hglib.clone('https://hg.mozilla.org/integration/' + repo_path,
                             source_repo_p,
                             noupdate=True, rev='tip')
        
    if not client.incoming(revrange='tip'):
        if not force:
            print repo_path, 'is cool'
            return
    else:
        client.pull(rev='tip')
    print 'converting', repo_path
    client.close()
    cmd = ['hg', 'gaiaconv', source_repo_p, target_repo_p,
           os.path.join(shas, repo_path)]
    print cmd
    subprocess.call(cmd)


if __name__=='__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 4:
        parser.error('Call with repos.txt source target shamaps')
    run_conversions(*args)

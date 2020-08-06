Tracking 167287.
#### Comparing your local copy
Have python3 installed and save the `diff.py` file.

Run script on a username and local directory
```
$ python diff.py e1.1iott ~/downloads/tiktok/el
Fetching Name Mapping...
Fetching Post Records for e1.1iott 6655930169944227846
Scanning post directory...
Local:   93 posts
Remote:  80 posts
Missing: 9 posts
Private: 22 posts
Print 31 missing/private post ids?
```
Missing posts are those that are not saved locally but are in the remote table.

Private posts are those that are saved locally but are not in the remote table.

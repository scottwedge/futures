cd /futures && git checkout master
git config --global alias.up '!git remote update -p; git merge --ff-only @{u}'
git up
python ./futures.py

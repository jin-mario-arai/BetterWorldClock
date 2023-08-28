

##Build instruction for Mac OS

You might want to consider setting up virtual env with venv or conda before proceeeding.
```
pip install -r requirements.txt -r requirements.mac.txt
python3 -m py2app
open dist
```
You should see "Better World Clock" app in the dist folder.

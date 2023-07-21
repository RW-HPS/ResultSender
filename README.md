# GameResultSender
This is a simple script written for RW-HPS on linux with the following features:
>Server daily restart based on system time (this will fix bugs caused by running the server for too long)

>Server restart notification

>Post replay result to discord channel via webhook

>upload replay file to discord channel via webhook

>Send script error exceptions to discord channel via webhook


**Requirements:**

open the terminal in the folder

linux
```
sudo apt install screen
sudo apt install curl
```

python
```
pip install -r requirements.txt
```

**How to use?**

Move `RW-HPS-[version]` to the folder `Server/`

replace authcookie, discord webhook, `RW-HPS folder name (case sensitive)` in `Server/send.py`

replace webhook in `start.sh`

and run `start.sh`
```
bash start.sh
```


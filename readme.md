# Get Started
To get started, first install the latest version of Python
- [Download Python](https://www.python.org/downloads/)
- Follow the on-screen instructions

#### Verify Python Installation
Open your command line (Close and open your command line again if you have 1 opened already). You can do so by:
- &#8862; + CMD (You should see `Command Prompt`) + Enter
- Type `python` or `python3` (Depending on the alias you set). You should see the following:
```cmd
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
This means Python has been installed successfully.
#### ⚠️ What If I Do Not See The Above?
Don't worry, that means there are no environment variables set on your computer. Do the following:
- Locate the Python executable on your computer using Windows Explorer. It is normally located in `C:\Users\<username>\AppData\Local\Programs\Python\<pythonVersion>\python.exe`
- Copy the path of this file. Click on `python.exe` **ONE TIME** so it is **HIGHLIGHTED**
- On the top of Windows Explorer, you should see `Home` tab. Within this tab, click on `Copy path` (If you prefer to just click on the path link on the URL tab go ahead they work the same)
- Open your system environment variables:
  - &#8862; + env (You should see `Edit the system environment variables`) + Enter
  - Click on `Environment Variables...` at the bottom of the page
  - Under `System variables` find `PATH` (**CASE-SENSITIVE**) and select it. You should see a new window.
  - Click `New` on the right hand side. Paste your python path link you copied in step 1.
- **RESTART ALL COMMAND LINE INTERFACES FOR IT TO TAKE EFFECT**

Open your command line. You can do so by:
- &#8862; + CMD (You should see `Command Prompt`) + Enter
- Type `python` or `python3` (Depending on the alias you set). You should see the following:
```cmd
Python 3.13.5 (tags/v3.13.5:6cb20a2, Jun 11 2025, 16:15:46) [MSC v.1943 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
This means Python has been installed and linked successfully.

## Install Dependencies
All Python installations above come with `pip`. Install all dependencies just by simply running in the command line:
```cmd
pip install -r requirements.txt
```
NOTE: If you need dependencies, just write them in the file (`requirements.txt`) and run the code above again

## [🚧 WIP] Run The Scripts
For convenience, `main.py` is the start script. You can rename to whatever it is. This script will likely be the entrypoint for the backend + frontend server.

#### - `model/` Folder
This folder contains all business logic code. This is where we will do majority of the backend processing code.

#### - `router/` Folder
This folder contains the API interface code. This is where frontend from `static/` will interact with and this will execute code in `model/` and return any data back to the frontend.

#### - `static/` Folder
This folder contains all the HTML code for the frontend.
# Requirements
1. Git
2. Python 3+
3. Powershell

# Installation
First, clone the repo.

```sh
git clone https://github.com/Cheespeasa1234/spotify-bpm
```

Then, navigate to the repository. 
```sh
cd spotify-bpm
```

Then, install the python requirements in a venv.
```sh
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Next, generate the gifs for each BPM.
```sh
mkdir static/dance
powershell .\generate_gifs.ps1
```

Last, you need your environment variables. Run the following:
```sh
echo "" > .env
```

First, go to `developer.spotify.com` and click your profile dropdown, then click Dashboard. Click Create App. 

Set the app name and description to whatever you want. Leave the website blank. Then set the Redirect URI to `http://127.0.0.1:5001/callback`, and Add it. Click the checkbox for `Web API`. Accept the terms and Save.

Back in the dashboard, click on the app you just made. Look for the Client ID. Also look for the client secret. Open the .env file and put in the following:

```conf
CLIENT_ID=<your client ID>
CLIENT_SECRET=<your client secret>
REDIRECT_URI=http://127.0.0.1:5001/callback
SCOPE=user-read-currently-playing
```

# Execution

To run the server, run the following command:
```sh
python main.py
```

Then, in your browser, open the URL `http://localhost:5001/`.

# How it works
It basically uses a python Flask server to communicate with the Spotify API, to track the song the user is now playing. It uses the Flask server to communicate with a browser and send relevant information to be displayed on a webpage.

# To Do
1. Have it periodically check now playing ON THE FRONTEND to efficiently refresh page
2. Have it make the requests to Flask more on the frontend
3. Make graphics less shit
4. Have it work when it is paused
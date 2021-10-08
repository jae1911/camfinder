# Cam Finder

Find open Hipcam webcams using the [Shodan](https://shodan.io) API.

## Getting started

    git clone https://code.jae.fi/jae/cam-finder.git
    cd cam-finder
    pip install -r requirements.txt

Now copy the file `config.example.json` to `config.json` and fill in your Shodan token.

## Usage

    python finder.py <number of runs>

One run goes trough 100 webcams in total, if you request 5 runs, it will go through 500 webcams.

## How does it works

The program will query a list of supposedly open webcams using the Shodan api.  
To test if the webcam is really open (without any password or just working), we use cv2 to detect if there is a video flux on the default Hipcam endpoint `rtsp://<cam ip>:554/11`  
As of now, only Hipcams are supported but other types will come later.

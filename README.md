# hue-amp

A script for visualizing a song using your Philips hue lightbuilbs. 
This script maps the amplitude of the left & right channels of a wav file to two hue lights while playing the song.

### Setup
1. ```brew install portaudio```
2. ```pip install -r requirements.txt```
3. Get a userid and bridge-ip address using the following [instructions](http://www.developers.meethue.com/documentation/getting-started)

### Run
```
> python run.py <bridge-ip> <userid> song.wav
```

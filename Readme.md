# Find duplicate songs

I have a very messy song collection I need to categorize my local songs neatly.  
The first step is to get rid of my duplicate songs among hundreds or thousands of songs. The first task of this project is satisfying this need.  
In order to delete duplicate songs, I have implemented an extremely simple method which is detecting songs with the same duration.  
The algorithm is simple, for songs with equal duration, I compare the similarity of their text title with [SpaCy](https://spacy.io) and if they're similar up to a point we can delete them automatically.  
However, sometimes we have to check these songs manually in order to make sure everything is okay to delete duplicate ones. This script helps you to do this with an extremely non-friendly method, but that's better than nothing!

The other steps including categorizing music-based title, genre, music itself are not my concern for now!

## Requirements

In ubuntu you have to install the following package:
```bash
$ sudo apt install mediainfo
```
And install the following Python packages (Python > 3.6)
* numpy
* spacy
* pymediainfo
* glob
You also need to download English data of spacy with the following command:
```bash
python -m spacy en
```

## How to run it

In order to run it simply run the following python script:
```bash
python main.py --music_path /path/to/music-root
```
I suggest that firstly run the above command to get rid of obvious duplicate musics. But if you have time and want to clear your music collection more, you need to remove suspicious files manually with the following argument:
```bash
python main.py --music_path /path/to/music-root --interactive
```
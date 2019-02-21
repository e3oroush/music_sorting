from pymediainfo import MediaInfo
from glob import glob
from glob import iglob
import os
import spacy

nlp = None
music_extension = ['*.mp3', '*.wma', '*.FLV', '*.MP3', '*.flac', '*.MP4', '*.Mp3', '*.DAT']
def get_info(song_path):
    """Get information of a song using mediainfo
    
    Arguments:
        song_path {str} -- Path to a song
    
    Returns:
        dict -- Information on the song
    """

    metadata = MediaInfo.parse(song_path)
    useful_info = \
    {
        "album":None,
        "album_performer":None,
        "composer":None,
        "file_size":None,
        "performer":None,
        "track_name":None,
        "title":None,
        "duration":None,
        "sampling_rate":None,
        "bit_rate":None,
        "genre":None,
        "complete_name":None

    }

    for track in metadata.tracks:
        if track.track_type == 'Video':
            print("You have entered a video file??")
            return None
        for key in useful_info.keys():
            try:
                value = getattr(track,key)
                if value is not None:
                    useful_info[key] = value
            except:
                continue
    return useful_info

def get_all_song_names(path):
    """Find all songs inside a directory. It searches recursively
    
    Arguments:
        path {str} -- Path to the root of music files
    
    Returns:
        list -- A list of music file names
    """

    if path.endswith('/'):
        path=path[:-1]
    exts = list(set([p.split('.')[-1] for p in os.listdir(path)]))
    print("Available extensions are {}".format(exts))
    file_names = []
    for ext in music_extension:
        file_names+=iglob(path+'/**/'+ext, recursive=True)
    return file_names

def get_song_similar_attributes(song1,song2):
    """Compare two songs and compute the similarity of them.
    It compares text fields with `spacy` and int fields with L1 comparing
    
    Arguments:
        song1 {dict} -- Infos of song1
        song2 {dict} -- Infos of Song2
    
    Returns:
        dict -- Result of comparing between song1 and song2
    """

    global nlp
    if nlp is None:
        nlp = spacy.load("en")
    similarity={}
    for key,value in song1.items():
        value2 = song2[key]
        if value is None or value2 is None:
            similarity[key] = 0
            continue
        if type(value) == str:
            d1=nlp(value)
            d2=nlp(value2)
            similarity[key] =  d1.similarity(d2)
        elif type(value) == int or type(value) == float:
            similarity[key] = 1-abs(int(value)-int(value2))/max(value,value2)
    return similarity
from utils import get_all_song_names, get_info, get_song_similar_attributes
import numpy as np
import json
import os
from argparse import ArgumentParser


def find_duplicate_songs(path):
    """Find duplicate songs inside a directory
    
    Arguments:
        path {str} -- Path to the root of music directory
    
    Returns:
        list[dict] -- A list of information on candidate songs duplicate
    """

    all_songs = get_all_song_names(path)
    songs_info = [get_info(p) for p in all_songs]
    songs_info = [p for p in songs_info if p is not None and p['duration'] is not None]
    songs_duration = np.array([p['duration'] for p in songs_info],dtype=np.int)
    print("We got {} songs in the directory {}".format(len(songs_duration),path))
    diffs = songs_duration.reshape(-1,1) - songs_duration.reshape(1,-1)
    duplicate_inds = np.where(np.abs(diffs)<10)
    sims={}
    filter_inds = []
    for x,y in sorted(zip(*duplicate_inds),key=lambda x: x[0]):
        if x == y or x in filter_inds:
            continue
        filter_inds.append(y)
        if str(x) not in sims:
            sims[str(x)] = {
                "similarity": [get_song_similar_attributes(songs_info[x],songs_info[y])], 
                "duplicate_songs_path": [songs_info[y]["complete_name"]], 
                "song_path": songs_info[x]["complete_name"]
                }
        else:
            sims[str(x)]["similarity"].append(get_song_similar_attributes(songs_info[x],songs_info[y]))
            sims[str(x)]["duplicate_songs_path"].append(songs_info[y]["complete_name"])
    print("We found {} candidate duplicate songs".format(len(sims)))
    with open("Results.json", "w") as fh:
        json.dump(sims,fh,indent=3)
    return sims

def search_through_duplicates(candidates, interactive=True):
    """Seatch through duplicate musics and delete them automatically and manually.
    
    Arguments:
        candidates {list[dict]} -- List of information on candidate duplicate music
    
    Keyword Arguments:
        interactive {bool} -- Perform automatic deleting or manually (default: {True} Manual deleting)
    """

    remove = {'y':lambda x: os.remove(x[1]), 'n': (lambda x: x), 'd': lambda x: os.remove(x[0])}
    for c in candidates.values():
        song_path = c["song_path"]
        print("Song path: {}".format(song_path))
        for i,s in enumerate(c["duplicate_songs_path"]):
            if interactive:
                q = input("Candidate song path: {}.\nDelete it? y(yes) n(no) d(keep this and detele original file)? ".format(s))
            else:
                if c["similarity"][i]["title"] > 0.9:
                    q = 'y'
                else:
                    q = 'n'
            try:
                remove[q]([song_path,s])
            except KeyError:
                print("Wrong input!")
            except:
                print("Couldn't delete your file")
            


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--music_path", help="Base path of your musics", required=True)
    parser.add_argument("--interactive", help="Deletes all songs which have similar titles automatically or do it manually", action="store_true")
    args = parser.parse_args()
    candidates = find_duplicate_songs(args.music_path)
    search_through_duplicates(candidates, interactive=args.interactive)
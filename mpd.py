import json
import codecs
import datetime as dt
import re


def get_top_n_related_artists(artist_uri, n=3, sort_by="popularity", include_name=False):
    
    assert sort_by in ["popularity", "similarity"]
    
    related_artists = [
        (rartist["uri"], rartist["name"], rartist["popularity"]) 
        for rartist 
        in sp.artist_related_artists(artist_uri)["artists"]
    ]
    
    if sort_by=="popularity":
        related_artists = sorted(related_artists, key=lambda x: -x[-1])[:n]
    
    return [rartist[:2] if include_name else rartist[0] for rartist in related_artists[:n]]

def normalize_name(name):
    name = name.lower()
    name = name.replace("'", "")
    name = re.sub(r"[.,\/#!$%\^\*;:{}=\_`~()@]", ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def to_date(epoch):
    return dt.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d")


"""
PLAYLIST DISPLAY
"""

def print_playlist(playlist, pretty=True, compact=False):
    if pretty:
        print ('===', playlist['pid'], '===')
        print (playlist['name'])
        print ("  followers     ", f"{playlist['num_followers']:<5}")
        print ("  modified      ", f"{dt.datetime.fromtimestamp(playlist['modified_at']).strftime('%Y-%m-%d'):<5}")
        print ("  edits         ", f"{playlist['num_edits']:<5}")
        print ("  collaborative ", f"{playlist['collaborative']:<5}")
        print ("  num_artists   ", f"{playlist['num_artists']:<5}")
        print ("  num_tracks    ", f"{playlist['num_tracks']:<5}")
        print ("  duration min  ", f"{(playlist['duration_ms']/(1000*60)):<5.2f}")        
        print()
        if not compact:
            print(f"{'#':>3} | {'track':<30} | {'album':<40} | {'artist':<20}")
            print("-"*100)
            for track in playlist['tracks']:
                print(f"{track['pos']:>3} | {track['track_name'][:29]:<30} | {track['album_name'][:39]:<40} | {track['artist_name']:<20}")
#                 print ("%3d %s - %s - %s" %(track['pos'], track['track_name'], track['album_name'], track['artist_name']))
            print()
    else:
        print (json.dumps(playlist, indent=4))


def show_playlist(pid, path="data/original"):
    if pid >=0 and pid < 1000000:
        low = 1000 * int(pid / 1000)
        high = low + 999
        offset = pid - low
        path = path + "/mpd.slice." + str(low) + '-' + str(high) + ".json"
        f = codecs.open(path, 'r', 'utf-8')
        js = f.read()
        f.close()
        playlist = json.loads(js)
        
        print_playlist(playlist['playlists'][offset])


def show_playlists_in_range(start, end):
    try:
        istart = int(start)
        iend = int(end)
        if istart <= iend and istart >= 0 and iend <= 1000000:
            for pid in xrange(istart, iend):
                show_playlist(pid)
    except:
        raise
        print ("bad pid")
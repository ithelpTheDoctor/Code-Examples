import youtube_dl
import re
import requests
import os
import argparse

def downSub(video_url,language):
    # check if valid youtube_link and remove playlist ID from url if exists.
    _temp = video_url.lower()
    if 'youtube.com' in _temp or 'youtu.be' in _temp:
        if '&list=' in video_url:
            video_url = video_url.split('&list=')[0].strip()
    
    
    ydl_opts = {'dump-json':True, 
     'writesubtitles':True, 
     'writeautomaticsub':True, 
     'youtube_include_dash_manifest':False}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
            info_dict = ydl.extract_info(video_url, download=False)
            #print(info_dict)
            if not info_dict['formats']:
                print(text=' Status : Something went wrong retry or video is unavailable')              
                return
    except:
        print('Error : Check your Internet Connection or Url.')
        return
    
    
    video_title = info_dict['title']
    
    # replacing reserved characters for windows for filename.
    video_name = re.sub('[\\\\/*?:"<>|]', '', video_title)
    
    subtitles = info_dict.get('subtitles')
    automatic_captions = info_dict.get('automatic_captions')
    
    
    if subtitles:
        subtitle = subtitles.get(language)
        if subtitle:
            for fmt in subtitle:
                if fmt['ext']=='vtt':
                    sub_dlink = fmt['url']
                    return [sub_dlink,video_name]
                    
    if automatic_captions:
        subtitle = automatic_captions.get(language)
        if subtitle:
            for fmt in subtitle:
                if fmt['ext']=='vtt':
                    sub_dlink = fmt['url']
                    return [sub_dlink,video_name]
    

      
def playlist(playlist_url):
    _temp = playlist_url.lower()
    if 'youtube.com' in _temp or 'youtu.be' in _temp:
        if not 'list' in _temp:
            print('\nError : Not a Playlist.')
            return
    else:
        print('Error : Invalid Youtube Url : '+playlist_url)
        return
    playlist = []
    ydl_opts = {'extract_flat':"in_playlist", 
     'quiet':True}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
            info_dict = ydl.extract_info(playlist_url, download=False)
            
    except Exception as e:
        print(e)
        print('\n Error : Something went wrong extracting playlist, retry or try a different playlist.')
        return
        
    if len(info_dict["entries"])<1:
        print('Error : No video found in playlist, probably no public videos in the playlist.')
        return 
    for video in info_dict['entries']:
        playlist.append('https://www.youtube.com/watch?v=' + video['id'])
        
    return playlist




if __name__=="__main__":

    if not os.path.exists("subtitles"):
        os.makedirs('subtitles')
        
    parser = argparse.ArgumentParser(description='Download Subtitles for Youtube video single or playlist.')   
    parser.add_argument('-t','--type',required=True,type=int,metavar=" ",choices=range(1,3),help='"1" for single and "2" for playlist.')
    parser.add_argument('-u','--url',metavar='"{URL}"',required=True,help='Youtube video or playlist url inside Quotes.')
    parser.add_argument('-l','--language',metavar=" ",default='en',help='Language Code to download e.g., "hi" for hindi.')
    args = parser.parse_args()
    
    lang = args.language
    
    if args.type==1:
        subtitle = downSub(args.url,lang)
        if subtitle:
            r = requests.get(subtitle[0])
            with open(os.path.join('subtitles',f"{subtitle[1]}.vtt"),'wb') as f:
                f.write(r.content)
            print('\n Subtitle Downloaded Successfully.')
        
    if args.type==2:
        playlist_links = playlist(args.url)
        if playlist_links:
            print("\n Found "+str(len(playlist_links))+" videos in playlist.")
            for link in playlist_links:
                subtitle = downSub(link,lang)
                if subtitle:
                    r = requests.get(subtitle[0])
                    with open(os.path.join('subtitles',f"{subtitle[1]}.vtt"),'wb') as f:
                        f.write(r.content)
            print('\n Subtitles Downloaded Successfully.')
            
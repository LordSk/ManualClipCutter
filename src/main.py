# Manual Clip Cutter

import app_config
import requests
import sys
import os
import ffmpeg

def get_clip_info(ID):
    try:
        url = 'https://api.twitch.tv/kraken/clips/' + ID
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': app_config.app_id,
        }
        r = requests.get(url, headers=headers)
        j = r.json()
    except:
        return None
    
    return {
        'offset': j['vod']['offset'],
        'duration': j['duration'],
        'title': j['title']
    }

def cut_video(path, start, duration, output):
    try:
        (
            ffmpeg
            .input(path, ss=start, t=duration)
            .output(output)
            #.run(capture_stdout=True, capture_stderr=True)
            .run()
        )
    except:
        return None
    return True



# ------------ main ------------
if len(sys.argv) < 3:
    print('Usage:')
    print(' mcc vod_file twitch_clip_code')

vod_path = sys.argv[1]
clip_code = sys.argv[2]

print('Fetching clip info...')
info = get_clip_info(clip_code)

if info == None:
    print('Could not fetch twitch clip info for code "' + clip_code + '"')
    sys.exit(1)

print('Cutting vod...')

output_path = os.path.join(os.path.dirname(vod_path), clip_code + '.mp4')

cut = cut_video(vod_path, info['offset'], info['duration'], output_path)
if cut == None:
    print('Could not cut video "' + vod_path + '" (' + str(info) + ')')
    sys.exit(1)

print('\n\n\n\n')
print('-------------------------------')
print(info['title'])
print('duration: ' + str(info['duration']))
print('-------------------------------')
print('')
print('Written to "' + output_path + '"')
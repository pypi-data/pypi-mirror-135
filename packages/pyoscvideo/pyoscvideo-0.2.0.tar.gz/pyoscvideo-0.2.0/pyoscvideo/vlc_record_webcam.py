# coding: utf-8
import vlc
import time
import sys

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def main():
    filename = sys.argv[1]
    webcams = sys.argv[2:]
    players = []
    v = vlc.Instance()

    for i, webcam in enumerate(webcams):
        p = v.media_player_new()
        m = v.media_new(f"v4l2://{webcam}:chroma=mp2v", ":live-caching=30")
        p.set_media(m)
        p.play()
        players.append(p)
   
    def prepareRecording():
        for player in players:
            pass

    def record():
        for player in players:
            player.stop()
            m = player.get_media()
            m.add_option(f'sout=#duplicate{{dst=display,dst="transcode{{vcodec=mp2v,fps=30}}:standard{{access=file,mux=ogg,dst={filename}_{i}.mp4}}"}}')
            player.play()

    dispatcher = Dispatcher()
    dispatcher.map("/oscVideo/prepareRecording", prepareRecording)
    dispatcher.map("/oscVideo/record", record)

    server = BlockingOSCUDPServer(('0.0.0.0', '9099'), dispatcher)
    server.serve_forever()


def stop():
    for player in players:
        player.stop()

if __name__ == '__main__':
    main()

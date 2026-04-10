from torrent.parser import Torrent
from tracker.client import TrackerClient

torrent = Torrent("C:\\Users\\kannan\\Desktop\\bittorrent\\myfile.torrent")

tracker = TrackerClient(torrent)
response = tracker.get_peers()

print(response)
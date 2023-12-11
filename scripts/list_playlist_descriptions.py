from mmmusic.data.playlist_configs import regular_playlists

for playlist_config in regular_playlists:
    print(f"{playlist_config.name}: {playlist_config.description}")

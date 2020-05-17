from gmusicapi import Musicmanager
import os
import fleep

mm = Musicmanager()
mm.login()


root_music_folder = "F:/Music/"
library = mm.get_uploaded_songs()
library_path = list()


# Create folders

illegal_characters = [":", "?", "\"", "*", "|", "<", ">", "/"]
i = 0
for d in library:
    album_artist = (d["artist"], "Unknown")[d["artist"] == '']
    album = (d["album"], "Unknown")[d["album"] == '']

    for c in illegal_characters:
        album = album.replace(c, "")
        album_artist = album_artist.replace(c, "")

    folder = f'{album_artist} - {album}'
    folder = folder.replace("  ", " ")

    folder_path = root_music_folder + folder

    library_path.append(folder_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


# Write files

extensions = [".flac", ".mp3", ".ogg", ".wav"]
for i in range(len(library_path)):
    for c in illegal_characters:
        library[i]["title"] = library[i]["title"].replace(c, "")

    full_path = f'{library_path[i]}/{library[i]["title"]}'
    full_path.encode("utf-8")
    cont = False

    if not os.path.exists(full_path):
        for e in extensions:
            if os.path.exists(full_path + e):
                print(full_path + e + " already exists.")
                cont = True
                break
        if cont:
            continue

        filename, audio = mm.download_song(library[i]["id"])
        r = library[i]["title"][library[i]["title"].rfind("."):]
        if r == -1 or r not in extensions:
            full_path += "." + fleep.get(audio).extension[0]

    else:
        print(full_path + " already exists.")
        continue

    print(f'[{i}]: {full_path}')

    with open(full_path, 'wb') as f:
        f.write(audio)

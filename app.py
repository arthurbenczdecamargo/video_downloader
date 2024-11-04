import os
from pytubefix import YouTube, Search
from pytubefix.cli import on_progress


def start_app(count=0):
    if count == 0:
        os.system("cls")
        print("--------------------------------")
        print("|   YouTube Video Downloader   |")
        print("--------------------------------")
    video = input("\nEnter YouTube video URL or search for a video: ")
    if video.startswith("https://www.youtube.com/"):
        try:
            url = video
            vid_title = YouTube(video).title
            choose_dir(url, vid_title)
        except Exception as e:
            print(f"Error: {e}")
    else:
        create_list(video)


def create_list(video, count=0):
    results = Search(video)
    videos_list = {}
    for vid in results.videos:
        title = vid.title
        url = vid.watch_url
        length = vid.length
        num = count + 1
        videos_list[title] = [num, url, length]
        count += 1
        if count == 20:
            break
    display_list(videos_list)


def display_list(videos_list, start_index=0, count=0):
    end_index = start_index + 5
    items = list(videos_list.items())
    for title, videos_info in items[start_index:end_index]:
        num, url, length = videos_info
        print(f"\n{num} - {title}")
        print(url)
        if length >= 60:
            vid_min = round(length / 60, 2)
            print(f"{vid_min} min")
        else:
            print(f"{length} sec")
        count += 1
        if count >= len(videos_list):
            choose_video(videos_list)
        if count % 5 == 0 and end_index < len(videos_list):
            load_more = input("\nLoad more five videos? (Y/N): \n")
            if load_more.lower() == "y":
                display_list(videos_list, end_index, count)
            else:
                choose_video(videos_list)


def choose_dir(url, vid_title):
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}\n")
    save_dir = input(
        f"Enter the directory to save the video '{vid_title}' (leave blank for current directory): "
    )

    if save_dir == "":
        save_dir = current_dir
        download_ytb_video(url, save_dir)
    else:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        download_ytb_video(url, save_dir)


def choose_video(videos_list):
    while True:
        try:
            download = int(input("\nChoose a video to download: "))
            keys = list(videos_list.keys())
            url = videos_list[keys[download - 1]][1]
            vid_title = keys[download - 1]
            if 1 <= download <= len(videos_list):
                choose_dir(url, vid_title)
                return
        except ValueError:
            print("Invalid input")
            choose_video(videos_list)


def download_ytb_video(url, save_dir):
    video = YouTube(url, on_progress_callback=on_progress)
    print(f"\nDownloading: {video.title}")
    stream = video.streams.get_highest_resolution()
    stream.download(save_dir)
    continue_app()


def continue_app():
    count = 0
    choice = input("\n\nDownload another video? (Y/N): ")
    if choice.lower() == "y":
        count += 1
        start_app(count)
    elif choice.lower() == "n":
        print("\nExiting...")
    else:
        print("\nInvalid input")
        continue_app()

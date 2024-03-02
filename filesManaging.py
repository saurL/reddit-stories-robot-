import json
import os


class FilesManaging():

    def __init__(self):
        #saving files location
        self.reddit_stories_location = "reddit_stories.json"
        self.stories_locations = "./stories"
        self.reddit_stories = []
        self.folder_path = os.getcwd()

    def save_reddit_post(self):
        with open(self.reddit_stories_location, "w", encoding='utf-8') as file:
            json.dump(self.reddit_stories, file)

    def get_reddit_post_saved(self):
        with open(self.reddit_stories_location, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def get_reddit_stories(self):
        all_data = []

        dir_stories = os.listdir(self.stories_locations)

        for dir_story in dir_stories:
            with open(f"{self.stories_locations}\{dir_story}\data.json",
                      'r',
                      encoding='utf-8') as file:
                all_data.append(json.load(file))

        return all_data

    def set_reddit_stories(self, reddit_stories):
        self.reddit_stories = reddit_stories
        self.save_reddit_post()

    def add_reddit_stories(self, reddit_stories):
        titles = [story["title"] for story in self.get_reddit_stories()]
        for story in reddit_stories:
            if story["title"] not in titles:
                story["posted"] = False
                story["uploaded"] = False
                story["projet_created"] = False
                story["folder_created"] = False
                self.reddit_stories.append(story)
                self.update_story_data(story)
        self.save_reddit_post()

    def get_new_stories(self):
        return [
            story for story in self.get_reddit_stories()
            if not story["folder_created"]
        ]

    def get_stories_withoutVoice(self):
        return [
            story for story in self.get_reddit_stories()
            if not story["voice_gotten"]
        ]

    def get_stories_withoutVideo(self):
        return [
            story for story in self.get_reddit_stories()
            if story["voice_gotten"] and not story["projet_created"]
        ]

    def get_stories_not_uploaed(self):
        return [
            story for story in self.get_reddit_stories()
            if story["projet_created"] and not story["posted"]
        ]

    def get_stories_not_uploaded_tiktok(self):
        return [
            story for story in self.get_reddit_stories()
            if story["posted"] and not story["upload_to_tiktok"]
        ]

    def get_stories_not_uploaded_youtube(self):
        return [
            story for story in self.get_reddit_stories()
            if story["posted"] and not story["upload_to_youtube"]
        ]

    def get_stories_not_commented(self):
        return [
            story for story in self.get_reddit_stories()
            if story["projet_created"] and not story["commented"]
        ]

    def get_video(self, post):
        videos_path = []

        for file in os.listdir(post["folder"]):
            if file.endswith(".mp4"):
                videos_path.append(
                    f"{self.folder_path}\{post['folder'][2:]}\{file}")
        return videos_path

    def add_reddit_story(self, story):
        titles = [story["title"] for story in self.reddit_stories]
        if story["title"] not in titles:
            story["posted"] = False
            story["projet_created"] = False
            story["folder_created"] = False
            story["voice_gotten"] = False
            self.reddit_stories.append(story)

    def create_folder(self, reddit_story):
        title = reddit_story['title'].replace('?', '').replace(
            '\"',
            '').replace("*", "").replace("/", "").replace(".",
                                                          "").replace(":", "")

        reddit_story["folder"] = self.stories_locations + f"\{title }"

        reddit_folder = reddit_story["folder"]
        if os.path.isdir(reddit_folder):
            return
        reddit_story["folder_created"] = True
        os.makedirs(reddit_folder)

    def update_story_data(self, reddit_story):
        reddit_folder = reddit_story["folder"]
        with open(reddit_folder + "\data.json", "w", encoding='utf-8') as file:
            json.dump(reddit_story, file)


"""f = FilesManaging()
post = {}
post[
    "folder"] = "./stories\\AITA for deciding my baby’s name even though my husband hadn’t agreed on it"
print(f.get_video(post))
"""
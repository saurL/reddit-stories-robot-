import sys
from Montage import Monteur
from sound_recorder import AudioRecorder
from Webcontroller import Webcontroller
from filesManaging import FilesManaging
from PySide6 import QtCore, QtWidgets, QtGui
import warnings

warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2


class RedditStoriesRobot(QtWidgets.QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.web_controller = Webcontroller()
        self.audio_recorder = AudioRecorder()
        self.fileManager = FilesManaging()
        self.video_editor = Monteur()

        self.button_get_stories = QtWidgets.QPushButton(
            "Récupèrez les histoires")
        self.button_get_audio = QtWidgets.QPushButton("Récupèrez l'audio")
        self.button_edit = QtWidgets.QPushButton("Monter les vidéos")
        self.button_render = QtWidgets.QPushButton("Uploader les vidéos")
        self.button_do_them_all = QtWidgets.QPushButton("Tout faire")

        self.button_get_stories.clicked.connect(self.check_new_stories)
        self.button_get_audio.clicked.connect(self.get_audio)
        self.button_edit.clicked.connect(self.edit)
        self.button_render.clicked.connect(self.save)
        self.button_do_them_all.clicked.connect(self.do_them_all)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.layout.addWidget(self.button_get_stories)
        self.layout.addWidget(self.button_get_audio)
        self.layout.addWidget(self.button_edit)
        self.layout.addWidget(self.button_render)
        self.layout.addWidget(self.button_do_them_all)

        self.width = 200
        self.height = 500

        self.resize(self.width, self.height)
        self.show()

    def hide_and_show_window(function):

        def wrapper(*arg):
            self = arg[0]
            self.showMinimized()
            result = function(self)
            self.show()

            return result

        return wrapper

    @hide_and_show_window
    @QtCore.Slot()
    def check_new_stories(self):
        self.showMinimized()
        web_controller = self.web_controller
        web_controller.check_new_stories()

    @hide_and_show_window
    @QtCore.Slot()
    def get_audio(self):
        web_controller = self.web_controller
        web_controller.go_to_text_to_speach()
        stories_without_voice = self.fileManager.get_stories_withoutVoice()
        for story in stories_without_voice:
            if not self.get_audio_for_story(story["title"], story["folder"],
                                            "title"):
                break
            if self.get_audio_for_story(story["content"], story["folder"],
                                        "content"):
                story["voice_gotten"] = True
                self.fileManager.update_story_data(story)
            else:
                break

    @hide_and_show_window
    @QtCore.Slot()
    def edit(self):
        self.video_editor.edit_video()

    @hide_and_show_window
    @QtCore.Slot()
    def save(self):
        self.video_editor.save_videos()

    @hide_and_show_window
    @QtCore.Slot()
    def do_them_all(self):
        self.check_new_stories()
        self.get_audio()
        self.edit()
        self.save()

    def get_audio_for_story(
        self,
        text,
        folder,
        name,
    ):
        finished = False
        web_controller = self.web_controller
        audio_recorder = AudioRecorder()
        button_cliked = False
        web_controller.fill_content(text)
        while not button_cliked:
            try:
                web_controller.start_text_to_speach()
            except:
                return False
            button_cliked, started = web_controller.wait_for_text_to_speach_start(
            )
            if not started:
                return False

        audio_recorder.start_recording()
        finished = web_controller.wait_for_text_to_speach_stop()
        audio_recorder.stop_recording()
        if finished:
            print("fini de record")
            audio_recorder.save(f"{folder}\{name}.wav")
        return finished

    def edit_video(self):
        self.video_editor.edit_video()

    def render_video_and_upload(self):
        self.video_editor.save_videos()
        self.web_controller.post_all_video_youtube()
        self.web_controller.post_all_video_tiktok()


#robot = RedditStoriesRobot()
#robot.check_new_stories_get_audio_and_edit()
#robot.render_video_and_upload()
#robot.video_editor.save_videos()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    robot = RedditStoriesRobot()

    sys.exit(app.exec())
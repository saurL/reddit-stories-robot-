from Montage import Monteur
from sound_recorder import AudioRecorder
from Webcontroller import Webcontroller
from filesManaging import FilesManaging


class commentRobot():

    def __init__(self) -> None:
        self.web_controller = Webcontroller("\comment_profile")
        self.fileManager = FilesManaging()

        

    def comment_tiktok_video(self):
        self.web_controller.comment_tiktok_video()
        return


robot = commentRobot()
robot.comment_tiktok_video()

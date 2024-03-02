import signal
import time
import pymiere
from pymiere import exe_utils
from pymiere.wrappers import time_from_seconds
from pymiere.wrappers import get_system_sequence_presets
from pymiere.wrappers import timecode_from_time
import os
import random
from pymiere.core import eval_script
from filesManaging import FilesManaging
from pydub import AudioSegment, silence
import pyautogui
from pyautogui import ImageNotFoundException


class Monteur:

    def __init__(self) -> None:
        exe_utils.start_premiere()

        self.folder_path = os.getcwd()
        self.satisfing_video_path = self.folder_path + "\Minecraft_parkourt.mp4"
        self.title_audio_path = "title.wav"
        self.content_audio_path = "content.wav"
        self.sequence_preset_path = r"C:\Users\sauro\OneDrive\Documents\Adobe\Premiere Pro\24.0\Profile-sauro\Settings\Personnalisé\short.sqpreset"
        self.export_preset = r"E:\adobe_app\Adobe Premiere Pro 2024\Settings\IngestPresets\Transcode\Match Source - H.264 High Bitrate.epr"
        self.image_path = "image.jpeg"
        self.max_duration_short = 62
        self.min_duration_short = 62
        self.fileManager = FilesManaging()

        self.screenshot_fodler = "./screenshots/"

    def edit_video(self):

        sotries_without_video = self.fileManager.get_stories_withoutVideo()
        nb_sotry = 0
        for stories in sotries_without_video:
            nb_sotry += 1

            pid = exe_utils.start_premiere()

            folder = self.folder_path + "\\" + stories["folder"][2:]
            time.sleep(10)
            pymiere.objects.app.newProject(f"{folder}/project.prproj")
            pymiere.objects.app.openDocument(f"{folder}/project.prproj")

            project = pymiere.objects.app.project

            title_audio_path = f"{folder}\{self.title_audio_path}"
            content_audio_path = f"{folder}\{self.content_audio_path}"
            image_path = f"{folder}\{self.image_path}"

            success = project.importFiles(
                [
                    self.satisfing_video_path, title_audio_path,
                    content_audio_path, image_path
                ],  # can import a list of media  
                suppressUI=True,
                targetBin=project.getInsertionBin(),
                importAsNumberedStills=False)

            nb_sequnces = 1
            sequence_name = f"Part {nb_sequnces}"
            pymiere.objects.qe.project.newSequence(sequence_name,
                                                   self.sequence_preset_path)
            time.sleep(1)
            sequences = [
                s for s in pymiere.objects.app.project.sequences
                if s.name == sequence_name
            ]

            sequence = sequences[0]
            # open sequence in UI
            pymiere.objects.app.project.openSequence(
                sequenceID=sequence.sequenceID)
            sequence = project.activeSequence
            """ check how long the video will be and how to cut it if needed"""
            """ deal with audio first """

            videos = project.rootItem.findItemsMatchingMediaPath(
                self.satisfing_video_path, ignoreSubclips=False)
            video = videos[0]

            audio = project.rootItem.findItemsMatchingMediaPath(
                title_audio_path, ignoreSubclips=False)

            sequence.audioTracks[1].insertClip(audio[0], time_from_seconds(0))
            sequence.audioTracks[1].clips[0].setSelected(True, True)
            self.enhance_voice()

            first_audio = sequence.audioTracks[1].clips[0]

            audio = project.rootItem.findItemsMatchingMediaPath(
                content_audio_path, ignoreSubclips=False)
            sequence.audioTracks[0].insertClip(audio[0], first_audio.duration)

            second_audio = sequence.audioTracks[0].clips[0]

            total_duration = first_audio.duration.seconds + second_audio.duration.seconds

            temp_video = project.rootItem.findItemsMatchingMediaPath(
                self.satisfing_video_path, ignoreSubclips=False)
            sequence.videoTracks[0].insertClip(temp_video[0],
                                               time_from_seconds(0))
            full_video_duration = sequence.videoTracks[0].clips[
                0].duration.seconds

            sequence.videoTracks[0].clips[0].remove(inRipple=True,
                                                    inAlignToVideo=True)
            for audio in sequence.audioTracks[0].clips:
                audio.remove(inRipple=False, inAlignToVideo=True)

            start_of_video = random.uniform(
                0, full_video_duration - total_duration)

            videos = project.rootItem.findItemsMatchingMediaPath(
                self.satisfing_video_path, ignoreSubclips=False)[0]
            shorted_video = video.createSubClip(
                "in time ",
                time_from_seconds(start_of_video),
                time_from_seconds(start_of_video + total_duration),
                takeVideo=True,
                hasHardBoundaries=True,
                takeAudio=False)
            sequence.videoTracks[0].insertClip(shorted_video,
                                               time_from_seconds(0))

            audio = project.rootItem.findItemsMatchingMediaPath(
                content_audio_path, ignoreSubclips=False)
            sequence.audioTracks[0].insertClip(audio[0], first_audio.duration)
            sequence.audioTracks[0].clips[0].setSelected(True, True)
            self.enhance_voice()

            self.create_subtitles()
            image = project.rootItem.findItemsMatchingMediaPath(
                image_path, ignoreSubclips=False)[0]
            image = image.createSubClip("title ",
                                        time_from_seconds(0),
                                        time_from_seconds(
                                            first_audio.duration.seconds),
                                        takeVideo=True,
                                        hasHardBoundaries=True,
                                        takeAudio=False)
            sequence.videoTracks[1].insertClip(image, time_from_seconds(0))
            project.save()
            project.closeDocument()
            stories["projet_created"] = True
            self.fileManager.update_story_data(stories)
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)

    def edit_video_in_many_part(self):

        sotries_without_video = self.fileManager.get_stories_withoutVideo()
        nb_sotry = 0
        for stories in sotries_without_video:
            nb_sotry += 1

            pid = exe_utils.start_premiere()

            folder = self.folder_path + "\\" + stories["folder"][2:]
            time.sleep(10)
            pymiere.objects.app.newProject(f"{folder}/project.prproj")
            pymiere.objects.app.openDocument(f"{folder}/project.prproj")

            project = pymiere.objects.app.project

            title_audio_path = f"{folder}\{self.title_audio_path}"
            content_audio_path = f"{folder}\{self.content_audio_path}"
            image_path = f"{folder}\{self.image_path}"

            success = project.importFiles(
                [
                    self.satisfing_video_path, title_audio_path,
                    content_audio_path, image_path
                ],  # can import a list of media  
                suppressUI=True,
                targetBin=project.getInsertionBin(),
                importAsNumberedStills=False)

            nb_sequnces = 1
            sequence_name = f"Part {nb_sequnces}"
            pymiere.objects.qe.project.newSequence(sequence_name,
                                                   self.sequence_preset_path)
            time.sleep(1)
            sequences = [
                s for s in pymiere.objects.app.project.sequences
                if s.name == sequence_name
            ]

            sequence = sequences[0]
            # open sequence in UI
            pymiere.objects.app.project.openSequence(
                sequenceID=sequence.sequenceID)
            sequence = project.activeSequence
            """ check how long the video will be and how to cut it if needed"""
            """ deal with audio first """

            videos = project.rootItem.findItemsMatchingMediaPath(
                self.satisfing_video_path, ignoreSubclips=False)
            video = videos[0]

            audio = project.rootItem.findItemsMatchingMediaPath(
                title_audio_path, ignoreSubclips=False)

            sequence.audioTracks[1].insertClip(audio[0], time_from_seconds(0))
            sequence.audioTracks[1].clips[0].setSelected(True, True)
            self.enhance_voice()

            first_audio = sequence.audioTracks[1].clips[0]

            audio = project.rootItem.findItemsMatchingMediaPath(
                content_audio_path, ignoreSubclips=False)
            sequence.audioTracks[0].insertClip(audio[0], first_audio.duration)

            second_audio = sequence.audioTracks[0].clips[0]
            sequence.audioTracks[0].clips[0].remove(inRipple=True,
                                                    inAlignToVideo=True)
            total_duration = first_audio.duration.seconds + second_audio.duration.seconds
            nb_of_segement = 1
            cut_timing = [[0, 0]]
            if total_duration > self.min_duration_short:
                myaudio = AudioSegment.from_wav(content_audio_path)
                dBFS = myaudio.dBFS
                silences = silence.detect_silence(myaudio,
                                                  min_silence_len=1,
                                                  silence_thresh=dBFS - 16)

                silences = [((start / 1000), (stop / 1000))
                            for start, stop in silences]

                nb_of_segement = int(total_duration // self.min_duration_short)

                for i in range(0, nb_of_segement):
                    for start, stop in silences:
                        if start >= self.min_duration_short * (i + 1):
                            cut_timing.append([
                                start - first_audio.duration.seconds,
                                stop - first_audio.duration.seconds
                            ])
                            break

                if len(cut_timing) != nb_of_segement:
                    nb_of_segement += 1
            else:
                nb_of_segement = 1

            cut_timing.append(
                [second_audio.duration.seconds, second_audio.duration.seconds])

            temp_video = project.rootItem.findItemsMatchingMediaPath(
                self.satisfing_video_path, ignoreSubclips=False)
            sequence.videoTracks[0].insertClip(temp_video[0],
                                               time_from_seconds(0))
            full_video_duration = sequence.videoTracks[0].clips[
                0].duration.seconds

            sequence.videoTracks[0].clips[0].remove(inRipple=True,
                                                    inAlignToVideo=True)
            sequence.audioTracks[0].clips[0].remove(inRipple=True,
                                                    inAlignToVideo=True)

            start_of_video = random.uniform(
                0, full_video_duration - total_duration)

            videos = project.rootItem.findItemsMatchingMediaPath(
                self.satisfing_video_path, ignoreSubclips=False)[0]
            shorted_video = video.createSubClip(
                "in time ",
                time_from_seconds(start_of_video),
                time_from_seconds(start_of_video +
                                  first_audio.duration.seconds),
                takeVideo=True,
                hasHardBoundaries=True,
                takeAudio=False)
            satisfing_video_passed = first_audio.duration.seconds
            sequence.videoTracks[0].insertClip(shorted_video,
                                               time_from_seconds(0))

            for segement_nb in range(1, nb_of_segement + 1):

                start = cut_timing[segement_nb - 1][1]
                stop = cut_timing[segement_nb][0]
                segement_time = stop - start

                shorted_video = video.createSubClip(
                    "in time ",
                    time_from_seconds(start_of_video + satisfing_video_passed),
                    time_from_seconds(start_of_video + satisfing_video_passed +
                                      segement_time),
                    takeVideo=True,
                    hasHardBoundaries=True,
                    takeAudio=False)

                satisfing_video_passed += segement_time
                if segement_nb != 1:
                    sequence.videoTracks[0].insertClip(shorted_video,
                                                       time_from_seconds(0))
                    sequence.videoTracks[0].clips[0].setSelected(True, True)
                else:
                    sequence.videoTracks[0].insertClip(
                        shorted_video,
                        time_from_seconds(first_audio.duration.seconds))
                audio = project.rootItem.findItemsMatchingMediaPath(
                    content_audio_path, ignoreSubclips=False)[0]

                shorted_audio = audio.createSubClip(f"audio{segement_nb}",
                                                    time_from_seconds(start),
                                                    time_from_seconds(stop),
                                                    takeVideo=False,
                                                    hasHardBoundaries=True,
                                                    takeAudio=True)
                if segement_nb != 1:
                    sequence.audioTracks[0].insertClip(shorted_audio,
                                                       time_from_seconds(0))

                else:
                    sequence.audioTracks[0].insertClip(shorted_audio,
                                                       first_audio.duration)
                sequence.audioTracks[0].clips[0].setSelected(True, True)
                self.enhance_voice()

                if segement_nb == 1:

                    image = project.rootItem.findItemsMatchingMediaPath(
                        image_path, ignoreSubclips=False)[0]
                    image = image.createSubClip(
                        "title ",
                        time_from_seconds(0),
                        time_from_seconds(first_audio.duration.seconds),
                        takeVideo=True,
                        hasHardBoundaries=True,
                        takeAudio=False)
                    sequence.videoTracks[1].insertClip(image,
                                                       time_from_seconds(0))
                self.create_subtitles()
                if segement_nb != nb_of_segement:
                    nb_sequnces += 1
                    sequence_name = f"Part {nb_sequnces}"
                    pymiere.objects.qe.project.newSequence(
                        sequence_name, self.sequence_preset_path)
                    sequence = [
                        s for s in pymiere.objects.app.project.sequences
                        if s.name == sequence_name
                    ][0]
                    # open sequence in UI
                    pymiere.objects.app.project.openSequence(
                        sequenceID=sequence.sequenceID)
                    sequence = project.activeSequence

            project.save()
            project.closeDocument()
            stories["projet_created"] = True
            self.fileManager.update_story_data(stories)
            if nb_sotry != len(sotries_without_video):
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)

    def save_videos(self):
        exe_utils.start_premiere()
        time.sleep(5)
        video_to_upload = self.fileManager.get_stories_not_uploaed()
        nb_sotry = 0
        for projet in video_to_upload:
            print(projet['title'])
            nb_sotry += 1
            pid = exe_utils.start_premiere()
            folder = self.folder_path + "\\" + projet["folder"][2:]
            pymiere.objects.app.openDocument(f"{folder}/project.prproj")
            sequences = [s for s in pymiere.objects.app.project.sequences]
            nb = 0
            for sequence in sequences:
                pymiere.objects.app.project.openSequence(
                    sequenceID=sequence.sequenceID)
                sequence = pymiere.objects.app.project.activeSequence
                nb += 1
                title = projet['title'].replace('?', '').replace(
                    '\"', '').replace("*", "").replace("/",
                                                       "").replace(".", "")
                for hastag in projet['hashtag']:
                    title += f" #{hastag}"

                result = sequence.exportAsMediaDirect(
                    f"{folder}\{sequence.name} {title}.mp4",  # path of the exported file
                    self.export_preset,  # path of the export preset file
                    pymiere.objects.app.encoder.
                    ENCODE_ENTIRE,  # what part of the sequence to export. Others are: ENCODE_IN_TO_OUT or ENCODE_WORKAREA
                )
            projet["posted"] = True
            self.fileManager.update_story_data(projet)
            try:
                pymiere.objects.app.project.closeDocument()
            except:
                print("error while closing projet in montage.py")
            if nb_sotry != len(video_to_upload):
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)

    def show_pr(self):
        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'premier_pro_icon.png',
                                            confidence=0.9)
        pyautogui.click(location)

    def create_subtitles(self):
        """ Create the subtitles """

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'text_icon_subtitle.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'create_subtitles.png',
                                            confidence=0.7)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'subtitles_preferences.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)
        location = list(
            pyautogui.locateAllOnScreen(self.screenshot_fodler +
                                        'drag_button.png',
                                        confidence=0.9))

        pyautogui.moveTo(location[0])
        pyautogui.drag(-310, 0, 1, button='left')
        time.sleep(1)
        pyautogui.moveTo(location[2])
        pyautogui.drag(-210, 0, 1, button='left')
        time.sleep(1)

        location = list(
            pyautogui.locateAllOnScreen(self.screenshot_fodler +
                                        'simple_button.png',
                                        confidence=0.8))
        pyautogui.click(location[0])

        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'transcript_pref.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'mixage.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'audio1.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'end_creation_subtitles.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        subtitles_created = False
        while not subtitles_created:
            time.sleep(5)
            try:
                location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                                    'sous_titre_icon.png')
                subtitles_created = True

            except ImageNotFoundException:
                subtitles_created = False
        pyautogui.moveTo(location)
        found = False
        while not found:
            try:
                pyautogui.click()
                pyautogui.click()
                time.sleep(1)
                pyautogui.locateOnScreen(self.screenshot_fodler +
                                         'font_image.png')
                found = True
            except ImageNotFoundException:
                pyautogui.move(10, 0)
                found = False
        """ Create the style for the subtitles and aplly them on all the subtitles of the track """
        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'font_image.png')
        pyautogui.click(location)
        pyautogui.write("Franklin Gothic Demi")
        pyautogui.press('enter')
        time.sleep(1.5)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'default_text_size.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)
        pyautogui.write("96")
        pyautogui.press('enter')
        time.sleep(1)

        location = pyautogui.locateCenterOnScreen(self.screenshot_fodler +
                                                  'location_text.png',
                                                  confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateCenterOnScreen(self.screenshot_fodler +
                                                  'default_style.png',
                                                  confidence=0.9)
        pyautogui.click(location)
        pyautogui.moveTo(10, 10)
        time.sleep(1)

        location = pyautogui.locateCenterOnScreen(self.screenshot_fodler +
                                                  'create_style.png',
                                                  confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateCenterOnScreen(self.screenshot_fodler +
                                                  'ok_button.png',
                                                  confidence=0.9)

        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateCenterOnScreen(self.screenshot_fodler +
                                                  'up_arrow.png',
                                                  confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateCenterOnScreen(self.screenshot_fodler +
                                                  'ok_button2.png',
                                                  confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

    def enhance_voice(self):
        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'ameloration_audio.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'dialogue.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'default_dialogue_param.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

        location = pyautogui.locateOnScreen(self.screenshot_fodler +
                                            'audio_param.png',
                                            confidence=0.9)
        pyautogui.click(location)
        time.sleep(1)

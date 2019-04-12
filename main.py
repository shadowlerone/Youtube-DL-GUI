from __future__ import unicode_literals

from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlFile
from pyforms.controls import ControlText
from pyforms.controls import ControlSlider
# from pyforms.controls import ControlPlayer
from pyforms.controls import ControlButton
from pyforms.controls import ControlImage
from pyforms.controls import ControlProgress
from pyforms.controls import ControlLabel
import downloader
import cv2
import numpy as np
import youtube_dl
import re


class YoutubeDownloader(BaseWidget):
	def __init__(self, *args, **kwargs):
		super().__init__('Youtube Downloader')
		self._url = ControlText('Link')
		self._runbutton = ControlButton('Download')
		self._progress = ControlProgress(max=100)
		self._actualLabel = ControlLabel("Progess:")
		self._status = ControlLabel("Idle")
		self._eta = ControlLabel("")
		self.pattern = re.compile(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$")
		# self._thumbnail = ControlImage()
		self._formset = [
			('_url', '_runbutton'),
			('_actualLabel', '_status'), ('_progress', '_eta'),
			' '
		]
		# self._url.finishEditing = self.__downloadImage
		self._runbutton.value = self.__buttonAction
		self.disabled = False

	def __downloadImage(self):
		print(self._url.value)
		x = downloader.get_image(self._url.value)
		print(x)
		self._thumbnail.value = x

	def __buttonAction(self):
		self._runbutton.label = "Download"
		if self.disabled:
			return
		if self.pattern.fullmatch(self._url.value) == None:
			self._runbutton.label = "Invalid Youtube Url"
			# print(self.pattern.match(self._url.value))
			return
		self.disabled = True
		print(self._url.value)
		try:
			self.downloadVid(self._url.value)
		except:
			self._runbutton.label = "Error! Check Url."
			self.disabled = False

		# self._thumbnail.value = "text.jpg"

	def downloadVid(self, url):
		self.reset()
		ydl_opts = {
			'progress_hooks': [self.my_hook],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])

	def my_hook(self, d):
		if d["status"] == "finished":
			self.disabled = False
		else:
			self._eta.value = str(d["eta"]) + "s"
		self._progress.value = d["downloaded_bytes"]/d["total_bytes"] * 100
		self._status.value = d["status"].capitalize()

	def reset(self):
		self._status.value = "Idle"
		self._progress.value = 0
		self._eta.value = ""


if __name__ == '__main__':
	from pyforms import start_app
	start_app(YoutubeDownloader, (500, 500, 500, 200))

"(idk, idk, idk, height?)"

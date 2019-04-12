import tempfile
import requests
from videos_id.video_info import VideoInfo


def get_image(url):
	temp = tempfile.NamedTemporaryFile(suffix=".jpg")
	video_info = VideoInfo()
	ident = video_info.check_video_id(url)
	template = "https://img.youtube.com/vi/{}/default.jpg".format(ident)
	r = requests.get(template)
	if r.status_code == 200:
		r.raw.decode_content = True
		try:
			# print(r.content)
			temp.write(r.content)
			# temp.seek(0)
			# print(temp.read())
			return temp.name
		finally:  
			temp.close()



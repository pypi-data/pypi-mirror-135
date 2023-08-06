from __future__ import unicode_literals
from datetime import datetime
import yt_dlp
import requests
import re
import tempfile
from PIL import Image
from io import BytesIO
from pathlib import Path

class BasketCase:
    def __init__(self, session_id=None):
        self._session = requests.Session()

        if session_id:
            self._session.cookies.set('sessionid', session_id)

        self._output_base = f'{Path.cwd()!s}/basketcase_{datetime.now()!s}'
        self._output_images = self._output_base + '/images'
        self._output_videos = self._output_base + '/videos'

    def fetch(self, target_urls):
        urls = self._scan(target_urls)
        
        if urls['images'] or urls['videos']:
            self._prepare_output()

            for url in urls['images']:
                self._get_image(url)

            self._get_videos(urls['videos'])
        else:
            print('Nothing was found. Maybe you need a session cookie?')

    def _prepare_output(self):
        Path(self._output_images).mkdir(parents=True, exist_ok=True)
        Path(self._output_videos).mkdir(parents=True, exist_ok=True)

    def _scan(self, target_urls):
        sets = {'images': set(), 'videos': set()}

        print('Scanning the targets. This can take a while.')

        for target_url in target_urls:
            request = self._session.get(target_url, timeout=10)
            image_urls = re.findall(r'"display_url":"(.*?)"', request.text)
            video_urls = re.findall(r'"video_url":"(.*?)"', request.text)

            for image_url in image_urls:
                image_url = self._decode_ampersands(image_url)
                sets['images'].add(image_url)

            for video_url in video_urls:
                video_url = self._decode_ampersands(video_url)
                sets['videos'].add(video_url)

        return sets

    def _decode_ampersands(self, url):
        return re.sub(r'\\u0026', '&', url)

    def _get_image(self, url):
        print('Downloading image:', url)

        request = self._session.get(url, timeout=10)

        # Build image from binary response data
        image = Image.open(BytesIO(request.content))
        fp = tempfile.NamedTemporaryFile(prefix='basketcase_', suffix='.jpg', dir=self._output_images, delete=False)
        image.save(fp, format='JPEG')

    def _get_videos(self, urls):
        if self._session.cookies.get('sessionid'):
            # Add the session cookie
            yt_dlp.utils.std_headers.update({'Cookie': 'sessionid=' + self._session.cookies.get('sessionid')})

        ydl_opts = {
            'outtmpl': self._output_videos + '/%(title)s.%(ext)s' # Set output directory
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)


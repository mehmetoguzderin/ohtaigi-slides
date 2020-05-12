import os
import pathlib
import subprocess

from flask import Flask, abort, request, send_file
from google.cloud import secretmanager

def content_to_video(voice, slides):
  video = 'video.mp4'
  ffconcat_str = 'ffconcat version 1.0\n'
  for slide, duration in slides:
    ffconcat_str += f'file {slide}\n'
    ffconcat_str += f'duration {duration}\n'
  ffconcat = open('in.ffconcat', 'w')
  ffconcat.write(ffconcat_str)
  ffconcat.close()
  process = ['ffmpeg', '-y',
                       '-safe', '0',
                       '-i', 'in.ffconcat',
                       '-i', voice,
                       '-c:a', 'aac',
                       '-c:v', 'libx264',
                       '-pix_fmt', 'yuv420p',
                       '-vf', 'fps=24',
                       video]
  subprocess.call(process)

def method_to_video():
  voice_file = request.files['voice']
  voice = 'voice' + ''.join(pathlib.Path(voice_file.filename).suffixes)
  voice_file.save(voice)
  slides = []
  for i in range(len(request.files) - 1):
    slides += [[f'show{i}.png', float(request.form[f'duration{i}'])]]
    request.files[f'show{i}'].save(f'show{i}.png')
  content_to_video(voice, slides)

app = Flask(__name__)

@app.route('/', methods=['POST'])
def slides():
  password = str(request.form['password'])
  client = secretmanager.SecretManagerServiceClient()
  name = client.secret_version_path('mehmetoguzderin', 'ohtaigi-slides', '1')
  response = client.access_secret_version(name)
  payload = response.payload.data.decode('UTF-8')
  if payload == password:
    method_to_video()
    response = send_file('video.mp4', as_attachment=True)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
  else:
    abort(404)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
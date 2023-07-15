import os
from urllib.parse import parse_qs, urlparse

from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flaskwebgui import FlaskUI
from pytube import Playlist, YouTube
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "MmqQwJt4d9"
bootstrap = Bootstrap5(app)


class YoutubeLinkForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired()])
    submit = SubmitField("Download")


@app.route("/", methods=["GET", "POST"])
def pytubeUi():
    form = YoutubeLinkForm()
    if form.validate_on_submit():
        link = form.url.data
        if is_playlist(link):
            playlist_id = extract_playlist_id(link)
            if playlist_id:
                try:
                    playlist = Playlist(
                        f"https://www.youtube.com/playlist?list={playlist_id}"
                    )
                    folder = os.path.join(
                        os.path.expanduser("~/Downloads"), playlist.title
                    )
                    os.makedirs(folder, exist_ok=True)
                    download_playlist(playlist, folder)
                    flash(category="success", message="Download da playlist concluído!")
                except Exception as e:
                    flash(
                        category="danger",
                        message=f"Ocorreu um erro durante o download da playlist: {str(e)}",
                    )
            else:
                flash(category="danger", message="Link da playlist inválido")
        else:
            video_id = extract_video_id(link)
            if video_id:
                try:
                    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
                    folder = os.path.expanduser("~/Downloads")
                    download_video(video, folder)
                    flash(category="success", message="Download do vídeo concluído!")
                except Exception as e:
                    flash(
                        category="danger",
                        message=f"Ocorreu um erro durante o download do vídeo: {str(e)}",
                    )
            else:
                flash("danger", "Link do YouTube inválido")
        return redirect(url_for("pytubeUi"))
    return render_template("index.html", form=form)


def is_playlist(url):
    parsed_url = urlparse(url)
    return parsed_url.path == "/playlist"


def extract_playlist_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    playlist_id = query_params.get("list")
    if playlist_id:
        return playlist_id[0]
    else:
        return None


def extract_video_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v")
    if video_id:
        return video_id[0]
    else:
        return None


def download_playlist(playlist, folder):
    for video in playlist.videos:
        try:
            youtube_object = video.streams.get_highest_resolution()
            file_path = os.path.join(folder, video.title + ".mp4")
            youtube_object.download(output_path=file_path)
        except Exception as e:
            print(f"Erro ao baixar o vídeo: {str(e)}")


def download_video(video, folder):
    try:
        youtube_object = video.streams.get_highest_resolution()
        file_path = os.path.join(folder, video.title + ".mp4")
        youtube_object.download(output_path=file_path)
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {str(e)}")


if __name__ == "__main__":
    FlaskUI(app=app, server="flask", width=800, height=600).run()

import os
from urllib.parse import parse_qs, urlparse

from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flaskwebgui import FlaskUI
from pytube import YouTube
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "MmqQwJt4d9"
bootstrap = Bootstrap(app)


class YoutubeLinkForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired()])
    submit = SubmitField("Download")


@app.route("/", methods=["GET", "POST"])
def pytubeUi():
    form = YoutubeLinkForm()
    if form.validate_on_submit():
        link = form.url.data
        video_id = extract_video_id(link)
        if video_id:
            folder = os.path.expanduser(
                "~/Downloads"
            )  # Obtém o caminho da pasta de downloads do sistema
            try:
                Download(video_id, folder)
                return redirect(url_for("download_complete"))
            except Exception as e:
                flash(f"Ocorreu um erro durante o download: {str(e)}", "danger")
        else:
            flash("Link do YouTube inválido", "danger")
    return render_template("index.html", form=form)


@app.route("/download_complete")
def download_complete():
    flash("Download concluído!", "success")
    return redirect(url_for("pytubeUi"))


def extract_video_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get("v")
    if video_id:
        return video_id[0]
    else:
        return None


def Download(video_id, folder):
    youtubeObject = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    youtubeObject.download(output_path=folder)


if __name__ == "__main__":
    FlaskUI(app=app, server="flask", width=800, height=600).run()

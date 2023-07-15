import os
from urllib.parse import parse_qs, urlparse

from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flaskwebgui import FlaskUI
from pytube import YouTube
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
        video_id = extract_video_id(link)
        if video_id:
            folder = os.path.expanduser("~/Downloads")
            try:
                Download(video_id, folder)
                flash(message="Download concluído!", category="success")
            except Exception as e:
                flash(
                    category="danger",
                    message=f"Ocorreu um erro durante o download: {str(e)}",
                )
        else:
            flash(message="Link do YouTube inválido", category="danger")
        return redirect(url_for("pytubeUi"))
    return render_template("index.html", form=form)


@app.route("/download_complete")
def download_complete():
    flash("success", "Download concluído!")
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

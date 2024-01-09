from flask import Flask, Blueprint, render_template, request, redirect, send_from_directory, url_for

from lib.extensions import db, Config
from models.library import *

api_bp = Blueprint('api', __name__)

## API
@api_bp.route('/api/tags')
def tags():
    tags_all = [(g.tags) for g in Game.query.all()]
    tag_list = []
    tags_unique = []

    for ta in tags_all:
        if ta:
            tag_string = ta.split(', ')
            for ts in tag_string:
                tag_list.append(ts)

    for tl in tag_list:
        if tl not in tags_unique:
            tags_unique.append(tl)

    sorted_tags = sorted(tags_unique)
    return (sorted_tags)
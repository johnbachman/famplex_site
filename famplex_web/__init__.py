import os
import csv
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from famplex_web.load_data import relationships, equivalences, synonyms, \
                                  entities


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/')
    def home():
        return render_template('entity_list.html', entities=entities)


    # The entity view page
    @app.route('/entity/<famplex_id>')
    def entity(famplex_id):
        isa_rels = []
        partof_rels = []
        for r in relationships:
            if not (r[0][0] == 'FPLX' and r[0][1] == famplex_id):
                continue
            if r[1] == 'isa':
                isa_rels.append(r[2])
            if r[1] == 'partof':
                partof_rels.append(r[2])

        equiv_list = []
        for equiv in equivalences.get(famplex_id, []):
            db, db_id = equiv
            eq_url = "http://identifiers.org/%s/%s" % (db, db_id)
            equiv_list.append((db, db_id, eq_url))

        return render_template(
                'entity.html',
                famplex_id = famplex_id,
                synonyms = synonyms[famplex_id],
                isa_rels = isa_rels,
                partof_rels = partof_rels,
                equivalences = equiv_list)
    return app

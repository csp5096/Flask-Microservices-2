from flask_admin.contrib.sqla import ModelView
from flask import (
  Flask, render_template, request, flash, redirect, url_for, session, jsonify
)

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('user') == 'Administrator'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(request.args.get('next') or url_for('home'))
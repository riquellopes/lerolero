# coding: utf-8
from functools import wraps
from flask import redirect, request, session, url_for

def login_required(func):
	@wraps(func)
	def decorated_view(*arg, **kwargs):
		if not session.get('user'):
			return redirect(url_for('.home', _external=True), code=403)
		return func(*arg, **kwargs)
	return decorated_view
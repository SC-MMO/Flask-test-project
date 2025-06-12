from flask import (
    Blueprint, redirect, render_template, session, url_for, abort
)
from flaskr.auth import login_required
from .models import SiteUser

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
def admin():
    User = SiteUser.objects(name=session.get('username')).first()
    if User.permissions.get("admin"):
        return render_template('admin/admin.html')
    abort(401)
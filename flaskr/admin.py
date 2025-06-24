from flask import (
    Blueprint, render_template, session, abort
)
from flaskr.auth import login_required
from .models import SiteUser

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
def admin():
    user = SiteUser.objects(id=session.get('id')).first()
    permissions = user.role.permissions
    if permissions.get('admin'):
        return render_template('admin/admin.html')
    abort(403)
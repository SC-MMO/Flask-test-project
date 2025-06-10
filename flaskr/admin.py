from flask import (
    Blueprint, redirect, render_template, session, url_for, abort
)


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def admin():
    return f"WIP"
    '''
    username = session.get('username')
    if str(username) == 'None':
        return redirect(url_for('index'))
    if username == 'admin':
        return render_template('admin/admin.html')
    abort(401)
    '''
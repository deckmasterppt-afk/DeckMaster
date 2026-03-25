# app.py - DeckMaster Flask Application

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import time

from config import (DEBUG, HOST, PORT, MAX_CONTENT_LENGTH,
                    OUTPUT_FOLDER, CORS_ORIGINS, SUBSCRIPTION_PLANS,
                    AVAILABLE_DESIGN_STYLES, ADMIN_PASSWORD)
from presentation_service import presentation_service
from user_manager import user_manager
from job_store import get_job
from feedback_store import save_feedback, get_all_feedback, get_feedback_count

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
CORS(app, origins=CORS_ORIGINS)


# ── Static files ──────────────────────────────────────────────────

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_file(f'static/{filename}')


# ── Health ────────────────────────────────────────────────────────

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': time.time(),
                    'message': 'DeckMaster is running'})


# ── Admin ─────────────────────────────────────────────────────────

@app.route('/api/admin/activate', methods=['POST'])
def activate_admin():
    try:
        data     = request.get_json() or {}
        password = data.get('password', '')
        user_id  = data.get('user_id', '')
        success, message = user_manager.activate_admin_mode(password, user_id)
        if success:
            return jsonify({'success': True, 'message': message, 'user_id': user_id})
        return jsonify({'success': False, 'error': message}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/deactivate', methods=['POST'])
def deactivate_admin():
    try:
        data    = request.get_json() or {}
        user_id = data.get('user_id', '')
        user_manager.deactivate_admin_mode(user_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ── Generation ────────────────────────────────────────────────────

@app.route('/api/generate', methods=['POST'])
def generate_presentation():
    try:
        data    = request.get_json() or {}
        user_id = data.get('user_id') or f'user_{int(time.time())}'
        print(f"[API] Generate | user={user_id} | slides={data.get('slide_count')} | design={data.get('design_style')}")
        result = presentation_service.start_generation(user_id, data)
        return jsonify(result), (200 if result['success'] else 400)
    except Exception as e:
        print(f"[API] Generate error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/job/<job_id>')
def get_job_status(job_id):
    try:
        return jsonify(presentation_service.get_job_status(job_id))
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<job_id>')
def download_presentation(job_id):
    try:
        job = get_job(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        if job['state'] != 'DONE':
            return jsonify({'error': f'Not ready ({job["state"]})'}), 400

        path = job['output']
        if not path or not os.path.exists(path):
            return jsonify({'error': 'File not found on server'}), 404

        print(f"[DOWNLOAD] {os.path.basename(path)} ({os.path.getsize(path)//1024} KB)")
        return send_file(
            path,
            as_attachment=True,
            download_name=os.path.basename(path),
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    except Exception as e:
        print(f"[DOWNLOAD] Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-info/<job_id>')
def get_file_info(job_id):
    try:
        job = get_job(job_id)
        if not job or job['state'] != 'DONE':
            return jsonify({'error': 'File not ready'}), 400
        path = job['output']
        if not os.path.exists(path):
            return jsonify({'error': 'File not found'}), 404
        size = os.path.getsize(path)
        return jsonify({
            'success': True,
            'file_info': {
                'filename':     os.path.basename(path),
                'absolute_path': os.path.abspath(path),
                'file_size':    size,
                'file_size_mb': round(size / 1048576, 2),
                'creation_date': time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(os.path.getctime(path))),
                'download_url': f'/api/download/{job_id}'
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Designs & Plans ───────────────────────────────────────────────

@app.route('/api/designs')
def get_designs():
    designs = [{'id': k, 'name': v} for k, v in AVAILABLE_DESIGN_STYLES.items()]
    return jsonify({'designs': designs, 'total': len(designs)})

@app.route('/api/plans')
def get_plans():
    return jsonify({'plans': SUBSCRIPTION_PLANS})


# ── Premium Feedback ──────────────────────────────────────────────

@app.route('/api/premium-feedback', methods=['POST'])
def submit_premium_feedback():
    try:
        data = request.get_json() or {}
        text = data.get('feedback', '').strip()
        if not text or len(text) < 10:
            return jsonify({'success': False,
                            'error': 'Please provide at least 10 characters of feedback'}), 400
        fid = save_feedback(text,
                            data.get('email') or None,
                            data.get('user_id'),
                            request.remote_addr)
        if fid:
            return jsonify({'success': True,
                            'message': "Thank you! We'll notify you when Premium launches.",
                            'feedback_id': fid})
        return jsonify({'success': False, 'error': 'Could not save feedback'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/feedback')
def get_admin_feedback():
    try:
        if request.headers.get('X-Admin-Password') != ADMIN_PASSWORD:
            return jsonify({'error': 'Unauthorized'}), 401
        return jsonify({'success': True,
                        'feedback': get_all_feedback(),
                        'total_count': get_feedback_count()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ── Entry point ───────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', PORT))
    print("=" * 50)
    print("  DeckMaster Server")
    print(f"  http://0.0.0.0:{port}")
    print(f"  Admin: {ADMIN_PASSWORD}")
    print("=" * 50)
    app.run(debug=DEBUG, host='0.0.0.0', port=port, threaded=True)

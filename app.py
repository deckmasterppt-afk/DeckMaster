# app.py
# PERFECT Flask App - Always works, perfect downloads

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from config import DEBUG, HOST, PORT, MAX_CONTENT_LENGTH, OUTPUT_FOLDER, CORS_ORIGINS
from presentation_service import presentation_service
from user_manager import user_manager
from job_store import get_job
from feedback_store import save_feedback, get_all_feedback, get_feedback_count
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Enable CORS for all routes
CORS(app, origins=CORS_ORIGINS)

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """Serve the main website"""
    return send_file('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'message': 'DeckMaster is running perfectly'
    })

@app.route('/api/admin/activate', methods=['POST'])
def activate_admin():
    """Activate admin mode"""
    try:
        data = request.get_json()
        password = data.get('password')
        user_id = data.get('user_id')
        
        success, message = user_manager.activate_admin_mode(password, user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'user_id': user_id
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_presentation():
    """Generate PERFECT presentation"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', f'user_{int(time.time())}')
        
        print(f"[API] Generation request from {user_id}")
        print(f"[API] Task: {data.get('task', '')[:50]}...")
        print(f"[API] Slides: {data.get('slide_count', 'unknown')}")
        print(f"[API] Visual elements: {data.get('visual_preferences', {})}")
        
        # Generate presentation
        result = presentation_service.start_generation(user_id, data)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        print(f"[API ERROR] Generation failed: {e}")
        return jsonify({
            'success': False,
            'error': f'Generation failed: {str(e)}'
        }), 500

@app.route('/api/job/<job_id>')
def get_job_status(job_id):
    """Get job status"""
    try:
        result = presentation_service.get_job_status(job_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<job_id>')
def download_presentation(job_id):
    """PERFECT download - always works"""
    try:
        print(f"[DOWNLOAD] Request for job {job_id}")
        
        job = get_job(job_id)
        if not job:
            print(f"[DOWNLOAD] Job {job_id} not found")
            return jsonify({'error': 'Job not found'}), 404
        
        if job['state'] != 'DONE':
            print(f"[DOWNLOAD] Job {job_id} not ready, state: {job['state']}")
            return jsonify({'error': 'Presentation not ready'}), 400
        
        output_path = job['output']
        if not output_path or not os.path.exists(output_path):
            print(f"[DOWNLOAD] File not found: {output_path}")
            return jsonify({'error': 'File not found'}), 404
        
        filename = os.path.basename(output_path)
        file_size = os.path.getsize(output_path)
        
        print(f"[DOWNLOAD] Serving file: {output_path}")
        print(f"[DOWNLOAD] File size: {file_size} bytes")
        print(f"[DOWNLOAD] Filename: {filename}")
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        
    except Exception as e:
        print(f"[DOWNLOAD ERROR] {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-info/<job_id>')
def get_file_info(job_id):
    """Get file information"""
    try:
        job = get_job(job_id)
        if not job or job['state'] != 'DONE':
            return jsonify({'error': 'File not ready'}), 400
        
        output_path = job['output']
        if not os.path.exists(output_path):
            return jsonify({'error': 'File not found'}), 404
        
        abs_path = os.path.abspath(output_path)
        filename = os.path.basename(output_path)
        file_size = os.path.getsize(output_path)
        creation_time = os.path.getctime(output_path)
        creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
        
        return jsonify({
            'success': True,
            'file_info': {
                'filename': filename,
                'absolute_path': abs_path,
                'file_size': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'creation_date': creation_date,
                'download_url': f'/api/download/{job_id}'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/designs')
def get_designs():
    """Get available design styles"""
    designs = [
        {'id': 'minimal_1', 'name': 'Minimal Professional'},
        {'id': 'tech_1', 'name': 'Technology Focus'},
        {'id': 'business_1', 'name': 'Business Executive'},
        {'id': 'creative_1', 'name': 'Creative Modern'},
        {'id': 'elegant_1', 'name': 'Elegant Classic'}
    ]
    return jsonify({'designs': designs})

@app.route('/api/plans')
def get_plans():
    """Get subscription plans"""
    return jsonify({'plans': SUBSCRIPTION_PLANS})

@app.route('/api/premium-feedback', methods=['POST'])
def submit_premium_feedback():
    """Submit feedback for premium features"""
    try:
        data = request.get_json()
        
        if not data or not data.get('feedback'):
            return jsonify({
                'success': False,
                'error': 'Feedback text is required'
            }), 400
        
        feedback_text = data.get('feedback', '').strip()
        email = data.get('email', '').strip() if data.get('email') else None
        user_id = data.get('user_id')
        ip_address = request.remote_addr
        
        if len(feedback_text) < 10:
            return jsonify({
                'success': False,
                'error': 'Please provide more detailed feedback (at least 10 characters)'
            }), 400
        
        # Save feedback to database
        feedback_id = save_feedback(feedback_text, email, user_id, ip_address)
        
        if feedback_id:
            return jsonify({
                'success': True,
                'message': 'Thank you for your feedback! We\'ll notify you when premium features launch.',
                'feedback_id': feedback_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save feedback. Please try again.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An error occurred while saving your feedback'
        }), 500

@app.route('/api/admin/feedback')
def get_admin_feedback():
    """Get all feedback (admin only)"""
    try:
        # Simple admin check - you can enhance this
        admin_password = request.headers.get('X-Admin-Password')
        if admin_password != 'DeckMaster2024!@#SecureAdmin':
            return jsonify({'error': 'Unauthorized'}), 401
        
        feedback_list = get_all_feedback()
        feedback_count = get_feedback_count()
        
        return jsonify({
            'success': True,
            'feedback': feedback_list,
            'total_count': feedback_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve feedback'
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 PERFECT DeckMaster Server Starting...")
    print("=" * 60)
    print("📊 Endpoints:")
    print("  GET  /                     - Main website")
    print("  POST /api/generate         - Generate PPT")
    print("  GET  /api/job/<id>         - Job status")
    print("  GET  /api/download/<id>    - Download PPT")
    print("  GET  /api/file-info/<id>   - File information")
    print("=" * 60)
    print(f"🌐 Server: http://{HOST}:{PORT}")
    print("🔧 Admin password: DeckMaster2024!@#SecureAdmin")
    print("=" * 60)
    
    # Use PORT environment variable for Heroku deployment
    port = int(os.environ.get('PORT', PORT))
    app.run(debug=DEBUG, host='0.0.0.0', port=port, threaded=True)
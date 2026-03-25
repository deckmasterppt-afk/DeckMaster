# presentation_service.py
# Async presentation generation - returns immediately, polls for completion

import os
import time
import threading
from typing import Dict
from config import SUBSCRIPTION_PLANS, OUTPUT_FOLDER
from user_manager import user_manager
from pipeline import run_pipeline
from job_store import create_job, get_job, update_state, complete_job, fail_job

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


class PresentationService:

    def validate_generation_request(self, user_id: str, request_data: Dict) -> Dict:
        can_generate = user_manager.can_generate_ppt(user_id)
        if not can_generate['can_generate']:
            return {'valid': False, 'error': can_generate['reason']}

        task = request_data.get('task', '').strip()
        url  = request_data.get('url',  '').strip()

        if not task:
            return {'valid': False, 'error': 'Presentation topic is required'}
        if not url:
            return {'valid': False, 'error': 'URL is required for content extraction'}
        if not (url.startswith('http://') or url.startswith('https://')):
            return {'valid': False, 'error': 'Please provide a valid URL (http:// or https://)'}

        user_stats  = user_manager.get_user_stats(user_id)
        plan        = user_stats['plan']
        slide_count = int(request_data.get('slide_count', 5))

        if slide_count > plan['max_slides']:
            return {'valid': False,
                    'error': f'Max {plan["max_slides"]} slides for your plan'}

        return {'valid': True, 'user_stats': user_stats, 'slide_count': slide_count}

    def start_generation(self, user_id: str, request_data: Dict) -> Dict:
        """
        Returns immediately with a job_id.
        Generation runs in a background thread.
        Frontend polls /api/job/<job_id> until state == DONE, then downloads.
        """
        validation = self.validate_generation_request(user_id, request_data)
        if not validation['valid']:
            return {'success': False, 'error': validation['error']}

        user_stats  = validation['user_stats']
        plan        = user_stats['plan']
        slide_count = validation['slide_count']
        url         = request_data.get('url', '').strip()
        design_style = request_data.get('design_style', 'minimal_1')

        # Build visual preferences
        vp = request_data.get('visual_preferences', {})
        if user_manager.is_admin_user(user_id):
            visual_preferences = {
                'graphs':     vp.get('graphs',    False),
                'tables':     vp.get('tables',    False),
                'pie_charts': vp.get('pieCharts', False),
                'images':     vp.get('images',    False),
            }
        else:
            has_visuals = plan.get('visual_elements', False)
            visual_preferences = {
                'graphs':     has_visuals and vp.get('graphs',    False),
                'tables':     has_visuals and vp.get('tables',    False),
                'pie_charts': has_visuals and vp.get('pieCharts', False),
                'images':     has_visuals and vp.get('images',    False),
            }

        job_id = create_job(user_id, {
            'task': request_data['task'], 'url': url,
            'design_style': design_style,
            'visual_preferences': visual_preferences,
            'slide_count': slide_count,
        })

        # ── Run generation in background thread ──────────────────────
        t = threading.Thread(
            target=self._generate_bg,
            args=(job_id, url, request_data['task'],
                  design_style, visual_preferences, user_id, slide_count),
            daemon=True
        )
        t.start()

        return {
            'success': True,
            'job_id': job_id,
            'message': 'Generation started',
            'estimated_time': max(30, slide_count * 8),
        }

    def _generate_bg(self, job_id, url, task, design_style,
                     visual_preferences, user_id, slide_count):
        """Background worker - runs in its own thread."""
        try:
            update_state(job_id, 'PROCESSING')

            # Unique output path
            ts          = int(time.time() * 1000)   # ms timestamp → no collisions
            output_path = os.path.abspath(
                os.path.join(OUTPUT_FOLDER, f'DeckMaster_{ts}.pptx'))

            print(f"[GEN] Job {job_id[:8]} | {slide_count} slides | {design_style}")

            result_path = run_pipeline(
                url, task, design_style, visual_preferences, slide_count)

            # Move to our named output path if pipeline used a different name
            if os.path.abspath(result_path) != output_path:
                import shutil
                shutil.move(result_path, output_path)

            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Output file missing: {output_path}")

            size = os.path.getsize(output_path)
            print(f"[GEN] Done → {output_path} ({size//1024} KB)")

            complete_job(job_id, output_path)
            user_manager.increment_usage(user_id)

        except Exception as e:
            print(f"[GEN] FAILED job {job_id[:8]}: {e}")
            fail_job(job_id, str(e))

    def get_job_status(self, job_id: str) -> Dict:
        job = get_job(job_id)
        if not job:
            return {'success': False, 'error': 'Job not found'}

        resp = {
            'success':    True,
            'job_id':     job_id,
            'state':      job['state'],
            'created_at': job['created_at'],
        }
        if job['state'] == 'DONE':
            resp['download_url'] = f'/api/download/{job_id}'
            resp['filename'] = os.path.basename(job['output']) if job['output'] else None
        elif job['state'] == 'FAILED':
            resp['error'] = job.get('error', 'Unknown error')

        return resp


presentation_service = PresentationService()

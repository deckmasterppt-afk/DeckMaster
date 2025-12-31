# image_api_service.py
# External Image API Service for Unsplash and Pexels

import requests
import os
import io
from PIL import Image
from config import (
    UNSPLASH_ACCESS_KEY, UNSPLASH_SECRET_KEY, UNSPLASH_APPLICATION_ID,
    PEXELS_API_KEY, IMAGE_SEARCH_RESULTS_LIMIT, IMAGE_DOWNLOAD_TIMEOUT, IMAGE_MAX_SIZE
)

class ImageAPIService:
    def __init__(self):
        self.unsplash_headers = {
            'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}',
            'Accept-Version': 'v1'
        }
        self.pexels_headers = {
            'Authorization': PEXELS_API_KEY
        }
    
    def search_images(self, query, source='unsplash', limit=None):
        """Search for images from external APIs"""
        if limit is None:
            limit = IMAGE_SEARCH_RESULTS_LIMIT
            
        try:
            if source == 'unsplash':
                return self._search_unsplash(query, limit)
            elif source == 'pexels':
                return self._search_pexels(query, limit)
            else:
                # Try both sources
                unsplash_results = self._search_unsplash(query, limit // 2)
                pexels_results = self._search_pexels(query, limit // 2)
                return unsplash_results + pexels_results
        except Exception as e:
            print(f"[IMAGE_API] Error searching images: {e}")
            return []
    
    def _search_unsplash(self, query, limit):
        """Search Unsplash API"""
        try:
            url = 'https://api.unsplash.com/search/photos'
            params = {
                'query': query,
                'per_page': min(limit, 30),  # Unsplash max is 30
                'orientation': 'landscape',
                'content_filter': 'high'
            }
            
            response = requests.get(url, headers=self.unsplash_headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for photo in data.get('results', []):
                results.append({
                    'id': photo['id'],
                    'url': photo['urls']['regular'],
                    'thumb_url': photo['urls']['thumb'],
                    'description': photo.get('description', photo.get('alt_description', '')),
                    'author': photo['user']['name'],
                    'source': 'unsplash',
                    'width': photo['width'],
                    'height': photo['height']
                })
            
            print(f"[UNSPLASH] Found {len(results)} images for '{query}'")
            return results
            
        except Exception as e:
            print(f"[UNSPLASH] Error: {e}")
            return []
    
    def _search_pexels(self, query, limit):
        """Search Pexels API"""
        try:
            url = 'https://api.pexels.com/v1/search'
            params = {
                'query': query,
                'per_page': min(limit, 80),  # Pexels max is 80
                'orientation': 'landscape'
            }
            
            response = requests.get(url, headers=self.pexels_headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for photo in data.get('photos', []):
                results.append({
                    'id': photo['id'],
                    'url': photo['src']['large'],
                    'thumb_url': photo['src']['medium'],
                    'description': photo.get('alt', ''),
                    'author': photo['photographer'],
                    'source': 'pexels',
                    'width': photo['width'],
                    'height': photo['height']
                })
            
            print(f"[PEXELS] Found {len(results)} images for '{query}'")
            return results
            
        except Exception as e:
            print(f"[PEXELS] Error: {e}")
            return []
    
    def download_image(self, image_url, save_path=None):
        """Download and process image from URL"""
        try:
            response = requests.get(image_url, timeout=IMAGE_DOWNLOAD_TIMEOUT)
            response.raise_for_status()
            
            # Open image with PIL
            image = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large
            if image.width > IMAGE_MAX_SIZE or image.height > IMAGE_MAX_SIZE:
                image.thumbnail((IMAGE_MAX_SIZE, IMAGE_MAX_SIZE), Image.Resampling.LANCZOS)
            
            # Save if path provided
            if save_path:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                image.save(save_path, 'JPEG', quality=85, optimize=True)
                return save_path
            
            # Return image bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='JPEG', quality=85, optimize=True)
            img_bytes.seek(0)
            return img_bytes.getvalue()
            
        except Exception as e:
            print(f"[IMAGE_DOWNLOAD] Error downloading {image_url}: {e}")
            return None
    
    def get_image_for_slide(self, slide_content, slide_type='content'):
        """Get appropriate image for slide content"""
        try:
            # Extract keywords from slide content
            keywords = self._extract_keywords(slide_content, slide_type)
            
            if not keywords:
                keywords = ['business', 'presentation']
            
            # Search for images
            images = self.search_images(' '.join(keywords[:3]), limit=5)
            
            if images and len(images) > 0:
                # Return the best match (first result)
                best_image = images[0]
                # Ensure all required fields are present
                if isinstance(best_image, dict) and 'url' in best_image:
                    return best_image
                else:
                    print(f"[IMAGE_API] Invalid image data structure: {best_image}")
                    return None
            else:
                print(f"[IMAGE_API] No images found for keywords: {keywords}")
                return None
                
        except Exception as e:
            print(f"[IMAGE_API] Error in get_image_for_slide: {e}")
            return None
    
    def _extract_keywords(self, slide_content, slide_type):
        """Extract relevant keywords from slide content"""
        keywords = []
        
        # Get text content
        title = slide_content.get('title', '').lower()
        bullets = ' '.join(slide_content.get('bullets', [])).lower()
        content = f"{title} {bullets}"
        
        # Keyword mapping based on content
        keyword_map = {
            'business': ['business', 'corporate', 'office', 'meeting'],
            'technology': ['technology', 'computer', 'digital', 'innovation'],
            'data': ['data', 'analytics', 'chart', 'graph', 'statistics'],
            'growth': ['growth', 'success', 'achievement', 'progress'],
            'team': ['team', 'collaboration', 'people', 'group'],
            'strategy': ['strategy', 'planning', 'goals', 'vision'],
            'finance': ['finance', 'money', 'investment', 'revenue'],
            'marketing': ['marketing', 'advertising', 'brand', 'customer'],
            'education': ['education', 'learning', 'training', 'knowledge'],
            'health': ['health', 'medical', 'wellness', 'care'],
            'environment': ['environment', 'nature', 'green', 'sustainability'],
            'travel': ['travel', 'journey', 'destination', 'adventure']
        }
        
        # Find matching categories
        for category, category_keywords in keyword_map.items():
            if any(keyword in content for keyword in category_keywords):
                keywords.extend(category_keywords[:2])
        
        # Add slide type specific keywords
        if slide_type == 'title':
            keywords.extend(['presentation', 'title', 'cover'])
        elif slide_type == 'summary':
            keywords.extend(['conclusion', 'summary', 'results'])
        
        # Remove duplicates and return
        return list(set(keywords))

# Global instance
image_api = ImageAPIService()
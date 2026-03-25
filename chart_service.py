# chart_service.py
# Chart and Table Generation Service using Matplotlib and Pandas

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import io
import base64
from PIL import Image
import seaborn as sns

class ChartService:
    def __init__(self):
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
    def generate_chart_data(self, slide_content, chart_type='bar'):
        """Generate chart data based on slide content"""
        try:
            # Extract meaningful data from slide content
            title = slide_content.get('title', 'Chart')
            bullets = slide_content.get('bullets', [])
            
            # Generate data based on content
            if chart_type == 'bar':
                return self._generate_bar_data(title, bullets)
            elif chart_type == 'line':
                return self._generate_line_data(title, bullets)
            elif chart_type == 'pie':
                return self._generate_pie_data(title, bullets)
            elif chart_type == 'scatter':
                return self._generate_scatter_data(title, bullets)
            else:
                return self._generate_bar_data(title, bullets)
                
        except Exception as e:
            print(f"[CHART_DATA] Error: {e}")
            return self._get_default_data(chart_type)
    
    def _generate_bar_data(self, title, bullets):
        """Generate bar chart data"""
        categories = []
        values = []
        
        # Try to extract categories from bullets
        for bullet in bullets[:6]:  # Max 6 categories
            # Look for numbers in bullets
            words = bullet.split()
            category = ' '.join(words[:2])  # First 2 words as category
            
            # Generate realistic values
            value = np.random.randint(20, 100)
            
            categories.append(category if category else f"Category {len(categories)+1}")
            values.append(value)
        
        # Ensure we have at least 3 categories
        while len(categories) < 3:
            categories.append(f"Item {len(categories)+1}")
            values.append(np.random.randint(30, 90))
        
        return {
            'type': 'bar',
            'categories': categories,
            'values': values,
            'title': title
        }
    
    def _generate_line_data(self, title, bullets):
        """Generate line chart data"""
        # Time series data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        values = [45, 52, 48, 61, 58, 67]  # Sample growth data
        
        return {
            'type': 'line',
            'x_data': months,
            'y_data': values,
            'title': title
        }
    
    def _generate_pie_data(self, title, bullets):
        """Generate pie chart data"""
        labels = []
        sizes = []
        
        # Extract categories from bullets
        for bullet in bullets[:5]:  # Max 5 slices
            words = bullet.split()
            label = ' '.join(words[:2])
            size = np.random.randint(10, 40)
            
            labels.append(label if label else f"Segment {len(labels)+1}")
            sizes.append(size)
        
        # Ensure we have at least 3 segments
        while len(labels) < 3:
            labels.append(f"Part {len(labels)+1}")
            sizes.append(np.random.randint(15, 35))
        
        # Normalize to 100%
        total = sum(sizes)
        sizes = [int((size/total) * 100) for size in sizes]
        
        return {
            'type': 'pie',
            'labels': labels,
            'sizes': sizes,
            'title': title
        }
    
    def _generate_scatter_data(self, title, bullets):
        """Generate scatter plot data"""
        n_points = 20
        x_data = np.random.normal(50, 15, n_points)
        y_data = x_data + np.random.normal(0, 10, n_points)
        
        return {
            'type': 'scatter',
            'x_data': x_data,
            'y_data': y_data,
            'title': title
        }
    
    def _get_default_data(self, chart_type):
        """Get default data for chart type"""
        if chart_type == 'pie':
            return {
                'type': 'pie',
                'labels': ['Category A', 'Category B', 'Category C'],
                'sizes': [40, 35, 25],
                'title': 'Distribution'
            }
        elif chart_type == 'line':
            return {
                'type': 'line',
                'x_data': ['Q1', 'Q2', 'Q3', 'Q4'],
                'y_data': [45, 55, 62, 58],
                'title': 'Trend Analysis'
            }
        else:
            return {
                'type': 'bar',
                'categories': ['Item 1', 'Item 2', 'Item 3'],
                'values': [65, 78, 52],
                'title': 'Performance'
            }
    
    def create_chart_image(self, chart_data, style='modern', accent_hex=None, size=(8, 6)):
        """Create chart image using matplotlib - design-aware colours"""
        try:
            # Build colour palette from design accent
            if accent_hex:
                h = accent_hex.lstrip('#')
                ar, ag, ab = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
                # Generate 6 shades from accent
                import colorsys
                hue, sat, val = colorsys.rgb_to_hsv(ar, ag, ab)
                colors = [colorsys.hsv_to_rgb(hue, max(0.2, sat - i*0.12),
                          min(1.0, val + i*0.08)) for i in range(6)]
            elif style == 'dark':
                colors = ['#00F5FF','#39FF14','#E040FB','#F59E0B','#FF6B6B','#4DB6AC']
            else:
                colors = ['#4361EE','#E94560','#2ecc71','#f39c12','#9b59b6','#1abc9c']

            # Background
            bg_color = '#1a1a2e' if style == 'dark' else '#ffffff'
            text_color = '#ffffff' if style == 'dark' else '#1a1a2e'

            fig, ax = plt.subplots(figsize=size)
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)

            chart_type = chart_data['type']

            if chart_type == 'bar':
                bars = ax.bar(chart_data['categories'], chart_data['values'],
                              color=colors, edgecolor='none')
                ax.set_ylabel('Values', color=text_color)
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                            f'{int(height)}', ha='center', va='bottom',
                            color=text_color, fontsize=9)

            elif chart_type == 'line':
                ax.plot(chart_data['x_data'], chart_data['y_data'],
                        marker='o', linewidth=2.5, markersize=7, color=colors[0])
                ax.set_ylabel('Values', color=text_color)
                ax.grid(True, alpha=0.2, color=text_color)

            elif chart_type == 'pie':
                wedges, texts, autotexts = ax.pie(
                    chart_data['sizes'], labels=chart_data['labels'],
                    colors=colors, autopct='%1.1f%%', startangle=90,
                    textprops={'color': text_color})
                for at in autotexts:
                    at.set_color(text_color)
                ax.axis('equal')

            # Axis styling
            ax.tick_params(colors=text_color)
            for spine in ax.spines.values():
                spine.set_edgecolor(text_color)
                spine.set_alpha(0.3)
            ax.set_title(chart_data['title'], fontsize=13, fontweight='bold',
                         pad=15, color=text_color)

            plt.tight_layout()
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight',
                        facecolor=bg_color)
            img_buffer.seek(0)
            plt.close(fig)
            return img_buffer.getvalue()

        except Exception as e:
            print(f"[CHART_CREATE] Error: {e}")
            return None
    
    def create_table_data(self, slide_content):
        """Create meaningful, readable table data using pandas"""
        try:
            title = slide_content.get('title', 'Data Table')
            bullets = slide_content.get('bullets', [])
            
            # Generate table based on content with better structure
            if len(bullets) >= 3:
                # Use bullets as data source with improved formatting
                data = []
                headers = ['Category', 'Value', 'Performance']
                
                for i, bullet in enumerate(bullets[:5]):  # Max 5 rows for readability
                    words = bullet.split()
                    # Create more meaningful category names
                    category = ' '.join(words[:3]) if len(words) >= 3 else f"Item {i+1}"
                    category = category.replace('•', '').strip()  # Remove bullet points
                    
                    # Generate realistic business values
                    value_types = ['${}K'.format(np.random.randint(50, 500)),
                                  '{}%'.format(np.random.randint(5, 95)),
                                  '{}'.format(np.random.randint(100, 9999)),
                                  '{}M'.format(round(np.random.uniform(1.0, 10.0), 1))]
                    
                    value = np.random.choice(value_types)
                    performance = np.random.choice(['Excellent', 'Good', 'Growing', 'Strong', 'Improving'])
                    
                    data.append([category[:20], value, performance])  # Limit category length
                
                df = pd.DataFrame(data, columns=headers)
            else:
                # Create contextual default table based on title
                title_lower = title.lower()
                
                if any(word in title_lower for word in ['financial', 'revenue', 'sales', 'profit']):
                    # Financial table
                    data = {
                        'Metric': ['Revenue', 'Profit', 'Growth', 'Margin'],
                        'Q3 2024': ['$2.4M', '$480K', '12.5%', '20%'],
                        'Q4 2024': ['$2.8M', '$560K', '16.7%', '22%'],
                        'Status': ['↗ Growing', '↗ Strong', '↗ Good', '↗ Improving']
                    }
                elif any(word in title_lower for word in ['user', 'customer', 'engagement']):
                    # User metrics table
                    data = {
                        'Metric': ['Active Users', 'New Signups', 'Retention', 'Satisfaction'],
                        'Current': ['15.2K', '1.2K/mo', '85%', '4.2/5'],
                        'Target': ['20.0K', '1.5K/mo', '90%', '4.5/5'],
                        'Progress': ['76%', '80%', '94%', '93%']
                    }
                elif any(word in title_lower for word in ['performance', 'kpi', 'metrics']):
                    # Performance table
                    data = {
                        'KPI': ['Efficiency', 'Quality', 'Speed', 'Cost'],
                        'Current': ['92%', '4.1/5', '2.3s', '$45K'],
                        'Benchmark': ['95%', '4.5/5', '2.0s', '$40K'],
                        'Gap': ['-3%', '-0.4', '+0.3s', '+$5K']
                    }
                else:
                    # Generic business table
                    data = {
                        'Category': ['Product A', 'Product B', 'Product C', 'Product D'],
                        'Sales': ['$125K', '$98K', '$156K', '$87K'],
                        'Growth': ['+15%', '+8%', '+22%', '+5%'],
                        'Rating': ['4.2★', '3.9★', '4.5★', '3.7★']
                    }
                
                df = pd.DataFrame(data)
            
            # Add table name for potential title
            df.name = title if title != 'Data Table' else None
            
            print(f"[TABLE_DATA] Created table with {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            print(f"[TABLE_CREATE] Error: {e}")
            # Return simple fallback table
            data = {
                'Item': ['A', 'B', 'C'],
                'Value': ['100', '150', '120'],
                'Status': ['Good', 'Great', 'Fair']
            }
            return pd.DataFrame(data)
    
    def create_table_image(self, df, style='modern', accent_hex=None, size=(8, 5)):
        """Create table image - design-aware colours"""
        try:
            fig, ax = plt.subplots(figsize=size)
            ax.axis('tight')
            ax.axis('off')

            if len(df) > 6:
                df = df.head(6)

            # Derive colours from accent or style
            if accent_hex:
                header_color = accent_hex
                # Light tint for alternating rows
                h = accent_hex.lstrip('#')
                r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
                alt_color1 = f'#{min(r+40,255):02x}{min(g+40,255):02x}{min(b+40,255):02x}'
                alt_color2 = '#ffffff'
                text_color = '#ffffff'
                body_text  = '#1a1a2e' if style != 'dark' else '#e0e0e0'
            elif style == 'dark':
                header_color = '#00F5FF'; alt_color1 = '#1e293b'
                alt_color2   = '#0f172a'; text_color = '#ffffff'; body_text = '#cbd5e1'
            else:
                header_color = '#4361EE'; alt_color1 = '#f0f4ff'
                alt_color2   = '#ffffff'; text_color = '#ffffff'; body_text = '#1a1a2e'

            bg = '#1a1a2e' if style == 'dark' else '#ffffff'
            fig.patch.set_facecolor(bg)

            table = ax.table(cellText=df.values, colLabels=df.columns,
                             cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
            table.auto_set_font_size(False)
            table.set_fontsize(11)
            table.scale(1, 2.2)

            for i in range(len(df.columns)):
                cell = table[(0, i)]
                cell.set_facecolor(header_color)
                cell.set_text_props(weight='bold', color=text_color, size=12)
                cell.set_height(0.15)

            for i in range(1, len(df) + 1):
                for j in range(len(df.columns)):
                    cell = table[(i, j)]
                    cell.set_facecolor(alt_color1 if i % 2 == 1 else alt_color2)
                    cell.set_text_props(color=body_text, size=10)
                    cell.set_height(0.12)
                    cell.set_edgecolor('#d1d5db')
                    cell.set_linewidth(0.5)

            plt.tight_layout()
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='PNG', dpi=200, bbox_inches='tight',
                        facecolor=bg, edgecolor='none')
            img_buffer.seek(0)
            plt.close(fig)
            print(f"[TABLE_IMAGE] Created professional table with {len(df)} rows, {len(df.columns)} columns")
            
            return img_buffer.getvalue()
            
        except Exception as e:
            print(f"[TABLE_IMAGE] Error: {e}")
            return None

# Global instance
chart_service = ChartService()
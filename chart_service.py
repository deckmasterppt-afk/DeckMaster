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
    
    def create_chart_image(self, chart_data, style='modern', size=(8, 6)):
        """Create chart image using matplotlib"""
        try:
            fig, ax = plt.subplots(figsize=size)
            
            # Set style based on design
            if style == 'modern':
                colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
            elif style == 'corporate':
                colors = ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7', '#ecf0f1']
            else:
                colors = plt.cm.Set3(np.linspace(0, 1, 6))
            
            chart_type = chart_data['type']
            
            if chart_type == 'bar':
                bars = ax.bar(chart_data['categories'], chart_data['values'], color=colors)
                ax.set_ylabel('Values')
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}', ha='center', va='bottom')
                
            elif chart_type == 'line':
                ax.plot(chart_data['x_data'], chart_data['y_data'], 
                       marker='o', linewidth=3, markersize=8, color=colors[0])
                ax.set_ylabel('Values')
                ax.grid(True, alpha=0.3)
                
            elif chart_type == 'pie':
                wedges, texts, autotexts = ax.pie(chart_data['sizes'], 
                                                 labels=chart_data['labels'],
                                                 colors=colors,
                                                 autopct='%1.1f%%',
                                                 startangle=90)
                ax.axis('equal')
                
            elif chart_type == 'scatter':
                ax.scatter(chart_data['x_data'], chart_data['y_data'], 
                          c=colors[0], alpha=0.7, s=60)
                ax.set_xlabel('X Values')
                ax.set_ylabel('Y Values')
                ax.grid(True, alpha=0.3)
            
            # Set title
            ax.set_title(chart_data['title'], fontsize=14, fontweight='bold', pad=20)
            
            # Improve layout
            plt.tight_layout()
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='PNG', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            plt.close(fig)  # Clean up
            
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
    
    def create_table_image(self, df, style='modern', size=(8, 5)):
        """Create beautiful, professional table image using matplotlib"""
        try:
            # Create figure with better proportions for slide
            fig, ax = plt.subplots(figsize=size)
            ax.axis('tight')
            ax.axis('off')
            
            # Limit table size for better readability
            if len(df) > 6:
                df = df.head(6)  # Max 6 rows for readability
            
            # Create table with better styling
            table = ax.table(cellText=df.values,
                           colLabels=df.columns,
                           cellLoc='center',
                           loc='center',
                           bbox=[0, 0, 1, 1])  # Full figure
            
            # IMPROVED: Better table styling
            table.auto_set_font_size(False)
            table.set_fontsize(11)  # Readable font size
            table.scale(1, 2.2)  # Better row height
            
            # Professional color scheme based on style
            if style == 'modern':
                header_color = '#2c3e50'  # Dark blue-gray
                alt_color1 = '#ecf0f1'    # Light gray
                alt_color2 = '#ffffff'    # White
                text_color = '#2c3e50'    # Dark text
            elif style == 'corporate':
                header_color = '#1e3a8a'  # Corporate blue
                alt_color1 = '#f1f5f9'    # Very light blue
                alt_color2 = '#ffffff'    # White
                text_color = '#1e3a8a'    # Corporate blue text
            else:
                header_color = '#374151'  # Dark gray
                alt_color1 = '#f9fafb'    # Very light gray
                alt_color2 = '#ffffff'    # White
                text_color = '#374151'    # Dark gray text
            
            # Style header row
            for i in range(len(df.columns)):
                cell = table[(0, i)]
                cell.set_facecolor(header_color)
                cell.set_text_props(weight='bold', color='white', size=12)
                cell.set_height(0.15)  # Header height
            
            # Style data rows with alternating colors
            for i in range(1, len(df) + 1):
                for j in range(len(df.columns)):
                    cell = table[(i, j)]
                    # Alternate row colors for better readability
                    color = alt_color1 if i % 2 == 1 else alt_color2
                    cell.set_facecolor(color)
                    cell.set_text_props(color=text_color, size=10)
                    cell.set_height(0.12)  # Data row height
                    
                    # Add subtle border
                    cell.set_edgecolor('#d1d5db')
                    cell.set_linewidth(0.5)
            
            # Add title if DataFrame has a name
            if hasattr(df, 'name') and df.name:
                plt.title(df.name, fontsize=14, fontweight='bold', pad=15, color=text_color)
            
            # Improve layout
            plt.tight_layout()
            plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
            
            # Save to bytes with high quality
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='PNG', dpi=200, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            
            plt.close(fig)  # Clean up
            
            print(f"[TABLE_IMAGE] Created professional table with {len(df)} rows, {len(df.columns)} columns")
            
            return img_buffer.getvalue()
            
        except Exception as e:
            print(f"[TABLE_IMAGE] Error: {e}")
            return None

# Global instance
chart_service = ChartService()
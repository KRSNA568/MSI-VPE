"""
PDF Export Service for MSI-VPE
Generates professional filmmaker-friendly PDF reports
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

try:
    # Lazy import to avoid circular deps if any
    from app.services.ai_text_service import get_ai_text_service
except Exception as _e:
    get_ai_text_service = None


class PDFExporter:
    """Generates filmmaker-friendly PDF reports from analysis results"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Create custom styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#007acc'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        # Scene header style
        self.styles.add(ParagraphStyle(
            name='SceneHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#252526'),
            spaceAfter=12,
            spaceBefore=20
        ))

        # Beat header style
        self.styles.add(ParagraphStyle(
            name='BeatHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#007acc'),
            spaceAfter=8,
            spaceBefore=12
        ))

    def _normalize_scenes(self, analysis_result: dict) -> list:
        """Accept either {scenes: [...]} or a single-scene dict and return list of scenes."""
        if not analysis_result:
            return []
        if isinstance(analysis_result, dict) and "scenes" in analysis_result:
            scenes = analysis_result.get("scenes") or []
            return scenes
        # Single scene shape
        return [analysis_result]

    def generate_pdf(self, analysis_data: dict, script_filename: str) -> BytesIO:
        """
        Generate a PDF report from analysis data
        
        Args:
            analysis_data: The analysis result dictionary
            script_filename: Original screenplay filename
            
        Returns:
            BytesIO: PDF file in memory
        """
        logger.info(f"Generating PDF for {script_filename}")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )

        # Build PDF content
        story = []
        
        # Title page
        story.append(Paragraph(
            "SCREENPLAY EMOTION ANALYSIS",
            self.styles['CustomTitle']
        ))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(
            f"<b>Script:</b> {script_filename}",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.5*inch))

        # Executive Summary
        story.append(Paragraph("<b>EXECUTIVE SUMMARY</b>", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        analysis_result = analysis_data.get('analysis_result', {})
        scenes = self._normalize_scenes(analysis_result)
        total_beats = sum(len(scene.get('beats', [])) for scene in scenes)
        
        summary_data = [
            ['Total Scenes', str(len(scenes))],
            ['Total Beats', str(total_beats)],
            ['Analysis Status', analysis_data.get('status', 'completed').upper()]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        story.append(summary_table)
        # Optional: AI-generated executive narrative
        if get_ai_text_service:
            try:
                ai = get_ai_text_service()
                exec_text = ai.generate_executive_summary(
                    {"scenes": scenes}, script_filename
                )
                if exec_text:
                    story.append(Spacer(1, 0.2*inch))
                    story.append(Paragraph("Director's Overview", self.styles['Heading3']))
                    story.append(Paragraph(exec_text, self.styles['Normal']))
            except Exception as e:
                logger.warning(f"AI executive summary failed: {e}")

        story.append(PageBreak())

        # Scene-by-scene breakdown
        for scene_idx, scene in enumerate(scenes, 1):
            story.append(Paragraph(
                f"SCENE {scene_idx}",
                self.styles['SceneHeader']
            ))
            
            scene_loc = scene.get('scene_location', 'UNKNOWN')
            story.append(Paragraph(
                f"<b>Location:</b> {scene_loc}",
                self.styles['Normal']
            ))
            story.append(Spacer(1, 0.1*inch))

            # AI scene overview and shot list
            if get_ai_text_service:
                try:
                    ai = get_ai_text_service()
                    overview = ai.generate_scene_overview(scene, scene_idx)
                    if overview:
                        story.append(Paragraph("Scene Overview", self.styles['Heading3']))
                        story.append(Paragraph(overview, self.styles['Normal']))
                        story.append(Spacer(1, 0.1*inch))
                    shots = ai.generate_shot_list(scene, count=5)
                    if shots:
                        story.append(Paragraph("Suggested Shot List", self.styles['Heading4']))
                        # Render as a simple two-column table if long
                        shot_rows = [[f"• {s}"] for s in shots]
                        shot_table = Table(shot_rows, colWidths=[5.5*inch])
                        shot_table.setStyle(TableStyle([
                            ('FONTSIZE', (0, 0), (-1, -1), 9),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
                        ]))
                        story.append(shot_table)
                        story.append(Spacer(1, 0.1*inch))
                except Exception as e:
                    logger.warning(f"AI scene text failed: {e}")

            # Process each beat
            beats = scene.get('beats', [])
            for beat_idx, beat in enumerate(beats, 1):
                beat_elements = []
                
                # Get characters and emotional info for header
                characters = beat.get('characters', [])
                emotional_arc = beat.get('emotional_arc', {})
                primary_raw = emotional_arc.get('primary_emotion', {})
                if isinstance(primary_raw, dict):
                    beat_emotion = primary_raw.get('emotion', 'neutral')
                else:
                    beat_emotion = str(primary_raw)
                
                # Beat header with character/emotion context
                header_text = f"Beat {beat_idx}"
                if characters:
                    header_text += f" - {', '.join(characters)}"
                header_text += f" ({beat_emotion.replace('_', ' ').title()})"
                
                beat_elements.append(Paragraph(
                    header_text,
                    self.styles['BeatHeader']
                ))
                
                # Dialogue/Action content
                dialogue_lines = beat.get('dialogue', [])
                action_lines = beat.get('action', [])
                characters = beat.get('characters', [])
                
                # Build content preview
                content_parts = []
                if action_lines:
                    content_parts.extend([f"[{line}]" for line in action_lines])
                if dialogue_lines:
                    char_name = characters[0] if characters else "CHARACTER"
                    content_parts.extend([f"{char_name}: {line}" for line in dialogue_lines])
                
                if content_parts:
                    content = " ".join(content_parts)
                    snippet = content[:200]
                    if len(content) > 200:
                        snippet += '...'
                    beat_elements.append(Paragraph(
                        f"<i>{snippet}</i>",
                        self.styles['Normal']
                    ))
                    beat_elements.append(Spacer(1, 0.1*inch))

                # Emotional analysis
                emotional_arc = beat.get('emotional_arc', {})
                if emotional_arc:
                    primary_raw = emotional_arc.get('primary_emotion') or emotional_arc.get('emotion') or 'neutral'
                    if isinstance(primary_raw, dict):
                        primary_emotion = primary_raw.get('emotion', 'neutral')
                        intensity_val = primary_raw.get('intensity', emotional_arc.get('overall_intensity', 0))
                    else:
                        primary_emotion = str(primary_raw)
                        intensity_val = emotional_arc.get('overall_intensity', emotional_arc.get('intensity', 0))
                    try:
                        intensity = float(intensity_val)
                    except Exception:
                        intensity = 0.0
                    
                    emotion_data = [
                        ['<b>Primary Emotion</b>', primary_emotion.title()],
                        ['<b>Intensity</b>', f"{intensity:.2f}"]
                    ]
                    
                    emotion_table = Table(emotion_data, colWidths=[2*inch, 3.5*inch])
                    emotion_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))
                    beat_elements.append(emotion_table)
                    beat_elements.append(Spacer(1, 0.1*inch))

                # Visual recommendations (support both legacy visual_recommendations and visual_signals)
                visual_recs = beat.get('visual_recommendations') or beat.get('visual_signals', {})
                if visual_recs:
                    beat_elements.append(Paragraph(
                        "<b>CINEMATOGRAPHY RECOMMENDATIONS</b>",
                        self.styles['Heading4']
                    ))
                    
                    # Add reasoning first if available
                    reasoning = visual_recs.get('reasoning', '')
                    if reasoning:
                        beat_elements.append(Paragraph(
                            f"<i>{reasoning}</i>",
                            self.styles['Normal']
                        ))
                        beat_elements.append(Spacer(1, 0.1*inch))
                    
                    # Camera work
                    camera = visual_recs.get('camera', {})
                    if camera:
                        def _format_value(val):
                            if isinstance(val, list):
                                return ', '.join([str(v).replace('_', ' ').title() for v in val])
                            if val is None or val == '':
                                return 'N/A'
                            return str(val).replace('_', ' ').title()
                        
                        shot_size = _format_value(camera.get('shot_size'))
                        movement = _format_value(camera.get('movement'))
                        vertical_angle = _format_value(camera.get('vertical_angle'))
                        horizontal_angle = _format_value(camera.get('horizontal_angle'))
                        focal_length = camera.get('focal_length_mm', '')
                        depth = _format_value(camera.get('depth_of_field'))
                        
                        camera_data = [
                            ['Shot Size', shot_size],
                            ['Camera Movement', movement],
                            ['Vertical Angle', vertical_angle],
                            ['Horizontal Angle', horizontal_angle]
                        ]
                        if focal_length:
                            camera_data.append(['Focal Length', f"{focal_length}mm"])
                        if depth and depth != 'N/A':
                            camera_data.append(['Depth of Field', depth])
                        
                        if camera_data:
                            camera_table = Table(camera_data, colWidths=[1.5*inch, 4*inch])
                            camera_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f8f8')),
                                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, -1), 8),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                                ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
                                ('VALIGN', (0, 0), (-1, -1), 'TOP')
                            ]))
                            beat_elements.append(camera_table)
                            beat_elements.append(Spacer(1, 0.05*inch))
                    
                    # Lighting
                    lighting = visual_recs.get('lighting', {})
                    if lighting:
                        def _format_light_val(val):
                            if val is None or val == '':
                                return 'N/A'
                            return str(val).replace('_', ' ').title()
                        
                        quality = lighting.get('quality', 'N/A')
                        if isinstance(quality, (int, float)):
                            quality = f"{quality}% Hard" if quality > 50 else f"{100-quality}% Soft"
                        direction = _format_light_val(lighting.get('direction'))
                        temperature = lighting.get('temperature_kelvin', '')
                        if temperature:
                            temperature = f"{temperature}K"
                        else:
                            temperature = 'N/A'
                        intensity = _format_light_val(lighting.get('intensity'))
                        contrast = lighting.get('contrast_ratio', 'N/A')
                        shadow_type = _format_light_val(lighting.get('shadow_type'))
                        technique = _format_light_val(lighting.get('technique'))
                        
                        lighting_data = [
                            ['Setup', quality],
                            ['Direction', direction],
                            ['Temperature', temperature],
                            ['Intensity', intensity],
                            ['Contrast Ratio', contrast],
                            ['Shadow Type', shadow_type]
                        ]
                        if technique and technique != 'N/A':
                            lighting_data.append(['Technique', technique])
                        
                        lighting_table = Table(lighting_data, colWidths=[1.5*inch, 4*inch])
                        lighting_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f8f8')),
                            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 8),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                            ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey)
                        ]))
                        beat_elements.append(lighting_table)
                        beat_elements.append(Spacer(1, 0.05*inch))
                    
                    # Color palette
                    colors_obj = visual_recs.get('colors', {})
                    if colors_obj:
                        primary_colors = colors_obj.get('primary_colors', [])
                        secondary_colors = colors_obj.get('secondary_colors', [])
                        accent_colors = colors_obj.get('accent_colors', [])
                        saturation = colors_obj.get('saturation', '')
                        brightness = colors_obj.get('brightness', '')
                        harmony = colors_obj.get('harmony_type', '')
                        
                        if primary_colors or secondary_colors or accent_colors:
                            color_text = []
                            if primary_colors:
                                color_text.append(f"<b>Primary:</b> {', '.join(primary_colors)}")
                            if secondary_colors:
                                color_text.append(f"<b>Secondary:</b> {', '.join(secondary_colors)}")
                            if accent_colors:
                                color_text.append(f"<b>Accent:</b> {', '.join(accent_colors)}")
                            if harmony:
                                color_text.append(f"<b>Harmony:</b> {str(harmony).replace('_', ' ').title()}")
                            if saturation or brightness:
                                color_text.append(f"<b>Properties:</b> Saturation {saturation}%, Brightness {brightness}%")
                            beat_elements.append(Paragraph(
                                '<br/>'.join(color_text),
                                self.styles['Normal']
                            ))
                
                beat_elements.append(Spacer(1, 0.2*inch))
                
                # Keep beat elements together
                story.append(KeepTogether(beat_elements))
            
            # Add page break between scenes
            if scene_idx < len(scenes):
                story.append(PageBreak())

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        logger.info(f"PDF generated successfully for {script_filename}")
        return buffer


# Singleton instance
_pdf_exporter = None


def get_pdf_exporter() -> PDFExporter:
    """Get the singleton PDF exporter instance"""
    global _pdf_exporter
    if _pdf_exporter is None:
        _pdf_exporter = PDFExporter()
    return _pdf_exporter

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(analysis_results: dict, output_path: str):
    """
    Generates a professional PDF report from the PolicyGuard analysis results.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom colors
    PRIMARY_COLOR = colors.HexColor("#1E293B")  # Dark slate
    SECONDARY_COLOR = colors.HexColor("#0F172A") # Near black
    ACCENT_COLOR = colors.HexColor("#F59E0B")    # Amber
    BORDER_COLOR = colors.HexColor("#E2E8F0")    # Light gray
    TEXT_COLOR = colors.HexColor("#334155")      # Slate gray
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY_COLOR,
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=25
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY_COLOR,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_COLOR
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBodyTextCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    th_style = ParagraphStyle(
        'TableHeaderText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.white
    )
    
    badge_conflict = ParagraphStyle(
        'BadgeConflict',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#991B1B") # Dark red
    )
    
    badge_redundant = ParagraphStyle(
        'BadgeRedundant',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#C2410C") # Dark orange
    )
    
    badge_stale = ParagraphStyle(
        'BadgeStale',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#854D0E") # Dark yellow
    )
    
    story = []
    
    # 1. Title Block
    story.append(Paragraph("PolicyGuard - Policy Governance Report", title_style))
    story.append(Paragraph("Societe Generale Compliance & Policy Staleness Audit Summary", subtitle_style))
    story.append(Spacer(1, 10))
    
    # 2. Executive Summary Metrics
    health_score = analysis_results["health_score"]
    metrics = analysis_results["metrics"]
    
    # Determine Health Status Text
    if health_score >= 80:
        health_status = "HEALTHY"
        status_color = "#10B981" # Emerald
    elif health_score >= 50:
        health_status = "WARNING"
        status_color = "#F59E0B" # Amber
    else:
        health_status = "CRITICAL"
        status_color = "#EF4444" # Red
        
    metrics_data = [
        [
            Paragraph("<b>Policy Health Score</b>", body_style),
            Paragraph(f"<font color='{status_color}'><b>{health_score} / 100</b> ({health_status})</font>", bold_body_style)
        ],
        [
            Paragraph("<b>Total Obligations</b>", body_style),
            Paragraph(str(metrics["total_obligations"]), body_style)
        ],
        [
            Paragraph("<b>Detected Conflicts</b>", body_style),
            Paragraph(str(metrics["conflicts"]), body_style)
        ],
        [
            Paragraph("<b>Detected Redundancies</b>", body_style),
            Paragraph(str(metrics["redundancies"]), body_style)
        ],
        [
            Paragraph("<b>Stale Documents / Superseded References</b>", body_style),
            Paragraph(str(metrics["stale_policies"]), body_style)
        ]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[200, 320])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(Paragraph("Executive Summary", section_heading))
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # 3. Conflicts & Potential Conflicts List
    story.append(Paragraph("1. Policy Conflicts & Potential Conflicts", section_heading))
    conflicts = [r for r in analysis_results["relations"] if r["type"] in ["CONFLICT", "POTENTIAL_CONFLICT"]]
    
    if not conflicts:
        story.append(Paragraph("No active policy conflicts detected.", body_style))
    else:
        conflict_data = [[
            Paragraph("Type", th_style),
            Paragraph("Source Clause", th_style),
            Paragraph("Target Clause", th_style),
            Paragraph("Description", th_style)
        ]]
        
        for c in conflicts:
            badge = Paragraph(f"<b>{c['type']}</b>", badge_conflict if c['type'] == 'CONFLICT' else badge_redundant)
            
            src_cell = f"<b>{c['source_doc']}</b><br/>Sec: {c['source_section']}<br/><font size='8' color='#475569'>{c['source_text']}</font>"
            tgt_cell = f"<b>{c['target_doc']}</b><br/>Sec: {c['target_section']}<br/><font size='8' color='#475569'>{c['target_text']}</font>"
            
            conflict_data.append([
                badge,
                Paragraph(src_cell, body_style),
                Paragraph(tgt_cell, body_style),
                Paragraph(c["explanation"], body_style)
            ])
            
        conflict_table = Table(conflict_data, colWidths=[80, 140, 140, 160])
        conflict_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(conflict_table)
        
    story.append(Spacer(1, 15))
    
    # 4. Redundancies List
    story.append(Paragraph("2. Policy Redundancies", section_heading))
    redundancies = [r for r in analysis_results["relations"] if r["type"] == "REDUNDANT"]
    
    if not redundancies:
        story.append(Paragraph("No redundant policy clauses detected.", body_style))
    else:
        redundant_data = [[
            Paragraph("Clause A", th_style),
            Paragraph("Clause B", th_style),
            Paragraph("Description", th_style)
        ]]
        
        for r in redundancies:
            src_cell = f"<b>{r['source_doc']}</b> (Sec {r['source_section']})<br/><font size='8'>{r['source_text']}</font>"
            tgt_cell = f"<b>{r['target_doc']}</b> (Sec {r['target_section']})<br/><font size='8'>{r['target_text']}</font>"
            
            redundant_data.append([
                Paragraph(src_cell, body_style),
                Paragraph(tgt_cell, body_style),
                Paragraph(r["explanation"], body_style)
            ])
            
        redundant_table = Table(redundant_data, colWidths=[170, 170, 180])
        redundant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(redundant_table)
        
    story.append(Spacer(1, 15))
    
    # 5. Staleness & Superseded Tech List
    story.append(Paragraph("3. Stale Policies & Superseded Technology References", section_heading))
    stale_items = []
    for o in analysis_results["obligations"]:
        if o["is_stale"]:
            stale_items.append(o)
            
    if not stale_items:
        story.append(Paragraph("No stale policy documents or superseded technology references detected.", body_style))
    else:
        stale_data = [[
            Paragraph("Document", th_style),
            Paragraph("Section", th_style),
            Paragraph("Clause Text", th_style),
            Paragraph("Staleness Finding", th_style)
        ]]
        
        for s in stale_items:
            reasons_html = "<br/>".join([f"&bull; {r}" for r in s["staleness_reasons"]])
            stale_data.append([
                Paragraph(f"<b>{s['source_doc']}</b><br/><font size='8' color='#64748B'>Reviewed: {s['last_reviewed']}</font>", body_style),
                Paragraph(s["section"], body_style),
                Paragraph(s["raw_text"], body_style),
                Paragraph(reasons_html, badge_stale)
            ])
            
        stale_table = Table(stale_data, colWidths=[120, 50, 170, 180])
        stale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(stale_table)
        
    # Build Document
    doc.build(story)

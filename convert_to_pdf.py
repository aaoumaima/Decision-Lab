import markdown
import sys
import os

def md_to_pdf_html(md_file, output_file):
    """Convert markdown to a styled HTML file that can be printed as PDF."""
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Remove mermaid code blocks (they won't render in static HTML)
    import re
    md_content = re.sub(r'```mermaid\n.*?```', '[Diagramme - voir version interactive]', md_content, flags=re.DOTALL)
    md_content = re.sub(r'```\n[^`]*?\n```', lambda m: m.group(0) if '```' not in m.group(0)[3:-3] else m.group(0), md_content, flags=re.DOTALL)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content, 
        extensions=['tables', 'fenced_code', 'toc', 'nl2br'],
        output_format='html5'
    )
    
    # Create styled HTML document
    styled_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Revue Systématique de la Littérature</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.7;
            color: #1a1a2e;
            background: #ffffff;
            padding: 40px 60px;
            max-width: 1000px;
            margin: 0 auto;
            font-size: 11pt;
        }}
        
        h1 {{
            font-size: 24pt;
            font-weight: 700;
            color: #0f3460;
            margin-top: 30px;
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 3px solid #e94560;
            page-break-after: avoid;
        }}
        
        h2 {{
            font-size: 18pt;
            font-weight: 600;
            color: #16213e;
            margin-top: 35px;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 2px solid #0f3460;
            page-break-after: avoid;
        }}
        
        h3 {{
            font-size: 14pt;
            font-weight: 600;
            color: #0f3460;
            margin-top: 25px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }}
        
        h4 {{
            font-size: 12pt;
            font-weight: 600;
            color: #533483;
            margin-top: 18px;
            margin-bottom: 6px;
        }}
        
        p {{
            margin-bottom: 10px;
            text-align: justify;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 9.5pt;
            page-break-inside: avoid;
        }}
        
        th {{
            background: linear-gradient(135deg, #0f3460, #16213e);
            color: white;
            padding: 10px 12px;
            text-align: left;
            font-weight: 600;
            font-size: 9pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 8px 12px;
            border-bottom: 1px solid #e8e8e8;
            vertical-align: top;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        tr:hover {{
            background-color: #e8f0fe;
        }}
        
        blockquote {{
            border-left: 4px solid #e94560;
            padding: 12px 20px;
            margin: 15px 0;
            background: #fef5f7;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: #333;
        }}
        
        code {{
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 9pt;
            color: #e94560;
        }}
        
        pre {{
            background: #1a1a2e;
            color: #a9d1e8;
            padding: 16px 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            font-size: 9pt;
            line-height: 1.5;
        }}
        
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}
        
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, #e94560, #0f3460, #533483);
            margin: 30px 0;
        }}
        
        strong {{
            color: #0f3460;
            font-weight: 600;
        }}
        
        a {{
            color: #e94560;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        ul, ol {{
            margin: 8px 0 15px 25px;
        }}
        
        li {{
            margin-bottom: 4px;
        }}
        
        /* Cover page styling */
        body > h1:first-of-type {{
            text-align: center;
            font-size: 28pt;
            margin-top: 60px;
            border-bottom: 4px solid #e94560;
            padding-bottom: 15px;
        }}
        
        body > h2:first-of-type {{
            text-align: center;
            font-size: 16pt;
            color: #533483;
            border-bottom: none;
            margin-top: 10px;
        }}
        
        body > h3:first-of-type {{
            text-align: center;
            font-size: 12pt;
            color: #666;
            font-weight: 400;
            margin-bottom: 40px;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                padding: 20px 40px;
                font-size: 10pt;
            }}
            
            h1 {{ page-break-after: avoid; }}
            h2 {{ page-break-after: avoid; page-break-before: auto; }}
            table {{ page-break-inside: avoid; }}
            
            @page {{
                size: A4;
                margin: 2cm;
            }}
        }}
        
        /* Alert boxes */
        .alert {{
            padding: 12px 16px;
            border-radius: 8px;
            margin: 12px 0;
            font-size: 10pt;
        }}
    </style>
</head>
<body>
{html_content}

<div style="margin-top: 60px; padding-top: 20px; border-top: 2px solid #e8e8e8; text-align: center; color: #888; font-size: 9pt;">
    <p>Document généré automatiquement — Revue Systématique de la Littérature</p>
    <p>Août 2026 — 261+ articles identifiés à travers 11 bases de données et 7 flux de recherche</p>
</div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(styled_html)
    
    print(f"HTML créé: {output_file}")
    return output_file

if __name__ == "__main__":
    md_file = r"e:\IA PFE\presentation_revue_systematique.md"
    html_file = r"e:\IA PFE\presentation_revue_systematique.html"
    
    md_to_pdf_html(md_file, html_file)
    print("Conversion terminée!")
    print(f"Fichier HTML: {html_file}")
    print("Pour obtenir le PDF: Ouvrez le fichier HTML dans votre navigateur et imprimez en PDF (Ctrl+P)")

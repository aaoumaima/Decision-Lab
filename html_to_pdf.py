"""
Convert MD to PDF using Python's built-in capabilities.
Uses markdown + reportlab for direct PDF generation without external dependencies.
"""
import markdown
import re
import os

def create_pdf_from_html(html_file, pdf_file):
    """Use playwright or selenium to print HTML to PDF, or fall back to manual instructions."""
    try:
        # Try using msedge or chrome headless mode for PDF
        import subprocess
        
        # Try Microsoft Edge first (available on Windows by default)
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        
        browser_path = None
        for path in edge_paths + chrome_paths:
            if os.path.exists(path):
                browser_path = path
                break
        
        if browser_path:
            abs_html = os.path.abspath(html_file)
            abs_pdf = os.path.abspath(pdf_file)
            file_url = f"file:///{abs_html.replace(os.sep, '/')}"
            
            cmd = [
                browser_path,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--print-to-pdf={abs_pdf}",
                "--print-to-pdf-no-header",
                "--no-pdf-header-footer",
                file_url
            ]
            
            print(f"Utilisation du navigateur: {os.path.basename(browser_path)}")
            print(f"URL: {file_url}")
            print(f"PDF: {abs_pdf}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if os.path.exists(abs_pdf):
                size_kb = os.path.getsize(abs_pdf) / 1024
                print(f"\n✅ PDF créé avec succès!")
                print(f"📄 Fichier: {abs_pdf}")
                print(f"📊 Taille: {size_kb:.1f} KB")
                return True
            else:
                print(f"⚠️ Le PDF n'a pas été créé. stderr: {result.stderr}")
                return False
        else:
            print("❌ Aucun navigateur trouvé (Edge/Chrome)")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    html_file = r"e:\IA PFE\presentation_revue_systematique.html"
    pdf_file = r"e:\IA PFE\Revue_Systematique_Litterature.pdf"
    
    if not os.path.exists(html_file):
        print("❌ Fichier HTML introuvable. Exécutez d'abord convert_to_pdf.py")
    else:
        success = create_pdf_from_html(html_file, pdf_file)
        if not success:
            print("\n📋 Alternative manuelle:")
            print(f"   1. Ouvrez le fichier: {html_file}")
            print(f"   2. Appuyez sur Ctrl+P")
            print(f"   3. Sélectionnez 'Enregistrer en PDF'")
            print(f"   4. Enregistrez sous: {pdf_file}")

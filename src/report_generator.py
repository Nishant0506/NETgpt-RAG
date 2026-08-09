from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ReportGenerator:
    def build_pdf(self, analysis: dict) -> BytesIO:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("NetGPT Report")
        pdf.drawString(40, 760, "NetGPT Troubleshooting Report")
        pdf.drawString(40, 740, f"Filename: {analysis.get('filename', 'unknown')}")
        pdf.drawString(40, 720, f"Summary: {analysis.get('summary', '')}")
        y = 690
        for finding in analysis.get('findings', []):
            pdf.drawString(40, y, f"- {finding['issue']} ({finding['severity']})")
            y -= 20
            if y < 60:
                pdf.showPage()
                y = 760
        pdf.save()
        buffer.seek(0)
        return buffer

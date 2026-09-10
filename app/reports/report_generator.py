from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_report(result):

    report = f"""
LEGAL DOCUMENT ANALYSIS REPORT

IMPORTANT CLAUSES

{result.get("reader_result", "No reader analysis available.")}

LEGAL RISKS

{result.get("risk_result", "No risk analysis available.")}

SUMMARY

{result.get("summary_result", "No summary available.")}
"""

    return report


def generate_pdf_report(result, filename="legal_report.pdf"):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "LEGAL DOCUMENT ANALYSIS REPORT",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "IMPORTANT CLAUSES",
            styles["Heading2"]
        )
    )

    reader_result = result.get(
        "reader_result",
        "No reader analysis available."
    )

    story.append(
        Paragraph(
            reader_result.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "LEGAL RISKS",
            styles["Heading2"]
        )
    )

    risk_result = result.get(
        "risk_result",
        "No risk analysis available."
    )

    story.append(
        Paragraph(
            risk_result.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "SUMMARY",
            styles["Heading2"]
        )
    )

    summary_result = result.get(
        "summary_result",
        "No summary available."
    )

    story.append(
        Paragraph(
            summary_result.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors

# Create PDF
pdf_path = 'Recommendation_Letter.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        rightMargin=1*inch, leftMargin=1*inch,
                        topMargin=1*inch, bottomMargin=1*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#000000'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#000000'),
    spaceAfter=12,
    alignment=TA_JUSTIFY,
    fontName='Helvetica',
    leading=14
)

address_style = ParagraphStyle(
    'Address',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#000000'),
    spaceAfter=6,
    alignment=TA_LEFT,
    fontName='Helvetica',
    leading=14
)

subject_style = ParagraphStyle(
    'Subject',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#000000'),
    spaceAfter=12,
    spaceBefore=12,
    alignment=TA_LEFT,
    fontName='Helvetica-Bold',
    leading=14
)

signature_style = ParagraphStyle(
    'Signature',
    parent=styles['Normal'],
    fontSize=11,
    textColor=colors.HexColor('#000000'),
    spaceAfter=6,
    spaceBefore=24,
    alignment=TA_LEFT,
    fontName='Helvetica',
    leading=14
)

# Add content
elements.append(Paragraph("RECOMMENDATION LETTER", title_style))
elements.append(Spacer(1, 0.3*inch))

elements.append(Paragraph("Date: January 13, 2026", address_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("UK Visas and Immigration", address_style))
elements.append(Paragraph("Home Office", address_style))
elements.append(Paragraph("United Kingdom", address_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("RE: Recommendation Letter in Support of Global Talent Visa Application", subject_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("Dear Sir/Madam,", body_style))
elements.append(Spacer(1, 0.15*inch))

# Main body paragraphs
para1 = ("I am writing to provide my strong recommendation in support of Deborah Akuoko's application "
         "for a Global Talent visa to the United Kingdom. As the Director of Project Assist Global Limited (PAGL), "
         "I have had the distinct pleasure of working directly with Deborah Akuoko and can attest to their exceptional "
         "technical capabilities, professional dedication, and significant contributions to our organization.")
elements.append(Paragraph(para1, body_style))
elements.append(Spacer(1, 0.15*inch))

para2 = ("During Deborah Akuoko's tenure with our company, they demonstrated outstanding technical skills in computer "
         "software development and deployment. Their expertise was instrumental in supporting critical web and mobile "
         "applications deployments for a major corporate banking client. Deborah Akuoko consistently delivered high-quality "
         "technical solutions that met and exceeded project requirements, playing a crucial role in the success of our "
         "client engagements.")
elements.append(Paragraph(para2, body_style))
elements.append(Spacer(1, 0.15*inch))

para3 = ("What particularly impressed me about Deborah Akuoko was their remarkable ability as a fast learner. When tasked "
         "with ATM machine deployments and operations-a complex technical domain requiring specialized knowledge-"
         "Deborah Akuoko quickly mastered the necessary skills and became proficient in this area. This was particularly "
         "valuable as these responsibilities were part of a fast-paced transformation program for a corporate bank, "
         "where adaptability and rapid skill acquisition were essential for project success.")
elements.append(Paragraph(para3, body_style))
elements.append(Spacer(1, 0.15*inch))

para4 = ("Beyond their technical competencies, Deborah Akuoko possesses an exceptional quality that sets them apart: "
         "an insatiable curiosity that enables them to solve novel problems on a daily basis. This intellectual "
         "curiosity, combined with their technical expertise, makes Deborah Akuoko an invaluable asset to any organization. "
         "They consistently approach challenges with innovative thinking and demonstrate the kind of problem-solving "
         "ability that drives technological advancement.")
elements.append(Paragraph(para4, body_style))
elements.append(Spacer(1, 0.15*inch))

para5 = ("Deborah Akuoko's contributions to our projects have been significant, and their work has directly supported "
         "the digital transformation initiatives of a major financial institution. Their technical skills, combined "
         "with their ability to quickly adapt to new technologies and solve complex problems, align perfectly with "
         "the criteria for exceptional talent that the Global Talent visa program seeks to attract to the United Kingdom.")
elements.append(Paragraph(para5, body_style))
elements.append(Spacer(1, 0.15*inch))

para6 = ("I have no hesitation in recommending Deborah Akuoko for the Global Talent visa. They represent exactly the "
         "kind of high-caliber professional that would make valuable contributions to the UK's technology sector and "
         "broader economy. Their technical expertise, combined with their innovative problem-solving abilities and "
         "professional dedication, would be an asset to any UK-based organization.")
elements.append(Paragraph(para6, body_style))
elements.append(Spacer(1, 0.15*inch))

para7 = ("Should you require any additional information or clarification, please do not hesitate to contact me.")
elements.append(Paragraph(para7, body_style))
elements.append(Spacer(1, 0.8*inch))

# Signature
elements.append(Paragraph("Yours sincerely,", signature_style))
elements.append(Spacer(1, 0.4*inch))
elements.append(Paragraph("Anita Appiah", signature_style))
elements.append(Paragraph("Director", signature_style))
elements.append(Paragraph("Project Assist Global Limited (PAGL)", signature_style))
elements.append(Paragraph("[Contact Information]", signature_style))

# Build PDF
doc.build(elements)
print(f"PDF created successfully: {pdf_path}")

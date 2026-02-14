#!/usr/bin/env python3
"""
Generate a Global Talent Visa recommendation letter from Ghana High Commissioner Zita Benson.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from datetime import datetime

def create_recommendation_letter():
    """Create the recommendation letter PDF."""
    
    # Create PDF document
    pdf_path = '/Users/pd3rvr/Documents/pubs/THESIS/Ukvi/zita/sample_recommendation_letter.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles - using Garamond font
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor='black',
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Times-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Times-Roman'
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=24,
        fontName='Times-Roman'
    )
    
    # Letter content
    date = datetime.now().strftime("%d %B %Y")
    
    # Header
    story.append(Paragraph("Ghana High Commission", title_style))
    story.append(Paragraph("London, United Kingdom", normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Date
    story.append(Paragraph(date, normal_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Recipient
    story.append(Paragraph("UK Visas and Immigration", normal_style))
    story.append(Paragraph("Home Office", normal_style))
    story.append(Paragraph("United Kingdom", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Subject
    story.append(Paragraph("<b>Subject: Recommendation Letter for Global Talent Visa Application</b>", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Salutation
    story.append(Paragraph("Dear Sir/Madam,", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Introduction
    intro_text = """
    I am writing in my official capacity as the High Commissioner of Ghana to the United Kingdom 
    to provide my strongest possible recommendation and unwavering support for the Global Talent 
    Visa application of Deborah Akuoko. I have had the privilege of observing her exceptional 
    dedication, academic excellence, and commitment to making a significant impact in her field 
    of study, and I am deeply impressed by her achievements.
    """
    story.append(Paragraph(intro_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Body paragraph 1 - Effort and dedication
    body1_text = """
    I have been deeply impressed by Deborah Akuoko's unwavering effort and dedication to 
    make a meaningful impact in her field of study. Her commitment to excellence is evident 
    in her academic achievements and research contributions. Through physical interaction and 
    observation, I have realised that Deborah Akuoko is a natural scientist, a fact that 
    is further proven by the evidence of her MPhil degree and her successful pursuit of a PhD, 
    along with her relevant research contributions which are further testified by her PhD 
    advisor. Through these direct interactions and review of her work, I have witnessed 
    firsthand her passion for advancing knowledge and her determination to contribute 
    significantly to her chosen discipline.
    """
    story.append(Paragraph(body1_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Body paragraph 2 - Female achievement and high impact research
    body2_text = """
    What particularly stands out is that Deborah Akuoko has demonstrated exceptional ability 
    to conduct high-impact research, as testified by her PhD advisor. As a female researcher 
    from a developing country, this achievement is especially noteworthy. It is unfortunately 
    not common to see women from developing countries achieving such levels of research excellence 
    and recognition. Deborah Akuoko's success serves as a powerful testament to her exceptional 
    talent, resilience, and determination to overcome barriers that many women in similar 
    circumstances face.
    """
    story.append(Paragraph(body2_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Body paragraph 3 - Role model and impact on other girls
    body3_text = """
    The Ghana High Commission in London strongly and unequivocally supports Deborah Akuoko's 
    visa application. I firmly believe that granting her the opportunity to advance her research 
    in the United Kingdom will go a long way to help girls similar to her, including serving as 
    a powerful role model. Not only will this visa enable her to continue her groundbreaking 
    work, but it will also serve as an inspiration to countless young girls in Ghana and other 
    developing countries who aspire to pursue careers in research and academia. Deborah Akuoko 
    has the potential to become a significant role model, demonstrating that with talent, 
    dedication, and opportunity, women from developing countries can achieve excellence in their 
    chosen fields and make substantial contributions to global knowledge and innovation. Her success 
    story will inspire the next generation of female researchers and scholars.
    """
    story.append(Paragraph(body3_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Body paragraph 4 - Contribution to UK and Ghana
    body4_text = """
    The United Kingdom stands to benefit greatly from Deborah Akuoko's research contributions, 
    while her success will also reflect positively on Ghana's commitment to developing its 
    human capital and supporting women in STEM fields. Her presence in the UK research 
    community will enrich the academic landscape and foster greater diversity and inclusion 
    in research institutions.
    """
    story.append(Paragraph(body4_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    conclusion_text = """
    On behalf of the Ghana High Commission in London, I wholeheartedly and most strongly 
    support Deborah Akuoko's Global Talent Visa application. Her exceptional talent, proven 
    track record of high-impact research as confirmed by her PhD advisor, and potential to 
    inspire future generations of female researchers make her an exemplary candidate for this 
    visa. I am confident that she will make significant contributions to her field and serve 
    as an outstanding representative of both Ghana's academic excellence and the potential of 
    women from developing countries to excel in research and innovation. The Ghana High 
    Commission stands firmly behind this application and believes that Deborah Akuoko 
    represents exactly the kind of exceptional talent that the Global Talent Visa programme 
    is designed to attract.
    """
    story.append(Paragraph(conclusion_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Closing
    story.append(Paragraph("Please do not hesitate to contact me if you require any further information.", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Signature
    story.append(Paragraph("Sincerely,", signature_style))
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("<b>Her Excellency Zita Benson</b>", signature_style))
    story.append(Paragraph("High Commissioner of Ghana to the United Kingdom", signature_style))
    story.append(Paragraph("Ghana High Commission, London", signature_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("London, United Kingdom", signature_style))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Recommendation letter created successfully at: {pdf_path}")

if __name__ == '__main__':
    create_recommendation_letter()


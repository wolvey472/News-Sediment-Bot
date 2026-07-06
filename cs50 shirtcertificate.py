from fpdf import FPDF


name = input("Name: ")

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.add_page()

# Title
pdf.set_font("Helvetica", "B", 48)
pdf.cell(0, 50, "CS50 Shirtificate", align="C")

# Shirt image, centered on A4 page
pdf.image("shirtificate.png", x=10, y=70, w=190)

# Name text on shirt
pdf.set_font("Helvetica", "B", 24)
pdf.set_text_color(255, 255, 255)
pdf.set_y(125)
pdf.cell(0, 10, f"{name} took CS50", align="C")

pdf.output("shirtificate.pdf")
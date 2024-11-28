from io import BytesIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import datetime
import pandas as pd

def generate_pdf_table(dataframe, file_prefix="table"):
    # Generate today's date for the filename
    today = datetime.date.today().strftime("%Y-%m-%d")
    file_name = f"{file_prefix}_{today}.pdf"

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')

    # Create a table from the DataFrame
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(dataframe.columns))))

    # Save the table as an image
    table_image = "table_image.png"
    plt.savefig(table_image, bbox_inches="tight", dpi=300)
    plt.close(fig)  # Close the figure to release memory

    # Generate a PDF with the table image
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Selected Colleges and Cutoffs", ln=True, align="C")
    pdf.image(table_image, x=10, y=30, w=190)

    # Write PDF to an in-memory BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)  # Output the PDF content to the buffer
    pdf_buffer.seek(0)  # Reset buffer pointer to the beginning

    return pdf_buffer, file_name

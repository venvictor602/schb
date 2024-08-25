

# import os
# import io
# from django.conf import settings
# from django.shortcuts import render
# from django.http import HttpResponse
# from .forms import DocumentForm
# from .models import DocumentData
# from PIL import Image
# import fitz  # PyMuPDF
# from docx import Document
# from docx.shared import Inches
# from datetime import date

# def pdf_to_images(pdf_file):
#     images = []
#     pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         pix = page.get_pixmap()
#         img = Image.open(io.BytesIO(pix.tobytes("png")))  # Ensure correct format
#         images.append(img)
#     return images

# def generate_document(data, images):
#     template_path = os.path.join(settings.BASE_DIR, 'document_app', 'templates', 'document_app', 'templates.docx')
#     document = Document(template_path)

#     # Convert all datetime.date fields to strings
#     for key, value in data.items():
#         if isinstance(value, date):
#             data[key] = value.strftime('%d-%m-%Y')  # Adjust the format as needed

#     # Replace placeholders in the document with form data
#     for paragraph in document.paragraphs:
#         for key, value in data.items():
#             placeholder = '{{' + key + '}}'
#             if placeholder in paragraph.text:
#                 paragraph.text = paragraph.text.replace(placeholder, value)

#     # Replace placeholders in tables (if any)
#     for table in document.tables:
#         for row in table.rows:
#             for cell in row.cells:
#                 for key, value in data.items():
#                     placeholder = '{{' + key + '}}'
#                     if placeholder in cell.text:
#                         cell.text = cell.text.replace(placeholder, value)

#     # Insert images into the document
#     for image in images:
#         # Save image to a BytesIO object
#         image_stream = io.BytesIO()
#         image.save(image_stream, format='PNG')  # Ensure format is specified
#         image_stream.seek(0)
        
#         # Add image to the document
#         document.add_paragraph()  # Add an empty paragraph before inserting the image
#         document.add_picture(image_stream, width=Inches(6))  # Adjust size as needed

#     # Save the modified document to a BytesIO object
#     output = io.BytesIO()
#     document.save(output)
#     output.seek(0)
    
#     return output

# def document_view(request):
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             pdf_file = request.FILES.get('pdf_file')
#             if pdf_file:
#                 images = pdf_to_images(pdf_file)
#                 doc_file = generate_document(form.cleaned_data, images)
#                 response = HttpResponse(doc_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#                 response['Content-Disposition'] = f'attachment; filename="{form.cleaned_data["well_name"]}_report.docx"'
#                 return response
#             else:
#                 return HttpResponse("PDF file is required.", status=400)
#     else:
#         form = DocumentForm()

#     return render(request, 'document_form.html', {'form': form})



import os
import io
from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .forms import DocumentForm
from .models import DocumentData
from PIL import Image
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches

def pdf_to_images(pdf_file):
    images = []
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))  # Ensure correct format
        images.append(img)
    return images

def generate_document(data, images1, images2):
    template_path = os.path.join(settings.BASE_DIR, 'document_app', 'templates', 'document_app', 'templates.docx')
    document = Document(template_path)

    # Replace form data placeholders with actual values
    for paragraph in document.paragraphs:
        for key, value in data.items():
            placeholder = '{{' + key + '}}'
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, value)

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items():
                    placeholder = '{{' + key + '}}'
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, value)

    def insert_images_at_placeholder(placeholder, images):
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if placeholder in cell.text:
                        # Clear existing content in the cell
                        for paragraph in cell.paragraphs:
                            p = paragraph._element
                            p.getparent().remove(p)
                        
                        # Insert images into the cell
                        for image in images:
                            image_stream = io.BytesIO()
                            image.save(image_stream, format='PNG')
                            image_stream.seek(0)
                            
                            # Add a new paragraph to the cell and insert the image
                            new_paragraph = cell.add_paragraph()
                            new_paragraph.add_run().add_picture(image_stream, width=Inches(6))  # Adjust size as needed
                        
                        # Stop searching once we have inserted images
                        return

    # Insert images into cells with placeholders
    insert_images_at_placeholder('{{pdf1_images}}', images1)
    insert_images_at_placeholder('{{pdf2_images}}', images2)

    # Save the modified document to a BytesIO object
    output = io.BytesIO()
    document.save(output)
    output.seek(0)

    return output






def document_view(request):
    if request.method == 'POST':
        # Collect all non-media fields from request.POST as a dictionary
        data = request.POST.dict()

        print("Received data:", data)


        # Handle file uploads
        pdf_file1 = request.FILES.get('pdf1_images')
        pdf_file2 = request.FILES.get('pdf_file2')

        # Convert PDFs to images if they exist
        images1 = pdf_to_images(pdf_file1) if pdf_file1 else []
        images2 = pdf_to_images(pdf_file2) if pdf_file2 else []

        # Generate the document with the provided data and images
        doc_file = generate_document(data, images1, images2)

        # Create an HTTP response to return the generated document
        response = HttpResponse(doc_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{data.get("well_name", "document")}_report.docx"'
        
        # Return the response to trigger the download
        return response

    # For GET requests, simply render the HTML form
    return render(request, 'job-1.html')



# def document_view(request):
#     if request.method == 'POST':
#          # Collect all non-media fields from request.POST as a dictionary
#             data = request.POST.dict()
        
#             pdf_file1 = request.FILES.get('pdf_file1')
#             pdf_file2 = request.FILES.get('pdf_file2')

#             images1 = pdf_to_images(pdf_file1) if pdf_file1 else []
#             images2 = pdf_to_images(pdf_file2) if pdf_file2 else []

#             doc_file = generate_document(data, images1, images2)
#             response = HttpResponse(doc_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#             response['Content-Disposition'] = f'attachment; filename="{data.get("well_name", "document")}_report.docx"'
    

#     return render(request, 'job-1.html')


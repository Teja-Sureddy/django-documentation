import fitz
import tempfile
import os
from django.http import JsonResponse


def processing_pdf_view(request):
    """
    Using pymupdf to extract/insert text, images, ... from/to pdf
    """
    if request.method == "GET":
        doc = fitz.open("static/assets/Invoice.pdf")

        # Metadata
        metadata = doc.metadata

        # Extracting Text - extract full text from pdf
        text = chr(12).join([page.get_text() for page in doc])

        # Searching Text - get the positions of text
        search_text = "sku"
        text_positions = {page.number: page.search_for(search_text) for page in doc}

        # Adding Annotations - adding annotations to text_positions
        for page_number, positions in text_positions.items():
            for position in positions:
                pdf_page = doc.load_page(page_number)
                pdf_page.add_highlight_annot(position)

        annot_file_path = get_temp_file_path("Invoice_annotations.pdf")
        doc.save(annot_file_path)

        # PDF Conversion - pdf pages to png
        for page in doc:
            matrix = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=matrix)
            file_path = get_temp_file_path(f"Invoice_page_{page.number}.png")
            pix.save(file_path)

        # Extracting Images - extract images from pdf
        for page in doc:
            images = page.get_images()
            for index, image in enumerate(images):
                img_data = doc.extract_image(image[0])
                file_path = get_temp_file_path(
                    f"Invoice_image_{page.number + index}.{img_data['ext']}"
                )

                with open(file_path, "wb") as file:
                    file.write(img_data["image"])

        # encrypt
        encrypt_file_path = get_temp_file_path("Invoice_encrypted.pdf")
        doc.save(
            encrypt_file_path,
            user_pw="user",
            owner_pw="owner",
            encryption=fitz.PDF_ENCRYPT_AES_256,
        )

        # decrypt
        doc_encrypted = fitz.open(encrypt_file_path)
        if doc_encrypted.is_encrypted:
            doc_encrypted.authenticate("user")  # 0 - Failed, 2 - User, 4 - Owner

        decrypt_file_path = get_temp_file_path("Invoice_decrypt.pdf")
        doc_encrypted.save(decrypt_file_path)

        doc.close()

        return JsonResponse(
            {
                "metadata": metadata,
                "text": text,
                "Message": "Check the Temp directory for files starting with `Invoice`.",
            }
        )


def get_temp_file_path(path):
    temp_directory = tempfile.gettempdir()
    file_path = os.path.join(temp_directory, path)
    return file_path

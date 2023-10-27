import PyPDF2
import fitz


def extract_images_from_pdf(pdf_path):
    images = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]
                image_format = base_image["ext"]
                img_path = f"Output/Image/image_{page_num}_{img_index}.{image_format}"
                with open(img_path, "wb") as f:
                    f.write(image_data)
                images.append(img_path)
    return images


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


# Example usage
pdf_path = "Attachements/Bank-Statement-Template-4-TemplateLab.pdf"

# Extract images
images = extract_images_from_pdf(pdf_path)
print("image saved")

# Extract text
text = extract_text_from_pdf(pdf_path)
file_path = "Output/Text/pdf_text.txt"
with open(file_path, "w") as file:
    file.write(text)
print("text saved")

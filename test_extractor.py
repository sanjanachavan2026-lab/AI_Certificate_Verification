from utils.ocr import extract_text
from utils.extractor import extract_certificate_info


file_path = "uploads/test_certificate.pdf"


print("Reading certificate...")


ocr_text = extract_text(
    file_path
)


print("\n========== OCR TEXT ==========\n")

print(ocr_text)


certificate_info = extract_certificate_info(
    ocr_text
)


print(
    "\n========== EXTRACTED INFORMATION ==========\n"
)


for key, value in certificate_info.items():

    if key != "raw_text":

        print(
            f"{key}: {value}"
        )
from flask import (
    Flask,
    render_template,
    request
)

import os
import sqlite3

from utils.ocr import extract_text

from utils.extractor import (
    extract_certificate_info
)

from utils.verification import (
    verify_certificate
)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_FOLDER = "uploads"

DATABASE_NAME = "database.db"


app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# DATABASE
# =========================================================

def get_all_certificates():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            certificate_id,
            name,
            issuer,
            certificate_type,
            course_or_event,
            issue_date,
            duration,
            status
        FROM certificates
        """
    )


    rows = cursor.fetchall()

    conn.close()


    records = []

    for row in rows:

        records.append(
            dict(row)
        )


    return records


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# VERIFY
# =========================================================

@app.route(
    "/verify",
    methods=["POST"]
)
def verify():

    # -----------------------------------------------------
    # Check file
    # -----------------------------------------------------

    if "certificate" not in request.files:

        return (
            "No certificate uploaded",
            400
        )


    file = request.files[
        "certificate"
    ]


    if file.filename == "":

        return (
            "Please select a certificate",
            400
        )


    # -----------------------------------------------------
    # File extension validation
    # -----------------------------------------------------

    allowed_extensions = {

        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"

    }


    extension = os.path.splitext(
        file.filename
    )[1].lower()


    if extension not in allowed_extensions:

        return (
            "Unsupported file format. "
            "Please upload PDF, JPG, JPEG or PNG.",
            400
        )


    # -----------------------------------------------------
    # Save file
    # -----------------------------------------------------

    file_path = os.path.join(

        app.config[
            "UPLOAD_FOLDER"
        ],

        file.filename

    )


    file.save(file_path)


    # =====================================================
    # STEP 1 — OCR
    # =====================================================

    try:

        extracted_text = extract_text(
            file_path
        )

    except Exception as error:

        return (
            f"OCR processing failed: {error}",
            500
        )


    # =====================================================
    # STEP 2 — INFORMATION EXTRACTION
    # =====================================================

    try:

        certificate_info = (
            extract_certificate_info(
                extracted_text
            )
        )

    except Exception as error:

        return (
            f"Certificate extraction failed: {error}",
            500
        )


    # =====================================================
    # STEP 3 — GET DATABASE RECORDS
    # =====================================================

    database_records = (
        get_all_certificates()
    )


    # =====================================================
    # STEP 4 — VERIFICATION
    # =====================================================

    verification_result = (
        verify_certificate(

            certificate_info,

            database_records

        )
    )


    # =====================================================
    # STEP 5 — RESULT PAGE
    # =====================================================

    return render_template(

        "result.html",

        result=verification_result,

        extracted_text=extracted_text,

        certificate_info=certificate_info

    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
import sqlite3

DATABASE_NAME = "database.db"


def create_database():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            certificate_id TEXT UNIQUE,

            name TEXT NOT NULL,

            issuer TEXT NOT NULL,

            certificate_type TEXT,

            course_or_event TEXT,

            issue_date TEXT,

            duration TEXT,

            status TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


def insert_sample_data():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    certificates = [

        (
            "CERT1001",
            "Rohit Rathod",
            "KIT College",
            "Workshop",
            "AI Workshop",
            "20-08-2026",
            "",
            "Valid"
        ),

        (
            "INT1002",
            "Amit Patil",
            "ABC Technologies Pvt. Ltd.",
            "Internship",
            "Software Development Internship",
            "18-08-2026",
            "June 2026 - August 2026",
            "Valid"
        ),

        (
            "CERT1003",
            "Sneha More",
            "KIT College",
            "Professional Certification",
            "Machine Learning",
            "15-08-2026",
            "",
            "Valid"
        ),

        (
            "CERT1004",
            "Priya Sharma",
            "XYZ Skill Development Institute",
            "Training",
            "Python Programming",
            "12-08-2026",
            "3 Months",
            "Valid"
        ),

        (
            "CERT1005",
            "Rahul Jadhav",
            "Tech Innovation Pvt. Ltd.",
            "Achievement",
            "Artificial Intelligence",
            "10-08-2026",
            "",
            "Valid"
        )

    ]


    for certificate in certificates:

        try:

            cursor.execute("""
                INSERT INTO certificates
                (
                    certificate_id,
                    name,
                    issuer,
                    certificate_type,
                    course_or_event,
                    issue_date,
                    duration,
                    status
                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """, certificate)

        except sqlite3.IntegrityError:

            pass


    conn.commit()

    conn.close()


if __name__ == "__main__":

    create_database()

    insert_sample_data()

    print("Generic certificate database created successfully!")

    print("Sample certificate records inserted successfully!")
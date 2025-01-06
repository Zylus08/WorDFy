import os
import time
from datetime import datetime, timedelta
import schedule
import pythoncom
from flask import Flask, request, render_template, send_from_directory
from docx2pdf import convert
import smtplib
from email.message import EmailMessage
import sqlite3

app = Flask(__name__)

# Define the base directory for the app
BASE_DIR = "E:\\users db"

# Email configuration
EMAIL_ADDRESS = "sakshammishra123@yahoo.com"  # Replace with your email address
EMAIL_PASSWORD = "Jyoti!123"          # Replace with your email password

# Database setup
DB_PATH = os.path.join(BASE_DIR, "users.db")

def init_db():
    os.makedirs(BASE_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            uploaded_file TEXT NOT NULL,
            pdf_file TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()


def safe_convert(docx_path, pdf_path):
    try:
        # Initialize COM library (only once per application lifecycle)
        pythoncom.CoInitialize()

        # Perform conversion
        convert(docx_path, pdf_path)
    finally:
        # Uninitialize COM library
        pythoncom.CoUninitialize()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        email = request.form["email"]
        docx_file = request.files["docx_file"]

        if not email or not docx_file:
            return "Email and file are required!", 400
        else:
            # Save uploaded .docx file
            upload_dir = os.path.join(BASE_DIR, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            docx_path = os.path.join(upload_dir, docx_file.filename)
            pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
            docx_file.save(docx_path)
            print("DEBUG: DOCX file saved at", docx_path)

            try:
                # Convert the .docx to PDF
                safe_convert(docx_path, pdf_path)
                print("DEBUG: PDF file created at", pdf_path)

                # Store user info in the database 
                save_user_to_db(email, docx_file.filename, os.path.basename(pdf_path)) 

                # Provide download link 
                download_link = f'<a href="/download/{os.path.basename(pdf_path)}">Click here to download your PDF.</a>'
                result = f"PDF has been created successfully! {download_link}"

                # Send the PDF via email
                send_email_with_attachment(email, pdf_path)

                result = f"PDF has been sent to {email} successfully! {download_link}"
                print("DEBUG: Success message with link:", result)
            except Exception as e:
                error = f"An error occurred: {e}" 
                print("DEBUG: Error message:", error)
    return render_template("index.html", result=result, error=error)

@app.route("/download/<filename>") 
def download_file(filename): 
    try: 
        print("DEBUG: Download requested for", filename) # Debugging statement 
        return send_from_directory("uploads", filename) 
    except Exception as e: 
        return str(e), 404

def send_email_with_attachment(to_email, file_path):
    msg = EmailMessage()
    msg["Subject"] = "Your Converted PDF File"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content("Please find the attached PDF file.")

    # Attach the PDF
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    print("DEBUG: Email message created")

    # Send the email
    try:
        with smtplib.SMTP("smtp.mail.yahoo.com", 587) as smtp: 
            smtp.ehlo() # Can be omitted 
            smtp.starttls() # Secure the connection 
            smtp.ehlo() # Can be omitted 
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def save_user_to_db(email, docx_file, pdf_file):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (email, uploaded_file, pdf_file)
        VALUES (?, ?, ?)
        """, (email, docx_file, pdf_file))
        conn.commit()

def cleanup_uploads(days=7): 
    now = datetime.now() 
    cutoff = now - timedelta(days=days) 
    
    upload_dir = "uploads" 
    for filename in os.listdir(upload_dir): 
        file_path = os.path.join(upload_dir, filename) 
        if os.path.isfile(file_path): 
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path)) 
            if file_mtime < cutoff: os.remove(file_path) 
            print(f"Removed old file: {file_path}")

if __name__ == "__main__":
    init_db()  # Initialize the database

    # Start the scheduled tasks in a separate thread 
    import threading 
    def run_scheduled_tasks(): 
        while True: 
            schedule.run_pending() 
            time.sleep(1) 
            
    threading.Thread(target=run_scheduled_tasks, daemon=True).start()

    app.run(debug=True)

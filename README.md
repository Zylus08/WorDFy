# WorDFy
 
WorDFy is a web application that allows users to upload DOCX files, convert them to PDF format, and receive the converted files via email or direct download. This project is built using Flask, and it integrates email functionality for sending the converted PDF files.

Features:
DOCX to PDF Conversion: Users can upload DOCX files and convert them to PDF.

Direct Download: Provides a link for users to download the converted PDF directly from the website.

Email Delivery: Optionally, users can receive the converted PDF file via email.

Scheduled Cleanup: Automatically removes old files from the server to save disk space.

User Data Storage: Stores user information and file details in a SQLite database.

Technologies Used:
Python

Flask

docx2pdf

smtplib

SQLite

HTML/CSS

schedule (for task scheduling)

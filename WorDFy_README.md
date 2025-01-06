# WorDFy - DOCX to PDF Converter

WorDFy is a web application that allows users to upload DOCX files, convert them to PDF format, and receive the converted files via email or direct download. This project is built using Flask and integrates email functionality for sending the converted PDF files.

---

## Features

- **DOCX to PDF Conversion**: Users can upload DOCX files and convert them to PDF.
- **Direct Download**: Provides a link for users to download the converted PDF directly from the website.
- **Email Delivery**: Optionally, users can receive the converted PDF file via email.
- **Scheduled Cleanup**: Automatically removes old files from the server to save disk space.
- **User Data Storage**: Stores user information and file details in a SQLite database.

---

## Technologies Used

- **Python**
- **Flask**
- **docx2pdf**
- **smtplib**
- **SQLite**
- **HTML/CSS**
- **schedule** (for task scheduling)

---

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/your-username/wordfy.git
cd wordfy
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Database Initialization
```bash
python -c "from app import init_db; init_db()"
```

### Run the Application
```bash
python app.py
```

### Access the Web Application
Open your browser and go to [http://localhost:5000](http://localhost:5000).

---

## Usage

1. Upload a DOCX file, enter your email address, and click **"Convert and Send."**
2. Download the converted PDF file using the provided link or check your email for the PDF attachment.

---

## Configuration

1. Update the `EMAIL_ADDRESS` and `EMAIL_PASSWORD` variables in `app.py` with your email credentials.
2. Customize the scheduled cleanup interval in `app.py` if needed.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -am 'Add new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Create a new Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

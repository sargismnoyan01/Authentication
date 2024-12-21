# Authentication System with Password and QR Code

## Overview
This repository provides an authentication system where users can log in using either their email and password or by scanning a QR code. The system ensures rapid and secure authentication through a streamlined process.

### Key Features
- **Dual Authentication Modes:**
  - Email and password authentication.
  - QR code scanning for seamless login.
- **Secure Communication:**
  - Secure email delivery for QR codes.
  - Secure backend implementation.
- **Fast and User-Friendly:**
  - A quick login experience with real-time QR scanning.

---

## Workflow

1. **Login Page:**
   - The user accesses the login page.
   - They can choose between two options:
     1. Entering their email and password.
     2. Clicking the "QR Scanning" button.

2. **QR Scanning:**
   - Upon clicking the "QR Scanning" button:
     - A new page opens where the user inputs their email.
     - The system sends a unique QR code to the provided email.
     - Simultaneously, the system activates the camera on the user's device.

3. **QR Code Validation:**
   - The user scans the received QR code using their device camera.
   - If the scanned QR matches the generated one, the user is automatically logged in.

---

## Technologies Used

- **Frontend:**
  - HTML, CSS, JavaScript
- **Backend:**
  - Django
- **Other:**
  - QR code generation and scanning libraries
  - Email handling via Gmail API or SMTP

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sargismnoyan01/Authentication.git/
   cd Authentication
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install dependencies:
   ```bash
   enter your gmail infos in settings.py
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

---


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## Contact

For questions or support, please reach out to [mnoyansargis@gmail.com](mnoyansargis@gmail.com).


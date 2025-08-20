#content://com.android.externalstorage.documents/tree/primary%3AACODE%20samsung%20phone%2FACODE::primary:ACODE samsung phone/ACODE/Acode-Chat-Backend/API/GENERAL/send_verification_email.pyimport random
import random
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


content1 = """
Hi [Recipient Name],

We’re excited to see you taking steps to secure your account with us! To proceed, please use the One-Time Password (OTP) below:


🎟 Your OTP Code: [OTP CODE]

⏳ Expires in 10 minutes.


For your security:

This OTP is unique to you.

Don’t share this code with anyone—our team will never ask for it.


If this wasn't you or you didn’t request an OTP, please let us know immediately. We’ve got your back!

Thanks for being part of the Mesaanger -Ax community! 💼

Stay safe,
Messanger - Ax

---

"""


# Function to send anonymous email with random device and location
def send_email(to_email, subject, body):
    result = {"status": False, "status_code": None, "message": ""}
    EMAIL = "hackesofice1@gmail.com"
    APP_PASSWORD = "wkykvotccroxxgdh"
    try:
        # --- Build Email ---
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # --- Connect to Gmail SMTP ---
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL, APP_PASSWORD)

        # --- Try Sending ---
        refused = server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        if refused:  # Gmail rejected recipient immediately
            result["status"] = False
            result["status_code"] = 400
            result["message"] = f"Recipient refused: {refused}"
        else:
            result["status"] = True
            result["status_code"] = 200
            result["message"] = "Email accepted by Gmail (delivery not guaranteed)"

    # --- Error Handling Section ---
    except smtplib.SMTPAuthenticationError as e:
        result["status"] = False
        result["status_code"] = e.smtp_code
        result["message"] = f"Authentication failed: {e.smtp_error.decode()}"
    except smtplib.SMTPRecipientsRefused as e:
        result["status"] = False
        result["status_code"] = 400
        result["message"] = f"All recipients were refused: {e.recipients}"
    except smtplib.SMTPSenderRefused as e:
        result["status"] = False
        result["status_code"] = 400
       # result["status_code"] = e.smtp_code
        result["message"] = f"Sender address refused: {e.smtp_error.decode()}"
    except smtplib.SMTPDataError as e:
        result["status"] = False
        result["status_code"] = 429
        # result["status_code"] = e.smtp_code
        result["message"] = f"SMTP data error: {e.smtp_error.decode()}"
    except smtplib.SMTPConnectError as e:
        result["status"] = False
        # result["status_code"] = e.smtp_code
        result["status_code"] = 429
        result["message"] = f"Connection error: {e.smtp_error.decode()}"
    except smtplib.SMTPHeloError as e:
        result["status"] = False
        result["status_code"] = 429
        # result["status_code"] = e.smtp_code
        result["message"] = f"Server did not reply properly to HELO: {e.smtp_error.decode()}"
    except smtplib.SMTPNotSupportedError as e:
        result["status"] = False
        result["status_code"] = 400
        result["message"] = f"SMTP feature not supported: {str(e)}"
    except smtplib.SMTPException as e:
        result["status"] = False
        result["status_code"] = 400
        result["message"] = f"General SMTP error: {str(e)}"
    except Exception as e:
        result["status"] = False
        result["status_code"] = 400
        result["message"] = f"Unexpected error: {str(e)}"

    return result


def sendOTP(to_email, otp_to_send, first_name, mode):
    print(otp_to_send)
    print(type(otp_to_send))
    if mode == 'otpForNewAcc':
        content = content1
        content = content.replace('[OTP CODE]', str(otp_to_send))
        content = content.replace('[Recipient Name]', first_name)
        subject = 'Verify Your messanger - AX Account'
        return send_email(to_email, subject, content)
    # elif mode == 'otpForResetPwd':
    #     content = content1
    #     content = content.replace('[OTP CODE]', otp_to_send)
    #     content = content.replace('[Recipient Name]', first_name)
    #     subject = 'Reset Your Connectify Password'
    #     send_anonymous_email(to_email, subject, content)
        
        
        

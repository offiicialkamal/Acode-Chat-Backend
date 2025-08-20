#content://com.android.externalstorage.documents/tree/primary%3AACODE%20samsung%20phone%2FACODE::primary:ACODE samsung phone/ACODE/Acode-Chat-Backend/API/GENERAL/send_verification_email.pyimport random
import requests
import random
import time

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


# Function to generate a random IP address
def generate_random_ip():
    return '.'.join(str(random.randint(1, 255)) for _ in range(4))

# Function to generate a random user agent
def generate_random_user_agent():
    os_choices = [
        # Windows
        lambda: f"Windows NT {random.choice(['10.0; Win64; x64', '6.1; WOW64', '11.0; Win64; x64'])}",
        # Mac
        lambda: f"Macintosh; Intel Mac OS X {random.randint(10, 13)}_{random.randint(0, 9)}_{random.randint(0, 9)}",
        # Linux
        lambda: f"X11; Linux {random.choice(['x86_64', 'i686', 'armv7l'])}",
        # Android
        lambda: f"Linux; Android {random.randint(7, 14)}; {random.choice(['Pixel', 'Samsung Galaxy', 'OnePlus', 'Xiaomi'])}{random.randint(1,9)}",
        # iOS
        lambda: f"iPhone; CPU iPhone OS {random.randint(12, 17)}_{random.randint(0,9)} like Mac OS X"
    ]

    browser_choices = [
        # Chrome
        lambda: f"Chrome/{random.randint(80, 124)}.0.{random.randint(1000, 9999)}.{random.randint(10, 999)}",
        # Firefox
        lambda: f"Firefox/{random.randint(80, 124)}.0",
        # Safari (WebKit-based)
        lambda: f"Version/{random.randint(10, 17)}.0 Safari/{random.randint(500, 999)}.{random.randint(1,9)}"
    ]

    os_part = random.choice(os_choices)()
    browser_part = random.choice(browser_choices)()
    
    # Add dynamic AppleWebKit version for realism
    webkit_version = f"AppleWebKit/{random.randint(500, 605)}.{random.randint(1,50)}"

    # Timestamp-based seed to ensure uniqueness across runs
    unique_build = str(int(time.time() * 1000))[-6:]

    return f"Mozilla/5.0 ({os_part}) {webkit_version} (KHTML, like Gecko) {browser_part}.{unique_build}"

# Function to send anonymous email with random device and location
def send_anonymous_email(to_email, subject, message):
    url = "https://api.proxynova.com/v1/send_email"  # Correct endpoint
    from_email = "hackesofice@gamil.com"
    random_user_agent = generate_random_user_agent()
    random_ip = generate_random_ip()
    
    headers = {                                                                                                                                                 
        'User-Agent': random_user_agent,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.proxynova.com',
        'Referer': 'https://www.proxynova.com/',
        'X-Forwarded-For': random_ip,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    data = {
        'to': to_email,
        'from': from_email,
        'subject': subject,
        'message': message
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        return response
    except Exception as e:
        print(e)
    
    # if response.status_code == 200:
    #     print(f"Email sent successfully from IP: {random_ip} using device: {random_user_agent}")
    # elif response.status_code == 429:
    #     print(f"Rate limit hit! Waiting before retrying... Status code: {response.status_code}")
    #     return "Rate limit hit!", response
    # else:
    #     print(f"Failed to send email. Status code: {response.status_code}")
    #     return "Failed to send email", response

def sendOTP(to_email, otp_to_send, first_name, mode):
    print(otp_to_send)
    print(type(otp_to_send))
    if mode == 'otpForNewAcc':
        content = content1
        content = content.replace('[OTP CODE]', str(otp_to_send))
        content = content.replace('[Recipient Name]', first_name)
        subject = 'Verify Your messanger - AX Account'
        return send_anonymous_email(to_email, subject, content)
    # elif mode == 'otpForResetPwd':
    #     content = content1
    #     content = content.replace('[OTP CODE]', otp_to_send)
    #     content = content.replace('[Recipient Name]', first_name)
    #     subject = 'Reset Your Connectify Password'
    #     send_anonymous_email(to_email, subject, content)
        
        
        

import smtplib
from email.message import EmailMessage

def to_sms(to_email, message_text):
    msg = EmailMessage()
    msg.set_content(message_text)
    msg['Subject'] = 'StepTest.uz'
    msg['From'] = 'uzbekflow3@gmail.com'  
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('uzbekflow3@gmail.com', 'djuttsaaakjgauzr')  
            smtp.send_message(msg)
            print("Xabar muvaffaqiyatli yuborildi!")
    except Exception as e:
        print("Email yuborishda xatolik:", e)

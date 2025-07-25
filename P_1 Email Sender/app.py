import gradio as gr
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load credentials from safe.env
load_dotenv("safe.env")

# Sender  credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD= os.getenv("EMAIL_PASSWORD")

# Email sending function
def send_email(to_email, subject, message,attachment):
    try:
        msg= EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To']= to_email
        msg.set_content(message)

        # if a FILE is attached
        if attachment is not None:
            filename= os.path.basename(attachment)  # getting just the file name
            with open(attachment, "rb") as f:
                file_data= f.read()
            msg.add_attachment(file_data, maintype= "application", subtype= "octet-stream", filename= filename)
            

        with smtplib.SMTP('smtp.gmail.com',587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return "✅ Email sent successfully!! with attachment" if attachment else " ✅ Email sent successfully?"
    except Exception as e:
        return f"❌ Failed to send email: {e}"
    
# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📧 Email Sender WEBApp")

    with gr.Row():
        to_input= gr.Textbox(label= "Recipient Email",placeholder="e.g. someone@exa.com")
        subject_input= gr.Textbox(label="Subject",placeholder= "Enter the subject")

    message_input= gr.Textbox(label="Message", lines=5, placeholder= "What you wanna inform!!??")

    attachment_input= gr.File(
        label="Attachment (Optional)",
        file_types=[".pdf", ".jpg", ".png", ".txt", ".docx", ".xlsx", ".csv"]
    )

    send_btn= gr.Button("Send Email?")
    output= gr.Textbox(label="Status")

    send_btn.click(
        fn=send_email,
        inputs=[to_input, subject_input, message_input,attachment_input],
        outputs=output
    )
demo.launch()


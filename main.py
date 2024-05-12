import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

api_key = os.environ.get('API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class SubscriptionRequest(BaseModel):
    email: str

class GetInTouchRequest(BaseModel):
    name:str
    email:str
    message:str

@app.get("/")
def read_root():
    return {"Hello":api_key}

@app.post('/subscribe')
async def subscribe(subscription_request: SubscriptionRequest):
    email = subscription_request.email

    subject = "Welcome to Alansa Updates!"
    from_email = "info@alansatech.com"
    to_email = email
    body = '''
<body>
    <p>Dear Valued Subscriber,</p>

    <p>Welcome to Alansa Updates!</p>

    <p>Thank you for subscribing to our newsletter. Get ready to stay in the loop with the latest news, innovations, and projects straight from Alansa.</p>

    <p>We'll be sharing exciting updates soon, so keep an eye on your inbox!</p>

    <p>Best regards,</p>

    <p>Solomon<br>
    CEO<br>
    Alansa</p>
</body>
'''

    send_email(subject=subject,body=body,from_email=from_email,to_email=to_email)

@app.post('/contactus')
async def contactus(request: GetInTouchRequest):
    name = request.name
    email = request.email
    message = request.message
    subject = "New Inquiry Received: Action Required"
    from_email = "info@alansatech.com"
    to_email = "info@alansatech.com"
    body = f'''
        <body>
    <p>Dear Alansa Team,</p>

    <p>We've received a new inquiry from a potential client. Here are the details:</p>

    <ul>
        <li><strong>Name:</strong> {name}</li>
        <li><strong>Email:</strong> {email}</li>
        <li><strong>Message:</strong> {message}</li>
    </ul>

    <p>Please review the inquiry and take appropriate action.</p>

    <p>Best regards,</p>

    <p>Solomon<br>
    CEO<br>
    Alansa</p>
</body>
'''
    
    send_email(subject=subject,body=body,from_email=from_email,to_email=to_email)



def send_email(subject, body, from_email, to_email):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=body)

    try:
        sg = SendGridAPIClient('api_key')
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
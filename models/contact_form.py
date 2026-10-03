from dataclasses import dataclass


@dataclass
class ContactForm:
    name: str = "Alex"
    email: str = "alex2@gmail.com"
    subject: str = "Problems"
    message: str = "Hello,testing contact page"


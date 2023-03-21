from rich.console import Console 
from redmail import gmail
from pathlib import Path
import os
import dotenv

dotenv.load_dotenv()

def send(sender:str, password:str, receiver:str, attachment, subject="Title", body="Body"):
    """
    Sends an email through Gmail

    PARAMS:
    -------
        * sender 
        * attachment
        * subject 
        * body
    """
    gmail.username = sender
    gmail.password = os.environ["app_password"]
    gmail.send(
        subject=subject,
        receivers=[receiver],
        text=body,
        attachments={subject: Path(attachment)}
    )

    Console().print("[bold green]Email sent![/bold green]")

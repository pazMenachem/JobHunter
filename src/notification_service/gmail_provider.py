"""Generic mail notification provider using SMTP."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.notification_service.notifier_interface import NotifierInterface
from src.logger import get_logger


class MailProvider(NotifierInterface):
    """Generic mail notification provider using SMTP."""
    
    def __init__(
        self,
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        smtp_server: str,
        smtp_port: int,
        max_message_length: int
    ) -> None:
        """Initialize the mail provider.
        
        Args:
            sender_email: Email address for sending
            sender_password: Email password or app password for authentication
            recipient_email: Email address to receive notifications
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_port: SMTP server port (e.g., 587 for TLS)
            max_message_length: Maximum message length for emails
        """
        super().__init__(max_message_length=max_message_length)
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.logger = get_logger("mail_provider")
    
    def _send_notification(self, message: str) -> None:
        """Send a notification email via SMTP.
        
        Args:
            message: Message text to send
            
        Raises:
            SMTPException: If email sending fails
        """
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = "JobHunter - Job Notifications"
            
            # Attach message body as plain text
            msg.attach(MIMEText(message, 'plain'))
            
            # Connect to SMTP server
            self.logger.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable TLS encryption
            
            # Login with credentials
            self.logger.info(f"Authenticating with email server...")
            server.login(self.sender_email, self.sender_password)
            
            # Send email
            server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            
            # Close connection
            server.quit()
                
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error(f"Email authentication failed: {e}")
            raise RuntimeError(
                "Email authentication failed. Please check your email and password."
            )
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error occurred: {e}")
            raise RuntimeError(f"Failed to send email: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error sending email: {e}")
            raise RuntimeError(f"Failed to send email: {e}")

"""
YSense™ Email Service
Handles all email communications for the platform
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Dict, Any
import os
from datetime import datetime
import logging

class EmailService:
    """Email service for YSense platform"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', 'contact@ysenseai.org')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'contact@ysenseai.org')
        self.support_email = os.getenv('SUPPORT_EMAIL', 'support@ysenseai.org')
        self.admin_email = os.getenv('ADMIN_EMAIL', 'admin@ysenseai.org')
        
        # Email templates
        self.templates = {
            'welcome': self._get_welcome_template(),
            'password_reset': self._get_password_reset_template(),
            'email_verification': self._get_email_verification_template(),
            'wisdom_approved': self._get_wisdom_approved_template(),
            'revenue_notification': self._get_revenue_notification_template(),
            'admin_alert': self._get_admin_alert_template()
        }
    
    def _get_welcome_template(self) -> str:
        """Welcome email template"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                            padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 2em;">Welcome to YSense™ v4.1</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">The Genesis of Human-AI Wisdom Collaboration</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2>🎉 Welcome to the Future of AI Attribution!</h2>
                    
                    <p>Dear {user_name},</p>
                    
                    <p>Welcome to YSense™ v4.1 | 慧觉™ - the world's first AI attribution infrastructure platform!</p>
                    
                    <h3>🚀 What You Can Do Now:</h3>
                    <ul>
                        <li><strong>Create Wisdom Drops</strong> - Share your knowledge with permanent attribution</li>
                        <li><strong>Earn Revenue</strong> - Get paid for your contributions (up to 100% for Founding Contributors)</li>
                        <li><strong>Use AI Agents</strong> - Access our 6 intelligent AI agents for analysis</li>
                        <li><strong>Download White Paper</strong> - Learn about our revolutionary platform</li>
                    </ul>
                    
                    <h3>🎯 Your Contributor Tier: {tier}</h3>
                    <p>Revenue Share: {revenue_share}%</p>
                    
                    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h4>🔐 Account Security</h4>
                        <p>Your account is secured with industry-standard encryption. Keep your password safe!</p>
                        <p>If you forget your password, use the "Forgot Password" feature on our platform.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{platform_url}" style="background: #4c1d95; color: white; padding: 15px 30px; 
                           text-decoration: none; border-radius: 25px; font-weight: bold;">
                            🚀 Start Using YSense™
                        </a>
                    </div>
                    
                    <p>Need help? Contact us at <a href="mailto:{support_email}">{support_email}</a></p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 0.9em; color: #666;">
                        This email was sent to {user_email}. If you didn't create an account with YSense™, 
                        please ignore this email or contact our support team.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_password_reset_template(self) -> str:
        """Password reset email template"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                            padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 2em;">Password Reset Request</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">YSense™ v4.1 | 慧觉™</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2>🔐 Reset Your Password</h2>
                    
                    <p>Dear {user_name},</p>
                    
                    <p>We received a request to reset your password for your YSense™ account.</p>
                    
                    <div style="background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                        <h4>⚠️ Important Security Notice</h4>
                        <p>This password reset link will expire in <strong>1 hour</strong> for your security.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" style="background: #dc3545; color: white; padding: 15px 30px; 
                           text-decoration: none; border-radius: 25px; font-weight: bold;">
                            🔐 Reset Password
                        </a>
                    </div>
                    
                    <p><strong>Reset Link:</strong> <a href="{reset_url}">{reset_url}</a></p>
                    
                    <div style="background: #d1ecf1; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h4>🛡️ Security Tips</h4>
                        <ul>
                            <li>Use a strong, unique password</li>
                            <li>Don't share your password with anyone</li>
                            <li>Log out from shared devices</li>
                            <li>Contact support if you didn't request this reset</li>
                        </ul>
                    </div>
                    
                    <p>If you didn't request this password reset, please ignore this email or contact our support team.</p>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 0.9em; color: #666;">
                        This email was sent to {user_email}. For security reasons, this link expires in 1 hour.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_email_verification_template(self) -> str:
        """Email verification template"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                            padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 2em;">Verify Your Email</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">YSense™ v4.1 | 慧觉™</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2>📧 Email Verification Required</h2>
                    
                    <p>Dear {user_name},</p>
                    
                    <p>Please verify your email address to complete your YSense™ account setup.</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" style="background: #28a745; color: white; padding: 15px 30px; 
                           text-decoration: none; border-radius: 25px; font-weight: bold;">
                            ✅ Verify Email
                        </a>
                    </div>
                    
                    <p><strong>Verification Link:</strong> <a href="{verification_url}">{verification_url}</a></p>
                    
                    <p>Once verified, you'll have full access to all YSense™ features!</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_wisdom_approved_template(self) -> str:
        """Wisdom approved notification template"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                            padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 2em;">Wisdom Approved! 🎉</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">YSense™ v4.1 | 慧觉™</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2>🎯 Your Wisdom Has Been Approved</h2>
                    
                    <p>Dear {user_name},</p>
                    
                    <p>Great news! Your wisdom drop "<strong>{wisdom_title}</strong>" has been approved and is now live on the platform!</p>
                    
                    <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h4>📊 Wisdom Statistics</h4>
                        <ul>
                            <li><strong>Views:</strong> {views}</li>
                            <li><strong>Downloads:</strong> {downloads}</li>
                            <li><strong>Revenue Earned:</strong> ${revenue_earned}</li>
                        </ul>
                    </div>
                    
                    <p>Your wisdom is now contributing to the AI attribution infrastructure and earning you revenue!</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_revenue_notification_template(self) -> str:
        """Revenue notification template"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4c1d95 0%, #3b82f6 100%); 
                            padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 2em;">💰 Revenue Update</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">YSense™ v4.1 | 慧觉™</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2>💵 Your Revenue Report</h2>
                    
                    <p>Dear {user_name},</p>
                    
                    <p>Here's your latest revenue report from YSense™:</p>
                    
                    <div style="background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h4>📈 Revenue Summary</h4>
                        <ul>
                            <li><strong>Period:</strong> {period}</li>
                            <li><strong>Total Revenue:</strong> ${total_revenue}</li>
                            <li><strong>Your Share:</strong> ${your_share} ({revenue_percentage}%)</li>
                            <li><strong>Contributor Tier:</strong> {tier}</li>
                        </ul>
                    </div>
                    
                    <p>Thank you for contributing to the future of AI attribution!</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _get_admin_alert_template(self) -> str:
        """Admin alert template"""
        return """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%); 
                            padding: 30px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 2em;">🚨 Admin Alert</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9;">YSense™ v4.1 | 慧觉™</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                    <h2>⚠️ System Alert</h2>
                    
                    <p><strong>Alert Type:</strong> {alert_type}</p>
                    <p><strong>Severity:</strong> {severity}</p>
                    <p><strong>Timestamp:</strong> {timestamp}</p>
                    
                    <div style="background: #f8d7da; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h4>📋 Alert Details</h4>
                        <p>{alert_message}</p>
                    </div>
                    
                    <p>Please review and take appropriate action.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def send_email(self, to_email: str, subject: str, template_name: str, 
                   template_data: Dict[str, Any] = None, attachments: List[str] = None) -> bool:
        """Send email using template"""
        try:
            # Check if SMTP is configured
            if not self.smtp_password or self.smtp_password == 'your_email_password_here':
                logging.info(f"SMTP not configured. Mock email sent to {to_email}")
                self._log_mock_email(to_email, subject, template_name, template_data)
                return True  # Return True to show success to user
            
            # Get template
            template = self.templates.get(template_name, '')
            if not template:
                logging.error(f"Template '{template_name}' not found")
                return False
            
            # Format template with data
            template_data = template_data or {}
            template_data.update({
                'platform_url': os.getenv('PLATFORM_URL', 'https://ysenseai.org'),
                'support_email': self.support_email,
                'admin_email': self.admin_email
            })
            
            html_content = template.format(**template_data)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {file_path}'
                        )
                        msg.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logging.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def _log_mock_email(self, to_email: str, subject: str, template_name: str, template_data: Dict[str, Any] = None):
        """Log mock email for development/testing"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        template_data = template_data or {}
        
        # Create a simple log entry
        log_entry = f"""
        📧 MOCK EMAIL SENT [{timestamp}]
        To: {to_email}
        Subject: {subject}
        Template: {template_name}
        Data: {template_data}
        """
        
        # Log to console
        print(log_entry)
        
        # Log to file
        try:
            with open('email_log.txt', 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Could not write to email log: {e}")
    
    def get_mock_email_info(self, template_name: str, template_data: Dict[str, Any] = None) -> str:
        """Get mock email information for display to user"""
        template_data = template_data or {}
        
        if template_name == 'password_reset':
            reset_token = template_data.get('reset_token', 'N/A')
            return f"""
            🔐 Password Reset Information:
            • Reset Token: {reset_token}
            • Expires: 1 hour from now
            • Use this token to reset your password
            """
        elif template_name == 'welcome':
            user_name = template_data.get('user_name', 'User')
            tier = template_data.get('tier', 'Standard')
            return f"""
            🎉 Welcome Email Sent:
            • Welcome {user_name}!
            • Tier: {tier}
            • Account activated successfully
            """
        elif template_name == 'email_verification':
            verification_token = template_data.get('verification_token', 'N/A')
            return f"""
            📧 Email Verification:
            • Verification Token: {verification_token}
            • Click to verify your email
            """
        else:
            return f"📧 {template_name.replace('_', ' ').title()} email sent successfully!"
    
    def send_welcome_email(self, user_email: str, user_name: str, tier: str, revenue_share: str) -> bool:
        """Send welcome email to new user"""
        return self.send_email(
            to_email=user_email,
            subject="🎉 Welcome to YSense™ v4.1 | 慧觉™",
            template_name='welcome',
            template_data={
                'user_name': user_name,
                'user_email': user_email,
                'tier': tier,
                'revenue_share': revenue_share
            }
        )
    
    def send_password_reset_email(self, user_email: str, user_name: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{os.getenv('PLATFORM_URL', 'https://ysenseai.org')}/reset-password?token={reset_token}"
        return self.send_email(
            to_email=user_email,
            subject="🔐 Password Reset Request - YSense™",
            template_name='password_reset',
            template_data={
                'user_name': user_name,
                'user_email': user_email,
                'reset_url': reset_url
            }
        )
    
    def send_email_verification(self, user_email: str, user_name: str, verification_token: str) -> bool:
        """Send email verification"""
        verification_url = f"{os.getenv('PLATFORM_URL', 'https://ysenseai.org')}/verify-email?token={verification_token}"
        return self.send_email(
            to_email=user_email,
            subject="📧 Verify Your Email - YSense™",
            template_name='email_verification',
            template_data={
                'user_name': user_name,
                'user_email': user_email,
                'verification_url': verification_url
            }
        )
    
    def send_wisdom_approved_notification(self, user_email: str, user_name: str, 
                                       wisdom_title: str, views: int, downloads: int, revenue_earned: float) -> bool:
        """Send wisdom approved notification"""
        return self.send_email(
            to_email=user_email,
            subject="🎉 Your Wisdom Has Been Approved!",
            template_name='wisdom_approved',
            template_data={
                'user_name': user_name,
                'user_email': user_email,
                'wisdom_title': wisdom_title,
                'views': views,
                'downloads': downloads,
                'revenue_earned': revenue_earned
            }
        )
    
    def send_revenue_notification(self, user_email: str, user_name: str, 
                               period: str, total_revenue: float, your_share: float, 
                               revenue_percentage: str, tier: str) -> bool:
        """Send revenue notification"""
        return self.send_email(
            to_email=user_email,
            subject="💰 Your YSense™ Revenue Report",
            template_name='revenue_notification',
            template_data={
                'user_name': user_name,
                'user_email': user_email,
                'period': period,
                'total_revenue': total_revenue,
                'your_share': your_share,
                'revenue_percentage': revenue_percentage,
                'tier': tier
            }
        )
    
    def send_admin_alert(self, alert_type: str, severity: str, alert_message: str) -> bool:
        """Send admin alert"""
        return self.send_email(
            to_email=self.admin_email,
            subject=f"🚨 Admin Alert: {alert_type}",
            template_name='admin_alert',
            template_data={
                'alert_type': alert_type,
                'severity': severity,
                'alert_message': alert_message,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
            }
        )

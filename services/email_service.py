import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self):
        # ---------------------------------------------------------------------
        # CONFIGURACIÓN SMTP
        # ---------------------------------------------------------------------
        # IMPORTANTE: Para que funcione, debes colocar tus credenciales reales.
        # Si usas Gmail, es recomendable usar una "Contraseña de Aplicación".
        # Guía: https://support.google.com/accounts/answer/185833
        # ---------------------------------------------------------------------
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "egeafran02@gmail.com"      # <--- COLOCA TU EMAIL AQUÍ
        self.sender_password = "dkzv jlqd pehg slkl"    # <--- COLOCA TU CONTRASEÑA DE APLICACIÓN AQUÍ

    def enviar_correo(self, destinatario, asunto, cuerpo):
        """
        Envía un correo electrónico real usando SMTP.
        """
        # Validación básica de credenciales
        if "tu_email" in self.sender_email or "tu_contraseña" in self.sender_password:
            print("ERROR CRÍTICO: Credenciales SMTP no configuradas en services/email_service.py")
            print("Por favor, edita el archivo y agrega tu email y contraseña de aplicación.")
            return False

        try:
            # Configurar el mensaje
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = destinatario
            msg['Subject'] = asunto

            msg.attach(MIMEText(cuerpo, 'plain'))

            # Conectar al servidor
            print(f"Conectando a {self.smtp_server}...")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls() # Encriptación TLS
            
            # Login
            server.login(self.sender_email, self.sender_password)
            
            # Enviar
            text = msg.as_string()
            server.sendmail(self.sender_email, destinatario, text)
            
            # Cerrar conexión
            server.quit()
            
            print(f"Email enviado correctamente a {destinatario}")
            return True

        except Exception as e:
            print(f"Error enviando email a {destinatario}: {str(e)}")
            return False

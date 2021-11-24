import os

class Config:
	SECRET_KEY = '20NEyZpyUUABF3g8lKQW7HyrhKvi1hNvNKDv0SA2etU' #os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT =  587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL')
	MAIL_PASSWORD = os.environ.get('EMAIL_PW')

	#UPLOAD_FOLDER = 'static/uploads/'
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
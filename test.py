from flask import Flask
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
email = 'test'
token = serializer.dumps(email)
print(token)
# eyJpZCI6NSwibmFtZSI6Iml0c2Rhbmdlcm91cyJ9.6YP6T0BaO67XP--9UzTrmurXSmg

data = serializer.loads(token, max_age=120)
print(data)
# itsdangerous

if __name__ == '__main__':
    app.run()
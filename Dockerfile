FROM python:3.10

# ติดตั้ง Dependencies ของระบบที่จำเป็น
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

WORKDIR /app
COPY . /app/

# อัปเกรด pip และติดตั้ง dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]

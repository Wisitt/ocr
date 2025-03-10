FROM python:3.10

# ติดตั้ง System dependencies ที่จำเป็น
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

# ตั้งค่า work directory
WORKDIR /app
COPY . /app/

# ติดตั้ง Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# รัน Flask API
CMD ["python", "app.py"]

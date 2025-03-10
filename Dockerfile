# ใช้ Python 3.10 เป็น Base Image
FROM python:3.10

# ติดตั้ง Dependency ที่จำเป็นสำหรับ EasyOCR และ OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# คัดลอกไฟล์ทั้งหมดไปที่ `/app`
COPY . /app/

# อัปเกรด pip และติดตั้ง dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# กำหนดคำสั่งเริ่มต้นให้รัน Flask
CMD ["python", "app.py"]

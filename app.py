from flask import Flask, request, jsonify
import os
import uuid
import easyocr

app = Flask(__name__)

# สร้าง EasyOCR Reader (ใช้ CPU เท่านั้น)
reader = easyocr.Reader(['th', 'en'], gpu=False)

# กำหนดโฟลเดอร์เก็บไฟล์ชั่วคราว
UPLOAD_FOLDER = '/tmp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/ocr', methods=['POST'])
def ocr():
    """ รับไฟล์ภาพ และใช้ EasyOCR อ่านข้อความ """
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    # สร้างชื่อไฟล์แบบสุ่มและบันทึกลง `/tmp`
    filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}.jpg")
    file.save(filename)

    try:
        # ใช้ EasyOCR อ่านข้อมูลจากภาพ
        result = reader.readtext(filename, detail=1)
        lines = [{"text": txt, "confidence": conf} for (_, txt, conf) in result]

        return jsonify({"success": True, "data": {"lines": lines}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # ลบไฟล์ชั่วคราวหลังใช้งาน
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

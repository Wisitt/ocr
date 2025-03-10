from flask import Flask, request, jsonify
import os
import uuid
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['thai', 'eng'], gpu=False)

# โฟลเดอร์ชั่วคราวสำหรับเก็บไฟล์ที่อัปโหลด
UPLOAD_FOLDER = '/tmp'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    # บันทึกไฟล์ลงในโฟลเดอร์ /tmp ด้วยชื่อสุ่ม
    filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}.jpg")
    file.save(filename)

    try:
        # เรียกใช้งาน EasyOCR อ่านไฟล์
        result = reader.readtext(filename, detail=1)
        lines = [{"text": txt, "confidence": conf} for (_, txt, conf) in result]
        return jsonify({"success": True, "data": {"lines": lines}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        # ลบไฟล์ชั่วคราว
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

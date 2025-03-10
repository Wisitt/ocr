# easyocr_script.py
import sys
import json
import easyocr

"""
Usage: python easyocr_script.py <image_path> <lang1> [<lang2> ...]

- <image_path>: path ไฟล์รูปภาพ .jpg/.png ที่ต้องการ OCR
- <langX>: ภาษาที่ต้องการ เช่น "thai" "eng" 
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: python easyocr_script.py <image_path> <lang1> [<lang2> ...]"
        }, ensure_ascii=False))
        sys.exit(1)

    image_path = sys.argv[1]
    langs = sys.argv[2:]

    try:
        # สร้าง EasyOCR Reader, gpu=False เพื่อใช้ CPU
        reader = easyocr.Reader(langs, gpu=False)
        # อ่านข้อความจากรูป, detail=1 จะได้ bounding box + text + confidence
        result = reader.readtext(image_path, detail=1)

        # แปลง result ให้เป็น JSON-friendly
        lines = []
        for (coords, txt, conf) in result:
            lines.append({
                "text": txt,
                "confidence": conf
            })

        # พิมพ์ JSON ออกไป (stdout)
        print(json.dumps({
            "lines": lines
        }, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

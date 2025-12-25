from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from mistralai import Mistral
import base64
import uvicorn

app = FastAPI()

# السماح لـ Next.js بالاتصال بالباثيون
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # في الإنتاج ضع رابط موقعك فقط
    allow_methods=["*"],
    allow_headers=["*"],
)
  
api_key = "Y5JDeh9dvzsMRosyEVmQlBOLKxpyRsnc"
model = "pixtral-12b-2409"
client = Mistral(api_key=api_key)


@app.post("/ocr")
async def do_ocr(file: UploadFile = File(...)):
    # 1. قراءة الملف وتحويله لـ base64
    contents = await file.read()
    base64_image = base64.b64encode(contents).decode('utf-8')

    # 2. إرسال الطلب لـ Mistral
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract all text from this image accurately."},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
            ]
        }
    ]
    
    response = client.chat.complete(model=model, messages=messages)
    return {"text": response.choices[0].message.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
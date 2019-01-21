import face_recognition

import train

known_image = face_recognition.load_image_file("timg.jpg")
known_encoding = face_recognition.face_encodings(known_image)#对脸部信息编码,一个人
train.init()
reconize_result = train.recognize_from_upload(known_image)  # 识别结果
print(reconize_result)
import os

import face_recognition
face_datas ={}#存图片信息以及人脸编码，格式：{"bob":[...,..],...}

#添加数据：人脸编码信息
def add_data(who,pic_name):
    known_image = face_recognition.load_image_file(pic_name)
    known_encoding = face_recognition.face_encodings(known_image)#对脸部信息编码,一个人
    if known_encoding==[]:
        print("图片错误：",pic_name)
    else:
        known_encoding = known_encoding[0]
        if who in face_datas:
            face_datas[who].append(known_encoding)

        else:
            face_datas[who] = [known_encoding]


# 初始化，即训练文件中已有人脸信息
def init():
    names = [x for x in os.listdir("know_images")]#获取该文件夹下的目录名
    # print(names)
    for i in names:
        name = [x for x in os.listdir("./know_images/"+i)]
        # print(name)
        for j in name:#获取每一个文件夹下的图片名称
            add_data(i,"./know_images/"+i+"/"+j)#将文件夹名称及其目录下所有图片名称


# 从服务端选择文件识别，用于测试
def recognize_from_fold(who):
    unknown_image = face_recognition.load_image_file("obama2.jpeg")  # 需识别图片
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces(who, unknown_encoding)  # 比较，返回[true] 或[false]
    print(results)


# 从上传文件中识别
def recognize_from_upload(file):
    img_info = []

    unknown_image = face_recognition.load_image_file(file)  # 待识别图片

    unknown_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_encoding==[]:  # 无人脸
        return "noface"
    face_locations = face_recognition.face_locations(unknown_image)
    print("face_locations",face_locations)

    for k in unknown_encoding: #遍历多张脸

        find = False
        for i in face_datas:  # 遍历已训练的人脸编码信息
            if face_recognition.compare_faces(face_datas[i], k,tolerance=0.4)[0]:  # 比较字典中与待识别图片,第一个参数为数组！！！
                img_info.append(i)
                find = True
                break
        if not find:
            img_info.append("somebody")
    return img_info,face_locations

if __name__ == '__main__':
    init()
    # recognize_from_fold(face_datas['trump']['encoding'])




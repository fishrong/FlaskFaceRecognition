import base64
import os

import uuid



from PIL import Image
from flask import Flask, render_template, request
import face_recognition
from flask_script import Manager
import train


app = Flask(__name__)
# manager = Manager(app)
app.config['secret_key'] = "ddddd"
train.init()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/pichandler', methods=['post', 'get'])
def pichandler():
    name = ""
    locations =""

    pic_data_url = request.form.get("picdata")
    # print(">>>>>>>",request.form.get('picdata'))
    imgdata = base64.b64decode(pic_data_url.split(',')[1])
    with open("temp3.jpg", 'wb') as f:  # 把上传图片保存为文件，！！！有待优化
        f.write(imgdata)

    # pic = request.files.get("myPic")  # 上传图片
    # print("pic:",pic)

    reconize_result = train.recognize_from_upload("temp3.jpg")  # 识别结果
    print("Recognize_result:", reconize_result)
    print(type(reconize_result))
    for i in reconize_result[0]:
        if name == "":
            name = i
        else:
            name = name + "," + i
    for i in reconize_result[1]:
        if locations == "":
            locations = i
        else:
            locations = str(locations) + ";" + str(i)

    return str(name)+"-"+str(locations)


@app.route('/update', methods=['post', 'get'])
def update():
    pic_data_url = request.form.get("picdata")
    imgdata = base64.b64decode(pic_data_url.split(',')[1])

    with open("temp.jpg", 'wb') as f:  # 把上传图片保存为文件，！！！有待优化
        f.write(imgdata)
    known_image = face_recognition.load_image_file("temp.jpg")
    name_list = request.form.get("picinfo").split(",")  # 上传名字
    print("need_to_update:", name_list)
    for name in name_list:  # * 为内容未改变
        if name != "*":
            #  known_encoding = face_recognition.face_encodings(known_image)[name_list.index(name)]  # 对改变名字的脸部信息编码
            face_location = face_recognition.face_locations(known_image)[name_list.index(name)]
            top, right, bottom, left = face_location
            face_image = known_image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            if not os.path.exists("know_images/" + name):
                os.mkdir("know_images/" + name)
            uuid_str = uuid.uuid4().hex
            pil_image.save("know_images/" + name + "/" + uuid_str + ".jpg")  # 保存图片
            train.add_data(name, "know_images/" + name + "/" + uuid_str + ".jpg")

    # print(known_encoding)
    return "success"


@app.route('/vidohandler',methods=['get','post'])
def vido_handler():
    name = ""
    locations = ""
    pic_data_url = request.form.get("picdata")
    imgdata = base64.b64decode(pic_data_url.split(',')[1])

    with open("temp2.jpg", 'wb') as f:  # 把上传图片保存为文件，！！！有待优化
        f.write(imgdata)
    reconize_result = train.recognize_from_upload("temp2.jpg")  # 识别结果
    print("reconize_result:",reconize_result)
    if reconize_result=="noface":
        return reconize_result
    for i in reconize_result[0]:
        if name == "":
            name = i
        else:
            name = name + "," + i
    for i in reconize_result[1]:
        if locations == "":
            locations = i
        else:
            locations = str(locations) + ";" + str(i)

    return str(name)+"-"+str(locations)


@app.route('/testjpg',methods=['post','get'])
def testjpg():
    pic_data_url = request.form.get("picdata")
    #print(">>>>>>>",request.form.get('picdata'))

    imgdata = base64.b64decode(pic_data_url.split(',')[1])

    with open("temp3.jpg", 'wb') as f:  # 把上传图片保存为文件，！！！有待优化
        f.write(imgdata)
    return "success"



if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5001",ssl_context='adhoc')

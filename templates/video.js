//访问用户媒体设备的兼容方法
function getUserMedia(constraints, success, error) {
    if (navigator.mediaDevices.getUserMedia) {
        //最新的标准API
        navigator.mediaDevices.getUserMedia(constraints).then(success).catch(error);
    } else if (navigator.webkitGetUserMedia) {
        //webkit核心浏览器
        navigator.webkitGetUserMedia(constraints, success, error)
    } else if (navigator.mozGetUserMedia) {
        //firfox浏览器
        navigator.mozGetUserMedia(constraints, success, error);
    } else if (navigator.getUserMedia) {
        //旧版API
        navigator.getUserMedia(constraints, success, error);
    }
}

// let video = document.getElementById('video');


context.strokeStyle = "red";
context2.strokeStyle = "red";

function success(stream) {
    //兼容webkit核心浏览器
    let CompatibleURL = window.URL || window.webkitURL;
    //将视频流设置为video元素的源
    //console.log(stream);
    myStream = stream;
    //video.src = CompatibleURL.createObjectURL(stream);
    video.srcObject = stream;
    video.play();
}

function error(error) {
    console.log(`访问用户媒体设备失败${error.name}, ${error.message}`);
    document.getElementById("testvideo").innerHTML=`访问用户媒体设备失败${error.name}`+`${error.message}`;
}

function playvideo() {
    if (navigator.mediaDevices.getUserMedia || navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia) {
        //调用用户媒体设备, 访问摄像头
        getUserMedia({video: {width: 640, height: 480}}, success, error);
    } else {
        alert('不支持访问用户媒体');
    }
}


$('#upload').click(function () {
    console.log("开始上传...");
    context2.drawImage(video, 0, 0, video_width, video_height);
    var src = canvas2.toDataURL("image/jpeg");
    console.log(src);
    send(src, "{{ url_for('vido_handler') }}")
});
var timer;

function start_recognization() {
    timer = setInterval(upload, 800);
}

function stop_recognization() {
    clearInterval(timer);
    context.clearRect(0, 0, video_width, video_height);
}

function upload() {
    // console.log("开始上传...");

    context2.drawImage(video, 0, 0, video_width, video_height);
    var src = canvas2.toDataURL("image/jpeg");
    send_video_pic(src, "{{ url_for('vido_handler') }}")
}

function send_video_pic(fileList, url) {
    var fd = new FormData();
    fd.append("picdata", fileList);
    var xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    //服务器响应

    xhr.onreadystatechange = function () {
        context.clearRect(0, 0, video_width, video_height);

        if (xhr.status === 200 && xhr.readyState === 4 && xhr.responseText !== 'noface') {
            // console.log("success");

            var responses = xhr.responseText.split("-");//'-'分开名字和位置
            var response_names = responses[0].split(",");//名字数组
            // console.log("res_names:", response_names);


            var response_loctions = responses[1].split(";");//位置数组
            //div_names.innerHTML = "";//与服务器传回顺序颠倒

            for (var i = 0; i < response_names.length; i++) {


                //设置名字位置
                var res_loction = response_loctions[i].replace("(", "").replace(")", "").split(",");
                //console.log("res_locations:", res_loction);
                var top = parseInt(res_loction[0]);
                var right = parseInt(res_loction[1]);
                var bottom = parseInt(res_loction[2]);
                var left = parseInt(res_loction[3]);
                context.strokeStyle = "red";
                context.fillStyle = "red";

                context.fillRect(left, bottom, right - left, 30);//文字背景色
                context.strokeRect(left, top, right - left, bottom - top);//脸部框
                context.fillStyle = "white";
                context.font = "24px serif";
                context.textAlign = "center";
                context.fillText(response_names[i], (left + right) / 2, bottom + 20);//文字


            }

        }

    };
    xhr.send(fd);
}
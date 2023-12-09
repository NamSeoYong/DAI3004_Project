


// 전역 변수 선언
var video, canvas, context;

window.onload = function () {
    // DOM 요소 찾기
    video = document.getElementById("videoElement");
    canvas = document.getElementById("canvas");
    context = canvas.getContext('2d');

    // getUserMedia 호출
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
            })
            .catch(function (error) {
                console.error("비디오 스트림을 가져오는데 실패했습니다.", error);
            });
    } else {
        console.error("navigator.mediaDevices.getUserMedia가 지원되지 않습니다.");
    }
};

function takeSnapshot() {
    // video와 canvas가 DOM에 존재하는지 확인합니다.
    if (video && canvas) {
        // videoWidth와 videoHeight 속성이 사용 가능한지 확인합니다.
        if (video.videoWidth && video.videoHeight) {
            // 캔버스의 크기를 비디오와 일치시킵니다.
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            // 캔버스에 비디오의 현재 프레임을 그립니다.
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // 캔버스를 보이게 합니다. 이제 캡처된 이미지가 right-container 내의 캔버스에 표시됩니다.
            canvas.style.display = "block";

            // 비디오 요소를 숨깁니다.
            video.style.display = "none";
        } else {
            console.error("비디오의 크기를 가져올 수 없습니다.");
        }
    } else {
        console.error("video 또는 canvas 요소를 찾을 수 없습니다.");
    }
}


function loadImage() {
    var img = document.getElementById('loadedImage');
    if (img) {
        img.style.display = 'block';  // 이미지를 보이게 합니다.
        console.log('Image should be visible now');
    } else {
        console.log('Failed to find the image element');
    }
}
        
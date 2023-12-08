// 이미지 로드 함수
function loadImage() {
    var img = document.getElementById('loadedImage');
    img.src = "C:\\Users\\ehfkw\\Desktop\\signature\\docx\\file.jpg"; // 이미지 경로
    img.style.display = 'block';
}
​
// 기존 코드
var video = document.querySelector("#videoElement");
var canvas = document.getElementById("canvas");
var context = canvas.getContext('2d');
​
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
            console.log("Something went wrong!");
        });
}
​
// 촬영하기 버튼 클릭 시 동작할 함수
function takeSnapshot() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.style.display = "block"; // 캔버스를 보이게 합니다
    video.style.display = "none"; // 비디오를 숨깁니다
}
var video = document.querySelector("#videoElement");
var canvas = document.getElementById("canvas");
var context = canvas.getContext('2d');

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
            console.log("Something went wrong!");
        });
}

function takeSnapshot() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL("image/png");
    var newTab = window.open();
    newTab.document.write('<img src="' + dataURL + '">');
}

function writeToFile(text) {
    // Your write to file logic here
    console.log("Writing to file:", text);
    // Add your file writing code here
}

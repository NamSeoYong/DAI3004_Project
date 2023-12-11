function playAudio(filePath) {
  const audioElement = document.createElement("audio");
  audioElement.src = filePath;

  audioElement.addEventListener("canplaythrough", () => {
    audioElement.play();
  });
}

// 전역 변수 선언
var video, canvas, context;

window.onload = function () {
  // DOM 요소 찾기
  video = document.getElementById("videoElement");
  canvas = document.getElementById("canvas");
  context = canvas.getContext("2d");

  // getUserMedia 호출
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
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
  playAudio("static/tts/찰칵.mp3");
  // video와 canvas가 DOM에 존재하는지 확인합니다.
  if (video && canvas) {
    // videoWidth와 videoHeight 속성이 사용 가능한지 확인합니다.
    if (video.videoWidth && video.videoHeight) {
      // 캔버스의 크기를 비디오와 일치시킵니다.
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // 캔버스에 비디오의 현재 프레임을 그립니다.
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      // 캔버스에서 이미지를 JPEG 형식으로 변환
      var imageData = canvas.toDataURL("image/jpeg");

      // 서버로 전송
      sendImageToServer(imageData);
    } else {
      console.error("비디오의 크기를 가져올 수 없습니다.");
    }
  } else {
    console.error("video 또는 canvas 요소를 찾을 수 없습니다.");
  }
  video.style.display = "none";
  //-----------------------파이썬 코드 연결-------------------------

  $.ajax({
    url: "/run_script",
    type: "get",
    success: function (response) {
      console.log("run_script 완료", response);
      // 첫 번째 요청이 성공한 후, 두 번째 요청을 보냅니다.
      getSimilarity();
    },
    error: function (xhr) {
      console.error("run_script 오류 발생:", xhr);
    },
  });
}

function sendImageToServer(imageData) {
  fetch("/upload-image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image: imageData }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function loadImage(letter) {
  var img1 = document.getElementById("loadedImage1");
  var img2 = document.getElementById("loadedImage2");
  var img3 = document.getElementById("loadedImage3");
  if (letter == "A") {
    img1.style.display = "block"; // 이미지를 보이게 합니다.
    img2.style.display = "none";
    img3.style.display = "none";
    playAudio("static/tts/A.mp3");
    console.log("Image1 should be visible now");
  } else if (letter == "B") {
    img1.style.display = "none"; // 이미지를 보이게 합니다.
    img2.style.display = "block";
    img3.style.display = "none";
    playAudio("static/tts/B.mp3");
    console.log("Image2 should be visible now");
  } else if (letter == "C") {
    img1.style.display = "none"; // 이미지를 보이게 합니다.
    img2.style.display = "none";
    img3.style.display = "block";
    playAudio("static/tts/C.mp3");
    console.log("Image3 should be visible now");
  } else {
    console.log("Failed to find the image element");
  }

  $.ajax({
    url: "/receive_image_choice",
    type: "POST",
    data: { letter: letter },
    success: function (response) {
      console.log("서버 응답:", response);
    },
    error: function (xhr) {
      console.error("오류 발생:", xhr);
    },
  });
}

function getSimilarity() {
  // 두 번째 AJAX 요청: /get_similarity
  $.ajax({
    url: "/get_similarity",
    type: "get",
    success: function (response) {
      // 유사도 값으로 HTML 업데이트
      $("#similarity").text("유사도 " + response.similarity + "%");
      console.log("유사도 완료", response);
    },
    error: function (xhr) {
      console.error("get_similarity 오류 발생:", xhr);
    },
  });
}

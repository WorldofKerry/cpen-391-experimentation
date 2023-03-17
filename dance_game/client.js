let canvas = document.getElementById('canvas');
let context = canvas.getContext('2d');

let socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('video_feed', function(data) {
    let img = new Image();
    img.src = 'data:image/jpeg;base64,' + data.data;

    img.onload = function() {
        // Draw the image on the canvas
        context.drawImage(img, 0, 0, canvas.width, canvas.height);
    };
});

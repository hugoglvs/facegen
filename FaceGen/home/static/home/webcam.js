$(document).ready(function () {
    const video = $("#webcam")[0];
    const canvas = $("#canvas")[0];
    const captureButton = $("#capture-button");
    const photo1 = $("#photo1");
    const photo2 = $("#photo2");
    const photo3 = $("#photo3");
    const photos = [];
    const trashButton = $(".trash-button");
    const sendButton = $("#send-button");
    let photoIndex = 0;

    navigator.mediaDevices
        .getUserMedia({ video: true }) // -> Promise<MediaTrackConstraints>
        // The promise is resolved with a MediaStream object if the user grants permission
        .then((stream) => {
            const video = $("#webcam")[0];
            video.srcObject = stream;
            video.play();
        })
        .catch((err) => {
            console.error("Error accessing the webcam: " + err);
        });

    captureButton.on("click", function () {
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL("image/png");
        console.log(`dataURL: ${dataURL}`)
        photos.push(dataURL);
        console.log(`photos: ${photos}`);
        console.log(`length: ${photos.length}`);
        switch (photoIndex) {
            case 0:
                photo1.attr("src", dataURL);
                break;
            case 1:
                photo2.attr("src", dataURL);
                break;
            case 2:
                photo3.attr("src", dataURL);
                break;
        }
        photoIndex = (photoIndex + 1) % 3;
    });

    trashButton.on("click", function () {
        const targetPhoto = $(this).siblings("img");
        console.log("Deleting associated image");
        targetPhoto.attr("src", "");
    });

    sendButton.on("click", () => {
        try {
            // Set the hx-vals attribute with the stringified JSON
            sendButton.attr("hx-vals", {user_photos: JSON.stringify(photos)});
            sendButton.attr("hx-vals", JSON.stringify({user_photos: photos}));
        } catch (error) {
            // Catch and log any errors that occur during stringification
            console.error("Error stringifying photos object:", error);
        }
    });
});

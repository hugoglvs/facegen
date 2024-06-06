$(document).ready(function () {
    const video = $("#webcam")[0];
    const canvas = $("#canvas")[0];
    const captureButton = $("#capture-button");
    const photoElements = [$("[data-photo-index=0]>img"), $("[data-photo-index=1]>img"), $("[data-photo-index=2]>img")];
    const trashButtons = $(".trash-button");
    const sendButton = $("#send-button");
    let photoIndex = 0;

    function setupWebcam() {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
                video.play();
            })
            .catch((err) => {
                console.error("Error accessing the webcam: " + err);
            });
    }

    function capturePhoto() {
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataURL = canvas.toDataURL("image/png");
        updatePhotoDisplay(photoIndex, dataURL);
        photoIndex = getMissingPhotoIndex(photoElements);
    }

    function updatePhotoDisplay(photoIndex, dataURL) {
        photoElements[photoIndex].attr("src", dataURL);
    }

    function deletePhoto(button) {
        const targetPhotoIndex = $(button).parent().attr("data-photo-index");
        updatePhotoDisplay(targetPhotoIndex, "");
        return targetPhotoIndex;
    }

    function sendPhotos() {
        try {
            const photos = photoElements.map((photoElement) => photoElement.attr("src"));
            const photoData = JSON.stringify({ user_photos: photos });
            sendButton.attr("hx-vals", photoData);
            console.log("Photos sent:", photoData)
        } catch (error) {
            console.error("Error stringifying photos object:", error);
        }
    }

    // Returns the first index of the photo element that is missing the photo
    function getMissingPhotoIndex(photoElement) {
        return photoElement.findIndex((photo) => photo.attr("src") === "");
    }

    setupWebcam();

    captureButton.on("click", capturePhoto);

    trashButtons.each(function () {
        $(this).on("click", function () {
            photoIndex = deletePhoto(this);
        });
    });

    sendButton.on("click", function() { console.log('click')});
});

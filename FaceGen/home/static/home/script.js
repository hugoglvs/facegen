$(document).ready(function() {
    historyHandler();
    cameraHandler();
});

function historyHandler() {
    const $historyItems = $('.historique-item');

    $historyItems.each(function() {
        const $item = $(this);
        const $image = $item.find('img');
        const $description = $item.find('p');

        $image.on('click', function() {
            const $modalContainer = $('<div>').addClass('modal-container');
            const $modalContent = $('<div>').addClass('modal-content');
            const $exitButton = $('<div>').addClass('exit-button').text('X');
            const $enlargedImage = $('<img>').attr('src', $image.attr('src'));
            const $enlargedDescription = $('<p>').text($description.text());

            $modalContent.append($exitButton, $enlargedImage, $enlargedDescription);
            $modalContainer.append($modalContent);
            $('body').append($modalContainer);

            $modalContainer.on('click', function(event) {
                if ($(event.target).is($modalContainer) || $(event.target).is($exitButton)) {
                    $modalContainer.remove();
                }
            });
        });
    });
}
function cameraHandler() {
    $('#camera').on('click', function() {
        navigator.mediaDevices.getUserMedia({ video: true })  // -> Promise<MediaTrackConstraints>
            // The promise is resolved with a MediaStream object if the user grants permission
            .then((stream) => {
                const video = $('#webcam')[0];
                video.srcObject = stream;
                video.play();
            })

            .catch((err) => {
                console.error("Error accessing the webcam: " + err);
            });

    
        const canvas = $('#canvas')[0];
        const video = $('#webcam')[0];
        const context = canvas.getContext('2d');
        const photos = [];
        let photoCount = 0;

        const takePhoto = () => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            photos.push(canvas.toDataURL('image/png'));
            photoCount++;

            if (photoCount < 5) {
                setTimeout(takePhoto, 1000); // Take a photo every second
            } else {
                // Upload photos to the server
                $.ajax({
                    url: '/home/upload_photos/',
                    method: 'POST',
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    data: JSON.stringify({ photos: photos }),
                    success: function(response) {
                        console.log(response);
                        // Redirect to generate.html or perform other actions
                        
                    },
                    error: function(error) {
                        console.error('Error:', error);
                    }
                });
            }
        };
        takePhoto();
    });
}
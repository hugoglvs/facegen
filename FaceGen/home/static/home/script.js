$(document).ready(function() {
    const themeManager = themeSwitcher();
    themeManager.init();
    setInterval(() => {
        const themes = ['blueFamily', 'greenFamily', 'purpleFamily', 'redFamily'];
        const currentThemeIndex = themes.indexOf(themeManager.theme);
        const nextTheme = themes[(currentThemeIndex + 1) % themes.length];
        themeManager.changeTheme(nextTheme);
    }, 5*60*1000);

    let lastActivityTime = Date.now();
    // List of events to track
    const events = ['mousemove', 'keydown', 'click', 'scroll'];

    // Add event listeners to update the last activity time on user interaction
    events.forEach(event => {
        $(document).on(event, () => {
            lastActivityTime = Date.now();
        });
    });

    // Check if the user has been inactive for 5 minutes
    setInterval(() => {
        const currentTime = Date.now();
        const inactiveTime = currentTime - lastActivityTime;
        if (inactiveTime > 5*60*1000) {
            location.reload();
        }
    }, 1000);
});

function initHistoryItems() {
    const $historyItems = $('.history-item');

    $historyItems.each(function() {
        const $item = $(this);
        const $itemContainer = $item.parent();
        const $image = $item.find('img');
        const $description = $item.find('p');
        const $trashButton = $item.find('.trash-button');

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

function initWebcam() {
    const video = $("#webcam")[0];
    const canvas = $("#canvas")[0];
    const captureButton = $("#capture-button");
    const photoElements = $("[data-photo-index]>img");
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
        $(photoElements[photoIndex]).attr("src", dataURL);
    }

    function deletePhoto(button) {
        const targetPhotoIndex = $(button).parent().attr("data-photo-index");
        updatePhotoDisplay(targetPhotoIndex, "");
        return targetPhotoIndex;
    }

    function sendPhotos() {
        try {
            const photos = photoElements.toArray().map((photoElement) => $(photoElement).attr("src"));
            const validPhotos = photos.filter(photo => photo); // Filter out empty src values
            const photoData = JSON.stringify({ user_photos: validPhotos });
            sendButton.attr("hx-vals", photoData);
        } catch (error) {
            console.error("Error stringifying photos object:", error);
        }
    }

    // Returns the first index of the photo element that is missing the photo
    function getMissingPhotoIndex(photoElements) {
        return photoElements.toArray().findIndex((photo) => $(photo).attr("src") === "");
    }

    setupWebcam();

    captureButton.on("click", capturePhoto);

    trashButtons.each(function () {
        $(this).on("click", function () {
            photoIndex = deletePhoto(this);
        });
    });

    sendButton.on("click", sendPhotos);
};

function themeSwitcher() {
    const themeManager = {
        theme: localStorage.getItem('theme') || 'blueFamily',
        init() {
            this.applyTheme(this.theme);
            this.observeThemeChange();
        },
        applyTheme(themeName) {
            const themes = {
                blueFamily: {
                    '--primary-color': 'var(--blue-primary)',
                    '--secondary-color': 'var(--blue-secondary)',
                    '--tertiary-color': 'var(--blue-tertiary)',
                },
                greenFamily: {
                    '--primary-color': 'var(--green-primary)',
                    '--secondary-color': 'var(--green-secondary)',
                    '--tertiary-color': 'var(--green-tertiary)',
                },
                purpleFamily: {
                    '--primary-color': 'var(--purple-primary)',
                    '--secondary-color': 'var(--purple-secondary)',
                    '--tertiary-color': 'var(--purple-tertiary)',
                },
                redFamily: {
                    '--primary-color': 'var(--red-primary)',
                    '--secondary-color': 'var(--red-secondary)',
                    '--tertiary-color': 'var(--red-tertiary)',
                },
            };

            const theme = themes[themeName];
            for (const variable in theme) {
                $(':root').css(variable, theme[variable]);
            }
        },
        changeTheme(newTheme) { 
            this.theme = newTheme;
            this.applyTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        },
        observeThemeChange() {
            let currentTheme = this.theme;
            setInterval(() => {
                if (this.theme !== currentTheme) {
                    this.applyTheme(this.theme);
                    localStorage.setItem('theme', this.theme);
                    currentTheme = this.theme;
                }
            }, 100);
        }
    };

    return themeManager;
}


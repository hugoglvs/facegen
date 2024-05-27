document.addEventListener("DOMContentLoaded", function() {
            const historiqueItems = document.querySelectorAll('.historique-item');

            historiqueItems.forEach(item => {
                const image = item.querySelector('img');
                const description = item.querySelector('p');
                
                image.addEventListener('click', function() {
                    const modalContainer = document.createElement('div');
                    modalContainer.classList.add('modal-container');

                    const modalContent = document.createElement('div');
                    modalContent.classList.add('modal-content');

                    const exitButton = document.createElement('div');
                    exitButton.classList.add('exit-button');
                    exitButton.textContent = 'X';

                    const enlargedImage = document.createElement('img');
                    enlargedImage.src = image.src;

                    const enlargedDescription = document.createElement('p');
                    enlargedDescription.textContent = description.textContent;

                    modalContent.appendChild(exitButton);
                    modalContent.appendChild(enlargedImage);
                    modalContent.appendChild(enlargedDescription);

                    modalContainer.appendChild(modalContent);

                    document.body.appendChild(modalContainer);

                    modalContainer.addEventListener('click', function(event) {
                        if (event.target === modalContainer || event.target === exitButton) {
                            modalContainer.remove();
                        }
                    });
                });
            });
        });
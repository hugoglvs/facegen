$(document).ready(function() {
    initHistoryItems();
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

        // $trashButton.on('click', () => {
        //     $itemContainer.remove();
        // });
    });
}
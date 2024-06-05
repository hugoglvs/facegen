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
    });
}

function themeSwitcher() {
  return {
    theme: localStorage.getItem('theme') || 'blueFamily',
    init() {
      this.applyTheme(this.theme);
      this.$watch('theme', value => {
        this.applyTheme(value);
        localStorage.setItem('theme', value);
      });
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
    }
  }
}
  
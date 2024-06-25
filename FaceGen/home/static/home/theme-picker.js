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

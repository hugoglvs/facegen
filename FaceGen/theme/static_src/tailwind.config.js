/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        colors: {
            berry: {
              100: '#ffebf5',
              200: '#ffc0df',
              300: '#f69ac6',
              400: '#e574aa',
              500: '#cb548d',
              600: '#ba467d',
              700: '#a8396f',
              800: '#7f234f',
              900: '#511230',
            },
            black: '#000000',
            blue: {
              100: '#d9f5fd',
              200: '#94dcf7',
              300: '#5cc1ee',
              400: '#31a2e3',
              500: '#1282d6',
              600: '#0672cb',
              700: '#0063b8',
              800: '#00468b',
              900: '#002a58',
            },
            gray: {
              100: '#f5f6f7',
              200: '#f0f0f0',
              300: '#e1e1e1',
              400: '#d2d2d2',
              500: '#b6b6b6',
              600: '#7e7e7e',
              700: '#6e6e6e',
              800: '#636363',
              900: '#0e0e0e',
            },
            green: {
              100: '#e9f5ce',
              200: '#c0dd78',
              300: '#9bc438',
              400: '#7aa809',
              500: '#5d8c00',
              600: '#4f7d00',
              700: '#436f00',
              800: '#2c5000',
              900: '#193100',
            },
            'light-blue': {
              100: '#daf5fd',
              200: '#97dcf4',
              300: '#61c1eb',
              400: '#36a2e0',
              500: '#1885c3',
              600: '#0d76b2',
              700: '#0468a1',
              800: '#004a77',
              900: '#002d4b',
            },
            orange: {
              100: '#ffeed2',
              200: '#fec97a',
              300: '#f8a433',
              400: '#e67f01',
              500: '#c96100',
              600: '#b85200',
              700: '#a64600',
              800: '#7d2e00',
              900: '#4f1a00',
            },
            purple: {
              100: '#fbebff',
              200: '#ecc4ff',
              300: '#db9eff',
              400: '#c47af4',
              500: '#a95adc',
              600: '#994ccc',
              700: '#8a3fba',
              800: '#66278f',
              900: '#40155c',
            },
            red: {
              100: '#ffecee',
              200: '#ffc3c9',
              300: '#ff99a1',
              400: '#fe6873',
              500: '#e4424d',
              600: '#d0353f',
              700: '#bb2a33',
              800: '#8c161f',
              900: '#590a0f',
            },
            slate: {
              100: '#ebf1f6',
              200: '#c5d4e3',
              300: '#a4b8cd',
              400: '#839db4',
              500: '#40586d',
              600: '#293b4d',
              700: '#1d2c3b',
              800: '#141d28',
              900: '#0a0e14',
            },
            white: '#ffffff',
            yellow: {
              100: '#feefcb',
              200: '#f5cd6f',
              300: '#e6ac28',
              400: '#ce8d00',
              500: '#b36f00',
              600: '#a36100',
              700: '#925400',
              800: '#6d3a00',
              900: '#442200',
            },
          },
        extend: {
            fontFamily: {
                roboto: ['Roboto', 'sans-serif'],
            },
            animation: {
              'fade-in': 'fadeIn 0.5s ease-in-out forwards',
              'fade-out': 'fadeOut 0.5s ease-in-out forwards',
            },
            keyframes: {
              fadeIn: {
                '0%': { opacity: 0, height: 0 },
                '100%': { opacity: 1, height: 'auto' },
              },
              fadeOut: {
                '0%': { opacity: 1, height: 'auto' },
                '100%': { opacity: 0, height: 0 },
              },  
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}

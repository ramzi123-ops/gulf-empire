// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Include global templates
    './apps/*/templates/**/*.html', // Include templates in each app
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00869E',
          50: '#E6F7FA',
          100: '#CCEFF5',
          200: '#99DFEB',
          300: '#66CFE1',
          400: '#33BFD7',
          500: '#00869E',
          600: '#006B7E',
          700: '#00505F',
          800: '#00353F',
          900: '#001A20',
        },
        secondary: {
          DEFAULT: '#065084',
          50: '#E6F0F8',
          100: '#CCE1F1',
          200: '#99C3E3',
          300: '#66A5D5',
          400: '#3387C7',
          500: '#065084',
          600: '#05406A',
          700: '#04304F',
          800: '#032035',
          900: '#01101A',
        },
      },
    },
  },
  plugins: [],
}
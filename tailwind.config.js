// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Include global templates
    './apps/*/templates/**/*.html', // Include templates in each app
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
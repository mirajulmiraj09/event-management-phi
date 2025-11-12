/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // template at the project level
    "./**/templates/**/*.*html" // template at the app level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


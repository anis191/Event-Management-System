/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Templates at the project level
    "./**/templates/**/*.html", // Templates inside apps

    // Python files containing Tailwind classes
    "./**/forms.py",
    "./**/views.py",
    "./**/models.py",
    
    // JavaScript files (if any)
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#0a0e17',
          800: '#0f1419',
          700: '#151b26',
          600: '#1f2937',
          500: '#374151',
        }
      }
    },
  },
  plugins: [],
}

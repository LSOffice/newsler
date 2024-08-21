/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx,ts,tsx}", "./components/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: '#275F6F',
        secondary: '#FCA311',
        tertiary: '#D3D3D3'
      }
    },
  },
  plugins: [],
}


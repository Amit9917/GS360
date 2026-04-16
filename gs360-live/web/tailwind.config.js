/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#234e7a",
          600: "#1e3a5f",
          700: "#1a2f4a",
          800: "#0f1d30",
          900: "#0a1420",
        },
        accent: {
          50: "#fdf2f8",
          100: "#fce7f3",
          200: "#fbcfe8",
          300: "#f9a8d4",
          400: "#e64f7e",
          500: "#d6336c",
          600: "#be185d",
        },
        upsc: {
          polity: "#2563eb",
          history: "#d97706",
          geography: "#059669",
          economy: "#7c3aed",
          science: "#dc2626",
          ethics: "#0891b2",
          current: "#ea580c",
          environment: "#16a34a",
        },
      },
      fontFamily: {
        sans: ["Plus Jakarta Sans", "system-ui", "sans-serif"],
        serif: ["Lora", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};

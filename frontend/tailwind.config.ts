import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f4ff",
          100: "#e0eaff",
          500: "#4f72ff",
          600: "#3a5bff",
          700: "#2642e8",
          900: "#1a2e99",
        },
      },
    },
  },
  plugins: [],
};
export default config;

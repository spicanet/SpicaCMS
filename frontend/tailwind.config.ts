// frontend/tailwind.config.ts

import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: 'class',
  content: [
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        transparent: 'transparent',
        current: 'currentColor',
        dbg: '#121212',
        lbg: '#f5f5f5',
        dtext: '#121212',
        ltext: '#f5f5f5',
        dcard: '#242424',
        lcard: '#f5f5f5',
        navigation: '#242424',
        primary: '#FF6B00',
        secondary: '#00996B',
      },
    },
  },
  plugins: [],
}

export default config;

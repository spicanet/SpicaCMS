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
        dbg: '#000000',
        lbg: '#ffffff',
        dtext: '#000000',
        ltext: '#ffffff',
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

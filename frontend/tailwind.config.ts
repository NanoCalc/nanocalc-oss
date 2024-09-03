import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
	      "nanocalc-blue": "#403E90",
        "nanocalc-apps": "#A7CDA6",
        "nanocalc-apps-button": "#3D7148"
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        'gradient-theme-nanocalc-apps': `linear-gradient(to bottom, theme('colors.nanocalc-apps'), rgb(var(--background-end-rgb)))`,
        'gradient-theme-common-logos': `linear-gradient(to top, theme('colors.nanocalc-apps'), rgb(var(--background-end-rgb)))`,
        'gradient-theme-nanocalc-apps-md': `linear-gradient(to left, theme('colors.nanocalc-apps'), rgb(var(--background-end-rgb)))`,
        'gradient-theme-common-logos-md': `linear-gradient(to right, theme('colors.nanocalc-apps'), rgb(var(--background-end-rgb)))`,
      },
      animation: {
        fadeIn: 'fadeIn 1s ease-in-out',
        slideIn: 'slideIn 1s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        slideIn: {
          '0%': { transform: 'translateY(-20px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 },
        },
      },
    },
  },
  plugins: [],
};

export default config;

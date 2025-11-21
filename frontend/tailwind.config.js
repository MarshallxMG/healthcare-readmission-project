/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          blue: '#00f3ff',
          purple: '#bc13fe',
          green: '#0aff0a',
        },
        dark: {
          bg: '#050505',
          card: '#101010',
          surface: '#1a1a1a'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #00f3ff, 0 0 10px #00f3ff' },
          '100%': { boxShadow: '0 0 20px #bc13fe, 0 0 30px #bc13fe' },
        }
      }
    },
  },
  plugins: [],
};

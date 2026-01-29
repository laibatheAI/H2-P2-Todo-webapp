/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/*.{js,ts,jsx,tsx,mdx}', // Explicitly include root app files
  ],
  darkMode: 'class', // Enable dark mode using the 'class' strategy
  theme: {
    extend: {
      colors: {
        'emerald-teal': {
          50: '#EAF7F4',
          100: '#D5EEE8',
          200: '#ABDED0',
          300: '#80CEB7',
          400: '#49BFA7',
          500: '#1FB37A', // Primary Green
          600: '#169B69', // Primary Hover / Active
          700: '#127D57',
          800: '#0F6247',
          900: '#0D4F3A',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
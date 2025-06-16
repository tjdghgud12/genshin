import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./pages/**/*.{js,ts,jsx,tsx,mdx}', './components/**/*.{js,ts,jsx,tsx,mdx}', './app/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      spacing: {
        /* % size */
        '1/20': '5%',
        '1/16': '6.25%',
        '1/11': '9.09%',
        '1/10': '10%',
        '1/8': '12.5%',
        '1/7': '14.3%',
        '1/5': '20%',
        '3/10': '30%',
        '7/10': '70%',
        '8/10': '80%',
        '7/8': '87.5%',
        '9/10': '90%',
        '15/100': '43%',
        '43/100': '43%',
        '45/100': '45%',
        '55/100': '55%',
        '95/100': '95%',
        userMain: '89%',
        /* px Size */
        '1px': '1px',
        m: '15px',
        '1.5px': '1.5px',
        '3px': '3px',
      },
    },
  },
  plugins: [],
};
export default config;

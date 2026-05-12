import defaultTheme from 'tailwindcss/defaultTheme'

export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['DM Sans', ...defaultTheme.fontFamily.sans],
        display: ['Sora', ...defaultTheme.fontFamily.sans],
        mono: ['JetBrains Mono', ...defaultTheme.fontFamily.mono],
      },
      colors: {
        bg: {
          base: '#0A0A0F',
          surface: '#111118',
          elevated: '#18181F',
          border: '#25252E',
        },
        accent: '#7C3AED',
        accentGlow: '#5B21B6',
        accentSoft: '#EDE9FE',
        text: {
          primary: '#F1F0F5',
          secondary: '#8B8A9B',
          muted: '#4A4958',
        },
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
      },
      boxShadow: {
        accent: '0 0 0 1px #7C3AED',
        glow: '0 0 0 10px rgba(124,58,237,0.12)',
      },
      transitionTimingFunction: {
        mellow: 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
      transitionDuration: {
        350: '350ms',
      },
    },
  },
  plugins: [],
}

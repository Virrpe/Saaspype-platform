/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    './src/**/*.svelte'
  ],
  theme: {
    extend: {
      colors: {
        // LuciQ Brand Kit v1.0 - Professional Color System
        midnight: '#0C0E16',    // Primary dark background
        'pure-white': '#FFFFFF', // Text, logo base
        'lucid-blue': {
          start: '#009DF5',     // Gradient start
          end: '#22D1EE',       // Gradient end
          solid: '#009DF5'      // Solid version
        },
        'wave-cyan': '#3BF0DA', // Accent for waveform
        'slate-gray': '#6B7280', // Secondary text, borders
        
        // Extended professional palette
        success: '#10B981',     // Positive metrics
        warning: '#F59E0B',     // Alerts
        error: '#EF4444',       // Critical states
        info: '#3B82F6',        // Neutral info
        
        // Sophisticated grayscale system
        gray: {
          50: '#F9FAFB',
          100: '#F3F4F6', 
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',   // Brand Slate Gray
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          900: '#111827'
        },
        
        // Legacy compatibility (will be phased out)
        primary: {
          500: '#009DF5',
          600: '#0082D1',
          700: '#006BA3'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      fontSize: {
        // LuciQ Professional Typography Scale
        'xs': ['12px', { lineHeight: '16px' }],
        'sm': ['14px', { lineHeight: '20px' }],
        'base': ['16px', { lineHeight: '24px' }],
        'lg': ['18px', { lineHeight: '28px' }],
        'xl': ['20px', { lineHeight: '32px' }],
        '2xl': ['24px', { lineHeight: '36px' }],
        '3xl': ['30px', { lineHeight: '42px' }],
        '4xl': ['36px', { lineHeight: '48px' }],
        '5xl': ['48px', { lineHeight: '60px' }],
        '6xl': ['60px', { lineHeight: '72px' }],
        '7xl': ['72px', { lineHeight: '84px' }]
      },
      fontWeight: {
        light: '300',
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
        extrabold: '800',
        black: '900'
      },
      // Phase 2: Professional 8-Point Grid System
      spacing: {
        // 8pt grid system for enterprise-grade consistency
        '1': '0.125rem',    // 2px
        '2': '0.25rem',     // 4px
        '3': '0.375rem',    // 6px
        '4': '0.5rem',      // 8px  - Base unit
        '5': '0.625rem',    // 10px
        '6': '0.75rem',     // 12px
        '8': '1rem',        // 16px - 2x base
        '10': '1.25rem',    // 20px
        '12': '1.5rem',     // 24px - 3x base
        '16': '2rem',       // 32px - 4x base
        '20': '2.5rem',     // 40px - 5x base
        '24': '3rem',       // 48px - 6x base
        '32': '4rem',       // 64px - 8x base
        '40': '5rem',       // 80px - 10x base
        '48': '6rem',       // 96px - 12x base
        '56': '7rem',       // 112px - 14x base
        '64': '8rem',       // 128px - 16x base
        '72': '9rem',       // 144px - 18x base
        '80': '10rem',      // 160px - 20x base
        '96': '12rem',      // 192px - 24x base
        
        // Professional layout spacing
        '18': '4.5rem',     // 72px - Custom for layouts
        '88': '22rem',      // 352px - Large sections
        '104': '26rem',     // 416px - Hero sections
        '112': '28rem',     // 448px - Feature sections
        '128': '32rem',     // 512px - Container max-widths
        
        // Section spacing system
        'section-xs': '3rem',    // 48px - Compact sections
        'section-sm': '4rem',    // 64px - Small sections  
        'section-md': '6rem',    // 96px - Medium sections
        'section-lg': '8rem',    // 128px - Large sections
        'section-xl': '12rem',   // 192px - Extra large sections
        'section-2xl': '16rem',  // 256px - Hero sections
        
        // Component spacing
        'component-xs': '0.5rem',  // 8px - Tight spacing
        'component-sm': '1rem',    // 16px - Small spacing
        'component-md': '1.5rem',  // 24px - Medium spacing
        'component-lg': '2rem',    // 32px - Large spacing
        'component-xl': '3rem'     // 48px - Extra large spacing
      },
      boxShadow: {
        // Professional shadow system for depth
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'card-hover': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'button': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'button-hover': '0 2px 4px 0 rgba(0, 0, 0, 0.1)',
        'professional': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        
        // Phase 2: Enhanced shadow system
        'section': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'section-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glass-hover': '0 8px 32px 0 rgba(31, 38, 135, 0.5)'
      },
      borderRadius: {
        'lg': '12px',
        'xl': '16px',
        '2xl': '20px',
        '3xl': '24px',
        '4xl': '32px'
      },
      // Phase 2: Sophisticated Background System
      backgroundImage: {
        // Professional gradient backgrounds
        'gradient-primary': 'linear-gradient(135deg, #009DF5 0%, #22D1EE 100%)',
        'gradient-dark': 'linear-gradient(135deg, #0C0E16 0%, #1F2937 50%, #374151 100%)',
        'gradient-light': 'linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%)',
        'gradient-midnight': 'linear-gradient(135deg, #0C0E16 0%, #111827 100%)',
        'gradient-wave': 'linear-gradient(135deg, #22D1EE 0%, #3BF0DA 100%)',
        
        // Section-specific backgrounds
        'hero-pattern': "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%233BF0DA' fill-opacity='0.05'%3E%3Cpath d='M8,6 Q10,4 12,6 T16,6 T20,6 M28,6 Q30,4 32,6 T36,6 T40,6'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
        'grid-pattern': "url(\"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23F3F4F6' fill-opacity='0.4'%3E%3Cpath d='M0 0h40v40H0z'/%3E%3Cpath d='M0 20h40M20 0v40' stroke='%23E5E7EB' stroke-width='1'/%3E%3C/g%3E%3C/svg%3E\")",
        'dots-pattern': "url(\"data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23D1D5DB' fill-opacity='0.3'%3E%3Ccircle cx='3' cy='3' r='1'/%3E%3Ccircle cx='13' cy='13' r='1'/%3E%3C/g%3E%3C/svg%3E\")"
      },
      // Phase 2: Advanced Layout Utilities
      maxWidth: {
        'section': '1280px',     // Standard section width
        'content': '1024px',     // Content width
        'prose': '768px',        // Reading width
        'narrow': '640px'        // Narrow content
      },
      minHeight: {
        'section': '400px',      // Minimum section height
        'hero': '600px',         // Hero section height
        'feature': '300px'       // Feature section height
      }
    },
  },
  plugins: [],
} 
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      // Palette reprise telle quelle du prototype d'écrans validé
      // (NkulIA_Prototype_Ecrans.html) — une seule source de vérité visuelle.
      colors: {
        forest: '#1F5D42',
        'forest-deep': '#123825',
        laterite: '#B44B26',
        gold: '#B5842A',
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./oblique/components/*.jinja",
  ],
  theme: {
    fontFamily: {
      sans: ["Roboto", "sans-serif"],
      body: ["Roboto", "sans-serif"],
      mono: ["ui-monospace", "monospace"],
    },
  },
  plugins: [],
  corePlugins: {
    preflight: false,
  },
  darkMode: "class",
}

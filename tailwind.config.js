/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./core/templates/core/*.html",
    "./core/templates/core/includes/*.html",
    "./userauth/templates/userauth/*.html",
  ],
  theme: {
    fontFamily: {
      openSans: 'OpenSans',
      openSansMedium: 'OpenSansMedium',
      openSansBold: 'OpenSansBold',
      sourceSansPro: 'SourceSansPro',
    },
    extend: {
      width: {
        '10p': '10%',
        '18p': '18%',
        '20p': '20%',
        '30p': '30%',
        '40p': '40%',
        '50p': '50%',
        '60p': '60%',
        '70p': '70%',
        '80p': '80%',
        '90p': '90%',
      },
      colors: {
        primary: '#125615',
        secondary: '#BEBDBD',
        tertiary: '#FFC805',
        background: '#EBEBEB',
      },
    },
  },
  plugins: [],
}

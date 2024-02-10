const mobileMenu = document.querySelector('.mobile-menu')
const navigationBarOptions = document.querySelector('.navigation-bar-options')

mobileMenu.addEventListener('click', function (e) {
  mobileMenu.classList.toggle('active')
  navigationBarOptions.classList.toggle('active')
})

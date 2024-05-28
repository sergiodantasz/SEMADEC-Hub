document.getElementById('form-logout').addEventListener('submit', function (e) {
  e.preventDefault()
  window.location.href = 'https://suap.ifrn.edu.br/accounts/logout/'
  this.submit()
})

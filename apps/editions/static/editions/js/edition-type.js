const editionsTypeContainers = document.querySelectorAll('#id_edition_type > div')

editionsTypeContainers.forEach((el) => {
  el.addEventListener('click', (e) => {
    el.firstElementChild.click()
  })
})

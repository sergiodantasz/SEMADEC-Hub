const imagesInput = document.querySelector('#id_images')
const imagesInfo = document.querySelector('.images-info')

function updateSelectedImages() {
  const filesLength = imagesInput.files.length
  if (filesLength == 0) {
    imagesInfo.textContent = 'Nenhum arquivo selecionado.'
  } else if (filesLength == 1) {
    imagesInfo.textContent = '1 arquivo selecionado.'
  } else {
    imagesInfo.textContent = `${filesLength} arquivos selecionados.`
  }
}

imagesInput.addEventListener('change', e => updateSelectedImages())

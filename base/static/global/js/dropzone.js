const dropzoneContainer = document.getElementById('dropzone-container')
const dropzoneArea = document.getElementById('dropzone-area')
const fileInfo = document.getElementById('dropzone-file-info')
const uploadButton = document.getElementById('dropzone-upload-button')
const iconInput = document.getElementById('id_cover')

function getCurrentFile() {
  return iconInput.files[0]
}

function setStyle(type) {
  if (type === 'over') {
    dropzoneContainer.classList.replace('dropzone-default', 'dropzone-over')
  } else {
    dropzoneContainer.classList.replace('dropzone-over', 'dropzone-default')
  }
}

function setFileInfo(text) {
  fileInfo.textContent = text
}

function makeFileInfoMessage(file) {
  return `${file.name} (${file.size} bytes)`
}

const fileInfoMessages = {
  withoutFile: 'Nenhum arquivo selecionado.',
  onOver: 'Solte para carregar o arquivo.'
}

iconInput.addEventListener('change', e => {
  file = getCurrentFile()
  if (file) {
    setFileInfo(makeFileInfoMessage(file))
  } else {
    setFileInfo(fileInfoMessages.withoutFile)
  }
})

uploadButton.addEventListener('click', e => iconInput.click())

dropzoneArea.addEventListener('dragover', e => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'copy'
  setStyle('over')
  setFileInfo(fileInfoMessages.onOver)
})

dropzoneArea.addEventListener('dragleave', e => {
  e.preventDefault()
  setStyle()
  file = getCurrentFile()
  if (file) {
    setFileInfo(makeFileInfoMessage(file))
  } else {
    setFileInfo(fileInfoMessages.withoutFile)
  }
})

dropzoneArea.addEventListener('drop', e => {
  e.preventDefault()
  setStyle()
  iconInput.files = e.dataTransfer.files
  file = getCurrentFile()
  if (file) {
    setFileInfo(makeFileInfoMessage(file))
  } else {
    setFileInfo(fileInfoMessages.withoutFile)
  }
})

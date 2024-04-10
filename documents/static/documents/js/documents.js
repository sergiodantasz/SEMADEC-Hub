const documentsInput = document.querySelector('#id_documents')
const documentsList = document.querySelector('.documents-list-container')

const header = `
  <div class="documents-list-row documents-list-row-header">
    <span><strong>Nome de exibição</strong></span>
    <span><strong>Arquivo</strong></span>
  </div>
`

const nothingFound = `
  <div class="nothing-found">
    <p>Nenhum documento foi selecionado.</p>
  </div>
`

const documentElement = `
  <div class="documents-list-row">
    <input type="text" name="document-{input-name}" value="{input-value}" maxlength="100" required="true">
    <span>{file-name} ({file-size} bytes)</span>
  </div>
`

function changeDocuments() {
  documentsList.innerHTML = header
  if (documentsInput.files.length > 0) {
    for (let i = 0; i < documentsInput.files.length; i++) {
      const file = documentsInput.files[i]
      documentsList.innerHTML += documentElement
        .replace('{input-name}', i)
        .replace('{input-value}', file.name)
        .replace('{file-name}', file.name)
        .replace('{file-size}', file.size)
    }
  } else {
    documentsList.innerHTML += nothingFound
  }
}

documentsInput.addEventListener('change', (e) => {changeDocuments()})

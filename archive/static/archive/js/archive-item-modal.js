let dialog = document.querySelector(".dialog");
let dialogImage = dialog.querySelector(".dialog-image");

let closeButton = document.getElementById("dialog-button-close");
let downloadButton = document.getElementById("dialog-button-download");
let deleteButton = document.getElementById("dialog-button-delete");

let imageContainers = document.querySelectorAll(".archive-image-wrapper");

const imageDeleteUrl = "/acervo/imagem/apagar/";

imageContainers.forEach((imageContainer) => {
  imageContainer.addEventListener("click", function (e) {
    const image = e.target;
    dialogImage.src = image.src;
    const imagePk = this.getAttribute("pk");
    deleteButton?.setAttribute("href", imageDeleteUrl.concat(imagePk, "/"));
    downloadButton.setAttribute("href", image.src);
    downloadButton.setAttribute("download", true);
    dialog.showModal();
  });
});

closeButton.addEventListener("click", (e) => dialog.close());
deleteButton?.addEventListener("click", (e) => dialog.close());

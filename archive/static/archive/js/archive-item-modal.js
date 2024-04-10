let containerOuter = document.querySelector('.images-container');
let containerInner = containerOuter.querySelectorAll('.archive-image-wrapper');
let modal = document.querySelector('.archive-modal');
let modalImage = document.querySelector('.archive-modal-image');
let closeButton = document.getElementById('archive-modal-button-close')

containerInner.forEach(function(container) {
  container.addEventListener('click', function(event) {
    let containerClicked = event.target;
    modalImage.src = containerClicked.src;
    modal.showModal();
  });
});

closeButton.onclick = function () {
  modal.close();
}
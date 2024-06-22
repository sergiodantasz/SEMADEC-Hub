const sidebar = document.querySelector(".sidebar");
const toggleSidebarButton = sidebar.querySelector(".toggle-sidebar");

toggleSidebarButton.addEventListener("click", () => {
  sidebar.classList.toggle("closed");
});

const navigationBarOptionContainer = document.querySelector(
  ".navigation-bar-options"
);
const options = navigationBarOptionContainer.querySelectorAll("li");

let currentNamespace = navigationBarOptionContainer
  .getAttribute("current-namespace")
  .split(":")
  .at(-2);

if (currentNamespace === "sports" || currentNamespace === "tests") {
  currentNamespace = "competitions";
}

options.forEach((option) => {
  if (option.id === currentNamespace) {
    option.classList.add("navigation-bar-current");
  }
});

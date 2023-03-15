const skillChoices = document.querySelectorAll(".skill-level")

md = new markdownit().disable(['list'])
skillChoices.forEach(choice => {
  formatMarkdownText(choice.parentElement)
})

function formatMarkdownText(label){
  const labelText = md.renderInline(label.innerText)
  spanEl = document.createElement("span")
  spanEl.innerHTML = labelText
  label.lastChild.replaceWith(spanEl)
}

window.addEventListener("load", () => {
  const validationErrorEl = document.querySelector(".help")
  validationErrorEl.parentElement.classList.add("has-background-danger-light", "pt-2")
})



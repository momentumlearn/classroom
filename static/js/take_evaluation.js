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



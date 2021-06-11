const skills = document.querySelector("#div_id_skills")
all_skills = skills.querySelectorAll("input")
const selectAllBtn = document.querySelector("#select-all")

const toggleSkills = () => {
  selectAllSkills()
  toggleButtonText()
}

const toggleButtonText = () => {
  text = selectAllBtn.innerText
  selectAllBtn.innerText = text == 'Check All' ? 'Uncheck all' : 'Check all'
}
const selectAllSkills = () => all_skills.forEach(skill => skill.toggleAttribute('checked'))

selectAllBtn.addEventListener("click", toggleSkills)

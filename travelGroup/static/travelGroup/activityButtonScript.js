const activityButton = document.getElementById("add_activity_button")
const totalNewForms = document.getElementById("id_form-TOTAL_FORMS")

activityButton.addEventListener("click", add_new_form)

function add_new_form(event){
    if(event){
        event.preventDefault()
    }
    
    const currentActivityForms = document.getElementsByClassName("activity_form")
    const currentFormCount = currentActivityForms.length //+ 1 
    const formCopyTarget = document.getElementById("activity_formset")
    const copyEmptyActivityForm = document.getElementById("empty_form").cloneNode(true)
    copyEmptyActivityForm.setAttribute("class", "activity_form")
    copyEmptyActivityForm.setAttribute("id", `form-${currentFormCount}`)
    const regex = new RegExp("__prefix__", "g")
    copyEmptyActivityForm.innerHTML = copyEmptyActivityForm.innerHTML.replace(regex, currentFormCount)
    totalNewForms.setAttribute("value", currentFormCount+1)
    formCopyTarget.append(copyEmptyActivityForm)

}


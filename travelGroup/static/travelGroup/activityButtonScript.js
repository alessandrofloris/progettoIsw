var activityFormset = document.getElementById("activityFormset");
var activityButton = document.getElementById("activityButton");

activityButton.addEventListener("click", function() {
    if (activityFormset.style.display === "none") {
        activityFormset.style.display = "inline";
        activityButton.value="Hide Activity"
    } else {
        activityFormset.style.display = "none";
        activityButton.value="Show Activity"
    }
});

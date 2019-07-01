// Prepare the body tag by adding a "js-paused" class
document.body.className += " js-loading";

const courseSigning = (ev) => {
  document.getElementById('myModal').style.display = "block";
};

const closeModal = (ev) => {
  document.getElementById('myModal').style.display = "none";
};

const showPage = () => {
  // Remove the "js-paused" class
  document.body.className = document.body.className.replace("js-loading","");
};

const highlightOption = (ev) => {
  if (ev.type === 'mouseenter') {
    ev.currentTarget.classList.add('highlighted')
  } else {
    ev.currentTarget.classList.remove('highlighted');
  }
};

// Listen for when everything has loaded
window.addEventListener("load", showPage, false);
document.querySelectorAll('.option').forEach ((e) => {
  e.addEventListener("mouseenter", highlightOption, false);
  e.addEventListener("mouseleave", highlightOption, false)
});
document.querySelectorAll('.course-card__action').forEach ((e) => {
  e.addEventListener('click', courseSigning,false);
});
document.getElementById('close').addEventListener('click', closeModal ,false);

// Prepare the body tag by adding a "js-paused" class
document.body.className += " js-loading";

let prevIndex = 0,
  currentIndex = 1,
  nextIndex = 2,
  lastIndex = document.getElementById('teachers__carousel').querySelectorAll('.teachers').length - 1,
  carouselRunning = true,
  carouselRestartTimeout;

function updatePips() {
  // Update the classes on the pips depending on the current indices
  const prev = document.getElementById('teachers__carousel-pips').querySelector('.previous');
  if (prev != null)
    prev.classList.remove('previous');
  const current = document.getElementById('teachers__carousel-pips').querySelector('.current');
  if (current != null)
    current.classList.remove('current');
  const next = document.getElementById('teachers__carousel-pips').querySelector('.next');
  if (next != null)
    next.classList.remove('next');
  const allPips = document.getElementById('teachers__carousel-pips').querySelectorAll('.pip');
  allPips[prevIndex].classList.add('previous');
  allPips[currentIndex].classList.add('current');
  allPips[nextIndex].classList.add('next');
}

const setLeftClass = () => {
  // For when we want the item to appear from the left side if it's "earlier" in the list
  const allQuotes = document.getElementById('teachers__carousel').querySelectorAll('.teachers');
  // Clear any previous "left" item
  const left = document.querySelector('.teachers.left');
  if (left != null)
    left.classList.remove('left');
  if (prevIndex > 0) {
    const index = prevIndex - 1;
    allQuotes[index].classList.add('left');
  } else {
    // It's the first item, so add "left" to the last in the list
    allQuotes[allQuotes.length - 1].classList.add('left');
  }
};

const generatePips = () => {
  // Add pips to the ul element in index.html
  const listContainer = document.getElementById('teachers__carousel-pips').querySelector('ul');
  for (let i = lastIndex; i >= 0; i--) {
    const newPip = '<li class="pip"></li>';
    listContainer.insertAdjacentHTML('beforeend', newPip);
  }
  updatePips();
};

const updateCarouselPosition = () => {
  // Remove any previous, current, next classes
  const prev = document.getElementById('teachers__carousel').querySelector('.previous');
  if (prev != null)
    prev.classList.remove('previous');
  const current = document.getElementById('teachers__carousel').querySelector('.current');
  if (current != null)
    current.classList.remove('current');
  const next = document.getElementById('teachers__carousel').querySelector('.next');
  if (next != null)
    next.classList.remove('next');
  const allQuotes = document.getElementById('teachers__carousel').querySelectorAll('.teachers');
  allQuotes[prevIndex].classList.add('previous');
  allQuotes[prevIndex].addEventListener('click', showQuote,false);
  allQuotes[currentIndex].classList.add('current');
  allQuotes[nextIndex].classList.add('next');
  allQuotes[nextIndex].addEventListener('click', showQuote,false);
};

const updateState = (index) => {
  // Calculates the previous and next indices, and updates the carousel
  prevIndex = index === 0 ? lastIndex : index - 1;
  currentIndex = index;
  nextIndex = index === lastIndex ? 0 : index + 1;

  updateCarouselPosition();
  setLeftClass();
  updatePips();
};

const showQuote = (ev) => {
  const target = ev.currentTarget;
  const teachers = Array.from(document.querySelectorAll('.teachers'));
  const index = teachers.indexOf(target);
  updateState(index);

  // Since this is by click, pause the automatic movement for a few seconds
  clearTimeout(carouselRestartTimeout);
  carouselRunning = false;
  carouselRestartTimeout = setTimeout(function() {
    carouselRunning = true;
  }, 10000);
};

// Cycle automatically
const showNextQuote = () => {
  // Calculate the indices needed to show the next quote
  if (currentIndex === lastIndex) {
    currentIndex = 0;
  } else {
    currentIndex++;
  }
  updateState(currentIndex);
};

// Set the carousel working
const interval = setInterval(() => {
  if (carouselRunning) {
    showNextQuote();
  }
}, 4000);

const showFromPip = (ev) => {
  // Helper for when someone clicks a pip
  const pips = Array.from(document.querySelectorAll('.pip'));
  const pIndex = pips.indexOf(ev.currentTarget);
  updateState(pIndex);
};

// Generate pips
generatePips();
setLeftClass();

const logging = () => {
  alert('!U ARE SUCCESSFULLY LOGGED IN!');
};

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
document.getElementById('header__login-button').addEventListener('click', logging,false);
document.querySelectorAll('.course-card__action').forEach ((e) => {
  e.addEventListener('click', courseSigning,false);
});
document.getElementById('close').addEventListener('click', closeModal ,false);

document.getElementById('teachers__carousel').querySelector('.previous').addEventListener('click', showQuote,false);
document.getElementById('teachers__carousel').querySelector('.next').addEventListener('click', showQuote,false);
document.getElementById('teachers__carousel-pips').querySelectorAll('.pip').forEach((e) => {
  e.addEventListener('click', showFromPip,false);
});
document.addEventListener("visibilitychange", () => { carouselRunning = !document.hidden });
// Prepare the body tag by adding a "js-paused" class
document.body.className += " js-loading";

const navSelect = (ev) => {
  const prevActive = document.querySelector('.navbar__item.active').classList;
  document.querySelectorAll(`.lessons__item.${prevActive.item(2)}`).forEach((e) => {
    e.classList.add('hide');
  });
  prevActive.remove('active');
  const newActive = ev.currentTarget.classList;
  document.querySelectorAll(`.lessons__item.${newActive.item(2)}`).forEach((e) => {
    e.classList.remove('hide');
  });
  newActive.add('active');
};

const showContent = (ev) => {
  const childs = ev.target.childNodes;
  if (ev.type === 'mouseenter') {
    childs.item(3).style.left = "auto";
    childs.item(3).style.position = "relative";
  } else {
    childs.item(3).style.left = "-9999em";
    childs.item(3).style.position = "absolute";
  }
};

const setComment = () => {
  document.getElementById('myModal').style.display = "block";
};
const closeModal = () => {
  document.getElementById('myModal').style.display = "none";
};

document.querySelectorAll('.navbar__item').forEach ((e) => {
  e.addEventListener('click', navSelect,false);
});
document.querySelectorAll('.lessons__item').forEach ((e) => {
  e.addEventListener('mouseenter', showContent,false);
  e.addEventListener("mouseleave", showContent, false)
});
document.querySelectorAll('.lessons__comment-link').forEach ((e) => {
  e.addEventListener('click', setComment,false);
});
document.getElementById('close').addEventListener('click', closeModal ,false);
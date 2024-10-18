// Nav Bar

const baseHeader = document.querySelector("#base-header");
const toggleBtn = baseHeader.querySelector(".menu");
const toggleBtnIcon = toggleBtn.querySelector("i");
const dropDownMenu = baseHeader.querySelector(".dropdown-menu");

toggleBtn.onclick = function () {
  dropDownMenu.classList.toggle("open");
  const isOpen = dropDownMenu.classList.contains("open");
  toggleBtnIcon.classList.toggle("fa-bars", !isOpen);
  toggleBtnIcon.classList.toggle("fa-xmark", isOpen);
};

// Nav Bar Ends

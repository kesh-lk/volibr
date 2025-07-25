const userProfileBtn = document.getElementById("userProfileBtn");
const userProfilePopup = document.getElementById("profile-window");

const buttons = document.querySelectorAll(".tab-btn");
const panels = document.querySelectorAll(".tab-panel");

userProfileBtn.addEventListener('click', () => {
  userProfilePopup.style.display = "block";

  console.log(panels)
  loadUserDetails();
});

buttons.forEach(btn => {
  btn.addEventListener("click", () => {
    // Remove active class from all
    buttons.forEach(b => b.classList.remove("active"));
    panels.forEach(p => p.classList.remove("active"));

    // Add to clicked button and corresponding panel
    btn.classList.add("active");
    const tabId = btn.getAttribute("data-tab");
    document.getElementById(tabId).classList.add("active");
  });
});

function activateFirstTab() {
  buttons[0].classList.add("active");
  panels[0].classList.add("active");
}

activateFirstTab();

function loadUserDetails() {
  const nameInput = document.getElementById("details-name");
  const emailInput = document.getElementById("details-email");
  const detailsSubmit = document.getElementById("details-submit")

  fetch('/profile')
  .then(response => {
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  })
  .then(data => {
    nameInput.value = data.name;
    emailInput.value = data.email;

    nameInput.disabled = false;
    emailInput.disabled = false;
    detailsSubmit.disabled = false;
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
}


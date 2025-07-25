document.getElementById('password-form').addEventListener('submit', function(e) {
  const newPassword = document.getElementById('new-password').value;
  const confirmPassword = document.getElementById('confirm-password').value;
  const errorMsg = document.getElementById('password-error');

  if (newPassword !== confirmPassword) {
    e.preventDefault();
    errorMsg.textContent = "Passwords do not match.";
  } else {
    errorMsg.textContent = "";
  }
});


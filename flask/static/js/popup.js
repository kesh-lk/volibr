function closePopup() {
  const popups = document.getElementsByClassName("popup");

  for(const popup of popups){
    popup.style.display = "none";
  }
}

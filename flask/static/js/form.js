const container = document.getElementById('multi-select');
const dropdown = document.getElementById('dropdown-options');
const selectedTags = document.getElementById('selected-tags');

// Open dropdown
selectedTags.addEventListener('click', () => {
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
});

function updateTags() {
  const checkboxes = dropdown.querySelectorAll('input[type="checkbox"]');

  selectedTags.innerHTML = '';
  checkboxes.forEach(cb => {
    if (cb.checked) {
      const tag = document.createElement('div');
      tag.className = 'tag';
      tag.innerHTML = `${cb.value} <span>&times;</span>`;
      tag.querySelector('span').addEventListener('click', () => {
        cb.checked = false;
        updateTags();
      });
      selectedTags.appendChild(tag);
    }
  });

  // If none selected, show placeholder
  if (selectedTags.children.length === 0) {
    selectedTags.innerHTML = '';
  }
}

// Close on outside click
document.addEventListener('click', (e) => {
  if (!container.contains(e.target)) {
    dropdown.style.display = 'none';
  }
});

// Initialize
updateTags();


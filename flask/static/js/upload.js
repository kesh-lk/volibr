const selectBtn = document.getElementById('uploadBookBtn');
const fileInput = document.getElementById('fileInput');
const popup = document.getElementById('upload-window');

const canvas = document.getElementById('pdf-canvas');
const ctx = canvas.getContext('2d');

selectBtn.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (file && file.type === 'application/pdf') {

    popup.style.display = 'block';

    const fileReader = new FileReader();
    fileReader.onload = function() {
      const typedarray = new Uint8Array(this.result);

      pdfjsLib.getDocument(typedarray).promise.then(pdf => {
        pdf.getPage(1).then(page => {
          const scale = 1.5;
          const viewport = page.getViewport({ scale: scale });

          canvas.width = viewport.width;
          canvas.height = viewport.height;

          const renderContext = {
            canvasContext: ctx,
            viewport: viewport
          };
          page.render(renderContext);
        });
      }).catch(err => {
        alert("Failed to load PDF: " + err.message);
      });
    };

    fileReader.readAsArrayBuffer(file);
  } else {
    alert("Please select a valid PDF file.");
  }
});

document.getElementById("book-form").addEventListener("submit", (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const selectedFile = fileInput.files[0];

  if (selectedFile) {
      formData.append("book_file", selectedFile);
  }

  const checkboxes = form.querySelectorAll('input[name="options"]');
  const selectedOptions = [];
  checkboxes.forEach(cb => {
    if (cb.checked) selectedOptions.push(cb.value);
  });
  formData.append("genre", selectedOptions);
  
  fetch("/book/upload", {
      method: "POST",
      body: formData,
  })
  .then(res => {
    if (res.redirected) {
      window.location.href = res.url;
    }
  })
  .catch(err => {
      console.error("Error:", err);
  });
});


function populateNavGenre(genres) {
  const searchGenre = document.getElementById("search-genre")

  for (const genre of genres) {
    searchGenre.insertAdjacentHTML("beforeend", `<option>${genre}</option>`)
  }
}

function populateUploadGenre(genres) {
  const dropdownOptions = document.getElementById("dropdown-options");
  
  for (const genre of genres) {
    dropdownOptions.insertAdjacentHTML("beforeend", `<span><input type="checkbox" name="options" value="${genre}"/> ${genre}</span>`);
  }

  // Update tags
  const checkboxes = dropdownOptions.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      updateTags();
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
  fetch('/book/genre')
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then(data => {
    populateUploadGenre(data);
    populateNavGenre(data);
  })
  .catch(error => {
    console.error("Fetch error:", error);
  });
});

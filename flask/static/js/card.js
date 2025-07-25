function openBook(book_id) {
  window.open(`/book/view?id=${book_id}`)
}

function downloadBook(book_id) {
  window.open(`/book/download?id=${book_id}`, "_blank");
}

async function deleteBook(book_id, owner) {
  if (!owner) {
    alert("You are not the owner");
    return
  }

  const confirmed = confirm("Are you sure to delete?");
  if (!confirmed) return;

  try {
    const response = await fetch('/book/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: book_id })
    });
    console.log("Submitted:", response);
    
    loadBooks();
  } catch (err) {
    console.error("Error:", err);
  }
}

const searchValue = document.getElementById("search-value");
const searchGenre = document.getElementById("search-genre");

searchValue.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    loadBooks();
  }
});

searchGenre.addEventListener('change', function () {
  loadBooks();
});

async function loadBooks() {
  const grid = document.querySelector(".card-grid");

  const params = new URLSearchParams({
    search: searchValue.value,
    genre: searchGenre.value
  });

  grid.innerHTML = `
    <div class="dot-loader">
      <span></span>
      <span></span>
      <span></span>
    </div>
  `;

  fetch(`/book/search?${params}`)
      .then(response => response.json())
      .then(books => {
          grid.innerHTML = "";
          console.log(books);
          books.forEach(book => {
              const card = document.createElement("div");
              card.className = "book-card";
              card.innerHTML = `
                  <img src="/book/cover?id=${book.id}" alt="Cover">
                  <progress value="${book.page}" max="${book.page_count}"></progress>
                  
                  <div class="book-overlay">
                    <div class="book-info">
                      <h4>${book.title}</h4>
                      <p>${book.author}</p>
                    </div>
                    <div class="book-actions">
                      <button class="text-button" onclick="openBook(${book.id})">View</button>
                      <div class="v-divider"></div>
                      <button class="text-button" onclick="downloadBook(${book.id})">Download</button>
                      <div class="v-divider"></div>
                      <button class="text-button" onclick="deleteBook(${book.id}, ${book.owner})">Delete</button>
                    </div>
                  </div>
              `;
              grid.appendChild(card);
          });
      })
      .catch(error => {
          console.error("Error loading books:", error);
          grid.innerHTML = "<p>Failed to load books.</p>";
      });
}

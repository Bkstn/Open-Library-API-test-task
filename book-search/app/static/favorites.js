const FAVORITES_KEY = "favoriteBooks";

function getFavorites() {
    const savedData = localStorage.getItem(FAVORITES_KEY);

    if (!savedData) {
        return [];
    }

    try {
        return JSON.parse(savedData);
    } catch {
        return [];
    }
}

function saveFavorites(favorites) {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
}

function isFavorite(bookId) {
    const normalizedId = normalizeBookId(bookId);
    const favorites = getFavorites();

    return favorites.some(book => normalizeBookId(book.id) === normalizedId);
}

function addFavorite(book) {
    const favorites = getFavorites();

    book.id = normalizeBookId(book.id);

    if (!isFavorite(book.id)) {
        favorites.push(book);
        saveFavorites(favorites);
    }
}

function removeFavorite(bookId) {
    const normalizedId = normalizeBookId(bookId);
    const favorites = getFavorites();

    const updatedFavorites = favorites.filter(
        book => normalizeBookId(book.id) !== normalizedId
    );

    saveFavorites(updatedFavorites);
}

function buildBookFromButton(button) {
    return {
        id: normalizeBookId(button.dataset.bookId),
        title: button.dataset.bookTitle,
        authors: button.dataset.bookAuthors,
        year: button.dataset.bookYear,
        isbn: button.dataset.bookIsbn,
        cover: button.dataset.bookCover,
        url: button.dataset.bookUrl,
        detailUrl: button.dataset.bookDetailUrl
    };
}

function updateFavoriteButtons() {
    const buttons = document.querySelectorAll(".favorite-button");

    buttons.forEach(button => {
        const bookId = button.dataset.bookId;

        if (isFavorite(bookId)) {
            button.textContent = "Remove from favorites";
        } else {
            button.textContent = "Add to favorites";
        }
    });
}

function normalizeBookId(bookId) {
    if (!bookId) {
        return "";
    }

    return String(bookId).replace(/^\/+/, "");
}

function removeDuplicateFavorites() {
    const favorites = getFavorites();
    const uniqueFavorites = [];

    favorites.forEach(book => {
        const normalizedId = normalizeBookId(book.id);

        const alreadyExists = uniqueFavorites.some(
            savedBook => normalizeBookId(savedBook.id) === normalizedId
        );

        if (!alreadyExists) {
            book.id = normalizedId;
            uniqueFavorites.push(book);
        }
    });

    saveFavorites(uniqueFavorites);
}

function setupFavoriteButtons() {
    const buttons = document.querySelectorAll(".favorite-button");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const book = buildBookFromButton(button);

            if (isFavorite(book.id)) {
                removeFavorite(book.id);
            } else {
                addFavorite(book);
            }

            updateFavoriteButtons();
        });
    });
}

function escapeHTML(value) {
    if (!value) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderFavoritesPage() {
    const favoritesContainer = document.getElementById("favorites-list");

    if (!favoritesContainer) {
        return;
    }

    const favorites = getFavorites();

    if (favorites.length === 0) {
        favoritesContainer.innerHTML = "<p>No favorite books yet.</p>";
        return;
    }

    favoritesContainer.innerHTML = "";

    favorites.forEach(book => {
        const bookCard = document.createElement("div");

        bookCard.innerHTML = `
            <h3>
                ${
                    book.detailUrl
                    ? `<a href="${escapeHTML(book.detailUrl)}">${escapeHTML(book.title)}</a>`
                    : escapeHTML(book.title)
                }
            </h3>

            <p><strong>Authors:</strong> ${escapeHTML(book.authors) || "Unknown"}</p>
            <p><strong>Published:</strong> ${escapeHTML(book.year) || "Unknown"}</p>
            <p><strong>ISBN:</strong> ${escapeHTML(book.isbn) || "No ISBN found"}</p>

            ${
                book.cover
                ? `<img src="${escapeHTML(book.cover)}" width="120">`
                : ""
            }

            ${
                book.url
                ? `<p><a href="${escapeHTML(book.url)}" target="_blank">View on Open Library</a></p>`
                : ""
            }

            <button type="button" class="remove-favorite-button" data-book-id="${escapeHTML(book.id)}">
                Remove from favorites
            </button>

            <hr>
        `;

        favoritesContainer.appendChild(bookCard);
    });

    const removeButtons = document.querySelectorAll(".remove-favorite-button");

    removeButtons.forEach(button => {
        button.addEventListener("click", () => {
            removeFavorite(button.dataset.bookId);
            renderFavoritesPage();
            updateFavoriteButtons();
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    removeDuplicateFavorites();
    setupFavoriteButtons();
    updateFavoriteButtons();
    renderFavoritesPage();
});


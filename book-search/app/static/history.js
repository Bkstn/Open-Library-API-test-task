const SEARCH_HISTORY_KEY = "searchHistory";
const MAX_HISTORY_ITEMS = 10;

function getSearchHistory() {
    const savedData = localStorage.getItem(SEARCH_HISTORY_KEY);

    if (!savedData) {
        return [];
    }

    try {
        return JSON.parse(savedData);
    } catch {
        return [];
    }
}

function saveSearchHistory(history) {
    localStorage.setItem(SEARCH_HISTORY_KEY, JSON.stringify(history));
}

function addSearchQuery(query) {
    const cleanedQuery = query.trim();

    if (!cleanedQuery) {
        return;
    }

    let history = getSearchHistory();

    history = history.filter(item => item.toLowerCase() !== cleanedQuery.toLowerCase());

    history.unshift(cleanedQuery);

    if (history.length > MAX_HISTORY_ITEMS) {
        history = history.slice(0, MAX_HISTORY_ITEMS);
    }

    saveSearchHistory(history);
}

function clearSearchHistory() {
    localStorage.removeItem(SEARCH_HISTORY_KEY);
}

function setupSearchFormHistory() {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");

    if (!searchForm || !searchInput) {
        return;
    }

    searchForm.addEventListener("submit", () => {
        addSearchQuery(searchInput.value);
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

function renderHistoryPage() {
    const historyContainer = document.getElementById("history-list");
    const clearButton = document.getElementById("clear-history-button");

    if (!historyContainer) {
        return;
    }

    const history = getSearchHistory();

    if (history.length === 0) {
        historyContainer.innerHTML = "<p>No search history yet.</p>";
    } else {
        historyContainer.innerHTML = "";

        history.forEach(query => {
            const item = document.createElement("div");

            item.innerHTML = `
                <p>
                    <a href="/search?title=${encodeURIComponent(query)}">
                        ${escapeHTML(query)}
                    </a>
                </p>
            `;

            historyContainer.appendChild(item);
        });
    }

    if (clearButton) {
        clearButton.addEventListener("click", () => {
            clearSearchHistory();
            renderHistoryPage();
        });
    }
}

function setupViewedBookHistory() {
    const viewedBookData = document.getElementById("viewed-book-data");

    if (!viewedBookData) {
        return;
    }

    const bookTitle = viewedBookData.dataset.bookTitle;

    if (bookTitle) {
        addSearchQuery(bookTitle);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    setupSearchFormHistory();
    setupViewedBookHistory();
    renderHistoryPage();
});

function setupViewedBookHistory() {
    const viewedBookTitle = document.body.dataset.viewedBookTitle;

    if (!viewedBookTitle) {
        return;
    }

    addSearchQuery(viewedBookTitle);
}
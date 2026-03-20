// Functionality to toggle categories in the sidebar
function toggleCategory(categoryId) {
    const list = document.getElementById(`list-${categoryId}`);
    const caret = document.getElementById(`caret-${categoryId}`);
    if (list) {
        list.classList.toggle('hidden');
    }
    if (caret) {
        caret.classList.toggle('open');
    }
}

// Functionality to toggle the entire sidebar on mobile
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Search filtering functionality
function filterUtilities() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();

    // Filter Sidebar Links
    const sidebarLinks = document.querySelectorAll('.util-link');
    sidebarLinks.forEach(link => {
        const name = link.getAttribute('data-name');
        const tags = link.getAttribute('data-tags');
        if (name.includes(filter) || tags.includes(filter)) {
            link.style.display = "block";
        } else {
            link.style.display = "none";
        }
    });

    // Filter Dashboard Cards if present
    const cards = document.querySelectorAll('.util-card');
    let cardsVisible = 0;

    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        const tags = card.getAttribute('data-tags');
        if (name.includes(filter) || tags.includes(filter)) {
            card.style.display = "flex";
            cardsVisible++;
        } else {
            card.style.display = "none";
        }
    });

    // Show no results message if dashboard view
    const noResults = document.getElementById('no-results');
    if (noResults && cards.length > 0) {
        if (cardsVisible === 0) {
            noResults.style.display = "block";
        } else {
            noResults.style.display = "none";
        }
    }
}

// Theme toggle logic
function toggleTheme() {
    const root = document.documentElement;
    if (root.classList.contains('light-theme')) {
        root.classList.remove('light-theme');
        localStorage.setItem('theme', 'dark');
    } else {
        root.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
    }
}

// Update budget value dynamically
function updateBudgetValue(value) {
    document.getElementById('budgetValue').textContent = value;
}

// Apply filter based on selected bed type and budget
function applyFilter() {
    // Get the selected bed types
    const bedTypes = [];
    if (document.getElementById('priceSingleBed').checked) bedTypes.push('single');
    if (document.getElementById('priceShared2Beds').checked) bedTypes.push('double');
    if (document.getElementById('priceShared3Beds').checked) bedTypes.push('triple');

    // **Force "single" as default if no checkboxes are checked**
    if (bedTypes.length === 0) {
        bedTypes.push('single'); // Default to Single Bed Filter
    }

    // Get selected budget
    const budget = document.getElementById('budgetRange').value;

    // Get current URL and add query parameters
    let currentUrl = new URL(window.location.href);

    // Add selected bed types as a comma-separated string
    currentUrl.searchParams.set('bed_types', bedTypes.join(','));
    
    // Add selected budget
    currentUrl.searchParams.set('budget', budget);

    // Redirect to the updated URL with applied filters
    window.location.href = currentUrl.toString();
}


document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    dropdownToggle.addEventListener('click', function (event) {
    event.stopPropagation();
    dropdownMenu.classList.toggle('show');
    });

    dropdownMenu.addEventListener('click', function (event) {
    event.stopPropagation(); // Prevent menu clicks from closing it
    });

    document.addEventListener('click', function (event) {
    if (!dropdownMenu.contains(event.target) && !dropdownToggle.contains(event.target)) {
        dropdownMenu.classList.remove('show');
    }
    });
});



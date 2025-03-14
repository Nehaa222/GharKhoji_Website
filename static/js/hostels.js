function updateBudgetValue(value) {
document.getElementById('budgetValue').textContent = value;
}
function applyFilter() {
let budget = document.getElementById('budgetRange').value;
let currentUrl = new URL(window.location.href);
currentUrl.searchParams.set('budget', budget);
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



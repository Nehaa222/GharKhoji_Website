    function enableField(icon) {
        const input = icon.previousElementSibling;
        input.removeAttribute("readonly");
        input.focus();
    }
    
    // Cancel button: Reset fields to original values
    function disableAllFields() {
        document.querySelectorAll(".form-input").forEach(input => {
            input.setAttribute("readonly", "readonly");
            input.value = input.defaultValue; // Reset to original value
        });
    }

    // Handle form submission: Ensure no readonly inputs before submission
    document.getElementById("profile-form").addEventListener("submit", function(event) {
        // Make sure all inputs are not readonly before submitting
        document.querySelectorAll(".form-input").forEach(input => {
            input.removeAttribute("readonly");
        });
    });

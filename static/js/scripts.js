document.addEventListener("DOMContentLoaded", function() {
    const diagnosticTests = JSON.parse(document.getElementById('diagnostic-tests-data').textContent);

    const testCategorySelect = document.getElementById('test_category');
    const diagnosticTestInput = document.getElementById('diagnostic_test');
    const diagnosticTestDatalist = document.getElementById('diagnostic_tests');
    const backButton = document.getElementById('backButton');

    let currentTests = [];

    function updateDiagnosticTests() {
        const category = testCategorySelect.value;
        currentTests = diagnosticTests[category] || [];
        
        // Clear the diagnostic test input field
        diagnosticTestInput.value = '';
        
        populateDiagnosticTests();
    }

    function populateDiagnosticTests() {
        // Clear previous options
        diagnosticTestDatalist.innerHTML = '';

        // Populate new options
        currentTests.forEach(function(test) {
            const option = document.createElement('option');
            option.value = test;
            diagnosticTestDatalist.appendChild(option);
        });
    }

    function filterTests() {
        const searchTerm = diagnosticTestInput.value.toLowerCase();
        
        // Clear previous options
        diagnosticTestDatalist.innerHTML = '';

        // Filter and populate new options based on search term
        currentTests.forEach(function(test) {
            if (test.toLowerCase().includes(searchTerm)) {
                const option = document.createElement('option');
                option.value = test;
                diagnosticTestDatalist.appendChild(option);
            }
        });

        // If search term is cleared, show all tests again
        if (searchTerm === '') {
            populateDiagnosticTests();
        }
    }

    function resetForm() {
        testCategorySelect.selectedIndex = 0;
        diagnosticTestInput.value = '';
        diagnosticTestDatalist.innerHTML = '';
        currentTests = [];
    }

    // Event listener for back button
    if (backButton) {
        backButton.addEventListener('click', function(e) {
            e.preventDefault();
            resetForm();
            // Use window.location.reload to refresh the page
            window.location.reload();
        });
    }

    // Event listener for category change
    if (testCategorySelect) {
        testCategorySelect.addEventListener('change', updateDiagnosticTests);
    }

    // Event listener for input changes in diagnostic test field
    if (diagnosticTestInput) {
        diagnosticTestInput.addEventListener('input', filterTests);
    }

    // Initialize the datalist on page load if a category is pre-selected
    if (testCategorySelect && testCategorySelect.value) {
        updateDiagnosticTests();
    }
});

////Upload Image Logic
document.getElementById('uploadImages').addEventListener('click', function () {
    document.getElementById('HostelImages').click();
    });

    let selectedFiles = []; // Store selected files

    document.getElementById('HostelImages').addEventListener('change', function (event) {
        const files = event.target.files;
        const previewContainer = document.getElementById('imagePreview');
        
        // Convert FileList to array and store in selectedFiles
        selectedFiles = Array.from(files);

        previewContainer.innerHTML = ''; // Clear previous previews
        
        selectedFiles.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imageItem = document.createElement('div');
                imageItem.classList.add('image-item');
                imageItem.innerHTML = `
                    <img src="${e.target.result}" alt="Uploaded Image">
                    <button type="button" class="remove-btn" data-index="${index}">&times;</button>
                `;
                previewContainer.appendChild(imageItem);
            };
            reader.readAsDataURL(file);
        });

        updateFileCountMessage();
    });

    document.getElementById('imagePreview').addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-btn')) {
            const index = parseInt(event.target.getAttribute('data-index'));

            // Remove the file from the selectedFiles array
            selectedFiles.splice(index, 1);

            // Update the FileList in the input field
            updateFileInput();

            // Refresh the image preview
            refreshPreview();
        }
    });

    function updateFileInput() {
        const dataTransfer = new DataTransfer(); // Create a new FileList
        selectedFiles.forEach(file => dataTransfer.items.add(file));
        document.getElementById('HostelImages').files = dataTransfer.files;
    }

    function refreshPreview() {
        const previewContainer = document.getElementById('imagePreview');
        previewContainer.innerHTML = '';

        selectedFiles.forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imageItem = document.createElement('div');
                imageItem.classList.add('image-item');
                imageItem.innerHTML = `
                    <img src="${e.target.result}" alt="Uploaded Image">
                    <button type="button" class="remove-btn" data-index="${index}">&times;</button>
                `;
                previewContainer.appendChild(imageItem);
            };
            reader.readAsDataURL(file);
        });

        updateFileCountMessage();
    }

    function updateFileCountMessage() {
        const message = document.getElementById('fileCountMessage');
        message.textContent = `Selected Images: ${selectedFiles.length}`;
    }
    ////Upload Image Logic End
    //For Map
    var map = L.map('map').setView([27.7102, 85.3240], 15);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // Remove default attribution
        map.attributionControl.setPrefix(false);

        var marker;

        map.on('click', function(e) {
            if (marker) {
                map.removeLayer(marker);
            }
            marker = L.marker([e.latlng.lat, e.latlng.lng]).addTo(map);
            
            document.getElementById('latitude').value = e.latlng.lat;
            document.getElementById('longitude').value = e.latlng.lng;
        });
        //Clean input field on page reload
        window.onload = function () {
        document.getElementById("latitude").value = "";
        document.getElementById("longitude").value = "";
        };
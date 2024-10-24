function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;

                fetch(`https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`)
                    .then(response => response.json())
                    .then(data => {
                        const city = data.address.city || data.address.town || data.address.village;
                        document.getElementById('city').value = city || "Unknown City";
                    })
                    .catch(error => {
                        console.error('Error retrieving city:', error);
                        alert("Unable to retrieve city information. Please enter your city manually.");
                    });
                },
            function(error) {
                console.error('Error occurred. Error code: ' + error.code);
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        alert("User denied the request for Geolocation.");
                        break;
                        case error.POSITION_UNAVAILABLE:
                            alert("Location information is unavailable.");
                            break;
                            case error.TIMEOUT:
                                alert("The request to get user location timed out.");
                                break;
                            case error.UNKNOWN_ERROR:
                                alert("An unknown error occurred.");
                                break;
                }
            }
            );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function filterUserList() {
    const searchInput = document.querySelector('input[name="username"]');
    const userList = document.getElementById('user-list');
    const userItems = userList.querySelectorAll('.user-item');

    searchInput.addEventListener('input', function () {
        const searchTerm = searchInput.value.toLowerCase();
        userItems.forEach(function (item) {
            const username = item.querySelector('.user-username').textContent.toLowerCase();
            if (username.includes(searchTerm)) {
                item.style.display = '';  // Show the item
            } else {
                item.style.display = 'none';  // Hide the item
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', filterUserList);


// app.js

function initializeProfileImageUpload() {
    // Preview the selected image before upload
    document.getElementById('profile_image').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('profile-image-preview').src = e.target.result; // Update the image source
            }
            reader.readAsDataURL(file);
        }
    });

    // Trigger file input when the upload button is clicked
    document.getElementById('upload-button').addEventListener('click', function() {
        document.getElementById('profile_image').click();
    });
}

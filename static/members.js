document.addEventListener("DOMContentLoaded", function() {
    const requestCount = document.getElementById('request-count');
    const addMemberButton = document.getElementById('add-member');
    const lightbox = document.getElementById('lightbox');
    const closeLightboxButton = document.getElementById('close-lightbox');
    const addMemberForm = document.getElementById('add-member-form');
    var deleteButtons = document.querySelectorAll('.delete-button');
    
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var memberId = this.getAttribute('data-member-id');
            deleteMember(memberId);
        });
    });
    
    addMemberButton.addEventListener('click', function() {
        lightbox.classList.add('active');
    });

    closeLightboxButton.addEventListener('click', function() {
        lightbox.classList.remove('active');
    });

    addMemberForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        // Gather form data
        const formData = new FormData(addMemberForm);

        // Convert FormData to JSON object
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        // Send form data to Flask route
        fetch('/add_member', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Print response from Flask function
            // You can add additional logic here to handle the response, such as displaying a success message
            lightbox.classList.remove('active'); // Close the lightbox after submitting
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            // You can add error handling logic here, such as displaying an error message
        });
    });

    

    function updateRequestCount() {
        fetch('/requests/count')
            .then(response => response.json())
            .then(data => {
                requestCount.textContent = data.count;
            });
    }

    setInterval(updateRequestCount, 10000);
    updateRequestCount();
});

function closeDetails() {
    document.getElementById('event-details').classList.add('hidden');
}

function deleteMember(memberId) {
    // Make an AJAX request to delete member
    console.log(memberId);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/delete_member', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Reload the page upon successful deletion
            location.reload();
        } else {
            console.log('Error deleting member');
        }
    };
    xhr.send(JSON.stringify({member_id: memberId}));
}

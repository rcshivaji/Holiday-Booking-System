document.addEventListener("DOMContentLoaded", function() {
    let currentMonth = new Date().getMonth();
    let currentYear = new Date().getFullYear();
    
    const calendar = document.getElementById('calendar');
    const eventDetails = document.getElementById('event-details');
    const eventName = document.getElementById('event-name');
    const eventTag = document.getElementById('event-tag');
    const eventDescription = document.getElementById('event-description');
    const monthSelect = document.getElementById('month-select');
    const yearSelect = document.getElementById('year-select');
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const goToDateButton = document.getElementById('go-to-date');
    const requestCount = document.getElementById('request-count');
    const requestHolidayButton = document.getElementById('request-holiday');
    const lightbox = document.getElementById('lightbox');
    const closeLightboxButton = document.getElementById('close-lightbox');
    const addMemberForm = document.getElementById('add-member-form');

    requestHolidayButton.addEventListener('click', function() {
        lightbox.classList.add('active');
    });
    
    closeLightboxButton.addEventListener('click', function() {
        lightbox.classList.remove('active');
    });

});

function closeDetails() {
    document.getElementById('event-details').classList.add('hidden');
}

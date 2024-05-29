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

    monthSelect.value = currentMonth;
    yearSelect.value = currentYear;

    requestHolidayButton.addEventListener('click', function() {
        lightbox.classList.add('active');
    });
    
    closeLightboxButton.addEventListener('click', function() {
        lightbox.classList.remove('active');
    });

    

    function loadEvents() {
        fetch(`/events?month=${currentMonth + 1}&year=${currentYear}`)
            .then(response => response.json())
            .then(events => {
                renderCalendar(events);
            });
    }

    function renderCalendar(events) {
        calendar.innerHTML = `
            <div class="day-header">Sunday</div>
            <div class="day-header">Monday</div>
            <div class="day-header">Tuesday</div>
            <div class="day-header">Wednesday</div>
            <div class="day-header">Thursday</div>
            <div class="day-header">Friday</div>
            <div class="day-header">Saturday</div>
        `;

        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

        for (let i = 0; i < firstDayOfMonth; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.classList.add('day');
            calendar.appendChild(emptyDiv);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('day');

            const date = new Date(currentYear, currentMonth, day);
            if (date.getDay() === 6) {
                dayDiv.classList.add('saturday');
            } else if (date.getDay() === 0) {
                dayDiv.classList.add('sunday');
            }

            dayDiv.textContent = day;

            events.forEach(event => {
                const eventStart = new Date(event.start);
                const eventEnd = new Date(event.end);
                const eventDay = new Date(currentYear, currentMonth, day);

                eventStart.setHours(0, 0, 0, 0);
                eventEnd.setHours(23, 59, 59, 999);
                eventDay.setHours(0, 0, 0, 0);

                if (eventDay >= eventStart && eventDay <= eventEnd) {
                    const eventDiv = document.createElement('div');
                    eventDiv.classList.add('event');
                    eventDiv.style.backgroundColor = event.color;
                    eventDiv.textContent = event.tag;
                    eventDiv.addEventListener('click', () => {
                        eventName.textContent = event.name;
                        eventTag.textContent = event.tag;
                        eventDescription.textContent = event.description;
                        eventDetails.classList.remove('hidden');
                    });
                    dayDiv.appendChild(eventDiv);
                }
            });

            calendar.appendChild(dayDiv);
        }
    }

    prevMonthButton.addEventListener('click', () => {
        if (currentMonth === 0) {
            currentMonth = 11;
            currentYear--;
        } else {
            currentMonth--;
        }
        loadEvents();
    });

    nextMonthButton.addEventListener('click', () => {
        if (currentMonth === 11) {
            currentMonth = 0;
            currentYear++;
        } else {
            currentMonth++;
        }
        loadEvents();
    });

    goToDateButton.addEventListener('click', () => {
        currentMonth = parseInt(monthSelect.value);
        currentYear = parseInt(yearSelect.value);
        loadEvents();
    });

    function updateRequestCount() {
        fetch('/requests/count')
            .then(response => response.json())
            .then(data => {
                requestCount.textContent = data.count;
            });
    }

    setInterval(updateRequestCount, 10000);

    loadEvents();
    updateRequestCount();
});

function closeDetails() {
    document.getElementById('event-details').classList.add('hidden');
}

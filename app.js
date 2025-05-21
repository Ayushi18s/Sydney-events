// Store the current event link
let currentEventLink = '';

// Fetch events from the backend
async function fetchEvents() {
    try {
        const response = await fetch('http://localhost:5000/events');
        const events = await response.json();
        displayEvents(events);
    } catch (error) {
        console.error('Error fetching events:', error);
        document.getElementById('events-container').innerHTML = 
            '<p class="error-message">Unable to load events. Please try again later.</p>';
    }
}

// Display events on the page
function displayEvents(events) {
    const container = document.getElementById('events-container');
    container.innerHTML = '';
    
    if (events.length === 0) {
        container.innerHTML = '<p class="no-events">No events found.</p>';
        return;
    }
    
    events.forEach(event => {
        const card = document.createElement('div');
        card.className = 'event-card';
        
        card.innerHTML = `
            <h3>${event.name}</h3>
            <p><strong>Date:</strong> ${event.date}</p>
            <p><strong>Venue:</strong> ${event.venue}</p>
            <p>${event.description || ''}</p>
            <button class="ticket-button" data-link="${event.ticket_link}">Get Tickets</button>
        `;
        
        container.appendChild(card);
    });
    
    // Add event listeners to all ticket buttons
    document.querySelectorAll('.ticket-button').forEach(button => {
        button.addEventListener('click', function() {
            openEmailModal(this.getAttribute('data-link'));
        });
    });
}

// Open the email modal
function openEmailModal(ticketLink) {
    currentEventLink = ticketLink;
    document.getElementById('email-modal').style.display = 'block';
    document.getElementById('email-input').focus();
}

// Set up event listeners when page loads
function setupEventListeners() {
    // Close the modal when clicking the X
    document.querySelector('.close-button').addEventListener('click', function() {
        document.getElementById('email-modal').style.display = 'none';
    });
    
    // Close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('email-modal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Submit email and redirect
    document.getElementById('submit-email').addEventListener('click', submitEmail);
    
    // Also submit when pressing Enter in the email input
    document.getElementById('email-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            submitEmail();
        }
    });
}

// Submit email and redirect to ticket page
async function submitEmail() {
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value;
    
    if (!email || !email.includes('@')) {
        alert('Please enter a valid email address');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5000/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Redirect to ticket page
            window.location.href = currentEventLink;
        } else {
            alert('There was an error. Please try again.');
        }
    } catch (error) {
        console.error('Error submitting email:', error);
        alert('There was an error connecting to the server. Please try again.');
    }
}

// Initialize when page loads
window.addEventListener('load', function() {
    setupEventListeners();
    fetchEvents();
});
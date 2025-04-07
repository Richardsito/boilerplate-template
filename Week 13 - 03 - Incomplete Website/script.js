// Initial slots available
let slotsAvailable = 10;
let currentDayIndex = 0;
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
let selectedSlot = null;

// Generate time slots from 7am to 11pm with 3-hour intervals for each day of the week (excluding Sunday)
const generateTimeSlots = () => {
    const slots = {};
    days.forEach(day => {
        slots[day] = [];
        for (let hour = 7; hour <= 23; hour += 3) {
            slots[day].push({ time: `${hour}:00`, available: true });
        }
    });
    return slots;
};

const timeSlots = generateTimeSlots();

// When the DOM loads, set the slots available
document.addEventListener("DOMContentLoaded", () => {
    const slotsContainer = document.getElementById("slotsContainer");
    const currentDayElement = document.getElementById("currentDay");

    const updateSlotsDisplay = () => {
        slotsContainer.innerHTML = '';
        const currentDay = days[currentDayIndex];
        currentDayElement.textContent = currentDay;

        timeSlots[currentDay].forEach(slot => {
            const slotElement = document.createElement("div");
            slotElement.classList.add("slot");
            slotElement.textContent = slot.time;
            slotElement.dataset.time = slot.time;
            slotElement.dataset.available = slot.available;
            if (!slot.available) {
                slotElement.classList.add("unavailable");
            } else {
                slotElement.addEventListener("click", () => {
                    if (selectedSlot) {
                        selectedSlot.classList.remove("selected");
                    }
                    selectedSlot = slotElement;
                    slotElement.classList.add("selected");
                });
            }
            slotsContainer.appendChild(slotElement);
        });
    };

    document.getElementById("prevDay").addEventListener("click", () => {
        currentDayIndex = (currentDayIndex - 1 + days.length) % days.length;
        updateSlotsDisplay();
    });

    document.getElementById("nextDay").addEventListener("click", () => {
        currentDayIndex = (currentDayIndex + 1) % days.length;
        updateSlotsDisplay();
    });

    updateSlotsDisplay();
});

// Handle form submission
document.getElementById("bookingForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Retrieve form values
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    if (selectedSlot) {
        const currentDay = days[currentDayIndex];
        const time = selectedSlot.dataset.time;

        // Display confirmation message
        const confirmationMessage = document.getElementById("confirmationMessage");
        if (confirmationMessage) {
            confirmationMessage.textContent = `Thank you, ${name}. Your booking for ${currentDay} at ${time} has been confirmed. A confirmation email will be sent to ${email}.`;
        }

        // Mark the slot as unavailable
        const slot = timeSlots[currentDay].find(slot => slot.time === time);
        slot.available = false;
        selectedSlot.classList.add("unavailable");
        selectedSlot.classList.remove("selected");
        selectedSlot = null;

        // Reduce slots available
        if (slotsAvailable > 0) {
            slotsAvailable--;
        }

        // Update the slots available display
        updateSlotsDisplay();
    } else {
        alert("Please select a slot to book.");
    }
});

const updateSlotsDisplay = () => {
    const slotsElement = document.getElementById("slotsAvailable");
    const bookingButton = document.querySelector("button[type='submit']");
    const slotElements = document.querySelectorAll(".slot");

    if (slotsElement) {
        if (slotsAvailable > 0) {
            slotsElement.textContent = `Available Slots: ${slotsAvailable}`;
            slotElements.forEach(slot => {
                if (slot.dataset.available === "true") {
                    slot.classList.remove("unavailable");
                }
            });
        } else {
            slotsElement.textContent = "No slots available";
            bookingButton.disabled = true;
            bookingButton.style.backgroundColor = "gray";
            slotElements.forEach(slot => slot.classList.add("unavailable"));
        }
    }
};
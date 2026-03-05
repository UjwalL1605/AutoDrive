document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Flatpickr Date Pickers
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');

    if (startDateInput && endDateInput) {
        // Common options
        const options = {
            dateFormat: "Y-m-d",
            minDate: "today",
            altInput: true,
            altFormat: "F j, Y",
        };

        // Start Date picker
        const fpStart = flatpickr(startDateInput, {
            ...options,
            onChange: function(selectedDates, dateStr, instance) {
                // Set minDate for end date picker
                fpEnd.set('minDate', dateStr);
                updatePrice();
            },
        });

        // End Date picker
        const fpEnd = flatpickr(endDateInput, {
            ...options,
            onChange: function(selectedDates, dateStr, instance) {
                updatePrice();
            },
        });
    }

    // Dynamic Price Calculator
    const calculator = document.getElementById('booking-calculator');
    if (calculator) {
        const driverToggle = document.getElementById('driver_toggle');
        
        // Add event listeners
        startDateInput.addEventListener('change', updatePrice);
        endDateInput.addEventListener('change', updatePrice);
        driverToggle.addEventListener('change', updatePrice);

        // Get prices from data attributes
        const basePricePerDay = parseInt(calculator.dataset.basePrice, 10);
        const driverFeePerDay = parseInt(calculator.dataset.driverFee, 10);

        // Get output elements
        const numDaysEl = document.getElementById('num_days');
        const basePriceEl = document.getElementById('base_price');
        const driverFeeSummary = document.getElementById('driver_fee_summary');
        const driverFeeTotalEl = document.getElementById('driver_fee_total');
        const totalPriceEl = document.getElementById('total_price');

        function updatePrice() {
            const start = new Date(startDateInput.value);
            const end = new Date(endDateInput.value);
            const driverAdded = driverToggle.checked;

            if (isNaN(start) || isNaN(end) || start > end) {
                // Invalid date range
                numDaysEl.textContent = '-- days';
                basePriceEl.textContent = '₹--';
                driverFeeSummary.classList.add('hidden');
                totalPriceEl.textContent = '₹--';
                return;
            }

            // Calculate number of days (inclusive)
            const timeDiff = end.getTime() - start.getTime();
            let numDays = Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;

            if (numDays <= 0) numDays = 1; // Minimum 1 day rental

            // Calculate prices
            const baseTotal = numDays * basePricePerDay;
            const driverTotal = numDays * driverFeePerDay;
            let finalTotal = baseTotal;

            // Update DOM
            numDaysEl.textContent = `${numDays} day${numDays > 1 ? 's' : ''}`;
            basePriceEl.textContent = `₹${baseTotal.toLocaleString('en-IN')}`;

            if (driverAdded) {
                finalTotal += driverTotal;
                driverFeeTotalEl.textContent = `₹${driverTotal.toLocaleString('en-IN')}`;
                driverFeeSummary.classList.remove('hidden');
            } else {
                driverFeeSummary.classList.add('hidden');
            }

            totalPriceEl.textContent = `₹${finalTotal.toLocaleString('en-IN')}`;
        }
    }
});
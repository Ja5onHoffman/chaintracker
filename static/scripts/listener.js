$(document).ready(function() {
  $('#bikeModal').on('shown.bs.modal', function() {
      // Make a Fetch request to retrieve the form data
      fetch('/get_bikes')
      .then(response => response.json())
      .then(data => {
          // Populate the form with the retrieved data
          populateForm(data);
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });

  function populateForm(data) {
      // Populate the form with the retrieved data
      const form = document.querySelector('#bikeModal form');
      form.innerHTML = ''; // Clear existing form content

      for (const bike of data.bikes) {
          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.name = 'selected_bikes';
          checkbox.value = bike.id;

          const label = document.createElement('label');
          label.textContent = bike.name;

          const div = document.createElement('div');
          div.className = 'form-check';
          div.appendChild(checkbox);
          div.appendChild(label);

          form.appendChild(div);
      }

      // Add the submit button back to the form after populating the bikes
      const submitButton = document.createElement('button');
      submitButton.type = 'submit';
      submitButton.className = 'btn btn-primary';
      submitButton.textContent = 'Add Bikes';

      form.appendChild(submitButton);
  }
});

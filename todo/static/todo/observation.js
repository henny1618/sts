// Name: Nichols Hennigar
// Class: CSCI E-33a
// Assigment: Final Project


document.addEventListener('DOMContentLoaded', function() {

    // Edit button
    const editButton = document.querySelector('#observation-edit-button');
    editButton.addEventListener('click', () => {
        const id = editButton.dataset.id;
        edit_observation(id)
    });

    // Delete button
    const deleteButton = document.querySelector('#observation-delete-button');
    deleteButton.addEventListener('click', () => {
        const id = deleteButton.dataset.id;
        delete_observation(id)
    });

    // Default view
    document.querySelector('#observation-div').style.display = 'block';
    document.querySelector('#observation-button-div').style.display = 'block';
    document.querySelector('#observation-confirmation-div').style.display = 'none';
    document.querySelector('#observation-edit-div').style.display = 'none';

});

function edit_observation(id) {
    document.querySelector('#observation-div').style.display = 'none';
    document.querySelector('#observation-button-div').style.display = 'none';
    document.querySelector('#observation-confirmation-div').style.display = 'none';
    document.querySelector('#observation-edit-div').style.display = 'block';

    // Update button
    document.querySelector('#observation-update-button').addEventListener('click', () => {

        let type = document.querySelector('#id_type').value;
        let component = document.querySelector('#id_component').value;
        let status = document.querySelector('#id_status').value;
        let procedure = document.querySelector('#id_procedure').value;

        fetch(`/edit_observation/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                type: type,
                component: component,
                status: status,
                procedure: procedure
            })
        })
        .then(response => response.json())
        .then(result => {
            // Display error message if we have one
            if (result.error) {
                const error = result.error;
                const errorDiv = document.querySelector('#api-error');
                errorDiv.innerHTML = error;
                errorDiv.style.display = 'block';
            } else {
                document.querySelector('#observation-div').style.display = 'block';
                document.querySelector('#observation-button-div').style.display = 'block';
                document.querySelector('#observation-confirmation-div').style.display = 'none';
                document.querySelector('#observation-edit-div').style.display = 'none';
    
                // Reloading page so it updates 
                location.reload();
            }
        })
        .catch(error => {
            console.log('Error:', error)
        });
        
    });
}

function delete_observation(id) {
    document.querySelector('#observation-div').style.display = 'none';
    document.querySelector('#observation-button-div').style.display = 'none';
    document.querySelector('#observation-confirmation-div').style.display = 'block';
    document.querySelector('#observation-edit-div').style.display = 'none';

    document.querySelector('#observation-delete-confirmation-button').addEventListener('click', () => {
        fetch(`/delete_observation/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                id: id
            })
        })
        .then(response => response.json())
        .then(result => {
            // Display error message if we have one
            if (result.error) {
                const error = result.error;
                const errorDiv = document.querySelector('#api-error');
                errorDiv.innerHTML = error;
                errorDiv.style.display = 'block';
            } else {
                document.querySelector('#observation-div').style.display = 'block';
                document.querySelector('#observation-button-div').style.display = 'block';
                document.querySelector('#observation-confirmation-div').style.display = 'none';
                document.querySelector('#observation-edit-div').style.display = 'none';

                // Redirect away from page that no longer exists
                window.location.replace("http://127.0.0.1:8000");
            }
        })
        .catch(error => {
            console.log('Error:', error)
        });
    });
}
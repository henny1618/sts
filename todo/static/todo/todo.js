// Name: Nichols Hennigar
// Class: CSCI E-33a
// Assigment: Final Project

document.addEventListener('DOMContentLoaded', function() {

    // Edit button
    const editButton = document.querySelector('#todo-edit-button');
    editButton.addEventListener('click', () => {
        const todo = editButton.dataset.todo;
        const id = editButton.dataset.id;
        edit_todo(id)
    });

    // Delete button
    const deleteButton = document.querySelector('#todo-delete-button');
    deleteButton.addEventListener('click', () => {
        const id = deleteButton.dataset.id;
        delete_todo(id)
    });

    // Default view
    document.querySelector('#todo-div').style.display = 'block';
    document.querySelector('#todo-button-div').style.display = 'block';
    document.querySelector('#todo-confirmation-div').style.display = 'none';
    document.querySelector('#todo-edit-div').style.display = 'none';

});

function edit_todo(id) {
    document.querySelector('#todo-div').style.display = 'none';
    document.querySelector('#todo-button-div').style.display = 'none';
    document.querySelector('#todo-confirmation-div').style.display = 'none';
    document.querySelector('#todo-edit-div').style.display = 'block';

    // Update button
    document.querySelector('#todo-update-button').addEventListener('click', () => {

        let comment = document.querySelector('#id_comment').value;
        let peace = document.querySelector('#id_peace').value;
        let rescue = document.querySelector('#id_rescue').value;
        let observation = document.querySelector('#id_observation').value;
        let title = document.querySelector('#id_title').value;

        fetch(`/edit_todo/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                title: title,
                comment: comment,
                peace: peace,
                rescue: rescue,
                observation: observation
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
                document.querySelector('#todo-div').style.display = 'block';
                document.querySelector('#todo-button-div').style.display = 'block';
                document.querySelector('#todo-confirmation-div').style.display = 'none';
                document.querySelector('#todo-edit-div').style.display = 'none';

                // Reloading page so it updates 
                location.reload();
            }
        })
        .catch(error => {
            console.log('Error:', error)
        });
        
    });
}

function delete_todo(id) {
    document.querySelector('#todo-div').style.display = 'none';
    document.querySelector('#todo-button-div').style.display = 'none';
    document.querySelector('#todo-confirmation-div').style.display = 'block';
    document.querySelector('#todo-edit-div').style.display = 'none';

    document.querySelector('#todo-delete-confirmation-button').addEventListener('click', () => {
        fetch(`/delete_todo/${id}`, {
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
                document.querySelector('#todo-div').style.display = 'block';
                document.querySelector('#todo-button-div').style.display = 'block';
                document.querySelector('#todo-confirmation-div').style.display = 'none';
                document.querySelector('#todo-edit-div').style.display = 'none';

                // Redirect away from page that no longer exists
                window.location.replace("http://127.0.0.1:8000");
            }
        })
        .catch(error => {
            console.log('Error:', error)
        });
    });
}
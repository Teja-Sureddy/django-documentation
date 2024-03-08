// Clear all Filters
function clearAll() {
    var url = window.location.href.split('?')[0];
    window.location.href = url;
}

// Delete
$('#deleteModel').on('show.bs.modal', function (event) {
    $('#delete-error-msg').text('')
    var button = $(event.relatedTarget);
    var pk = button.data('pk');
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    var deleteButton = $('#deleteButton');

    deleteButton.attr('onclick', 'deleteItem(' + pk + ', "' + csrfToken + '");');
});

function deleteItem(pk, csrfToken) {
    $.ajax({
        url: 'delete/' + pk + '/',
        type: 'DELETE',
        headers: {'X-CSRFToken': csrfToken},
        success: function (response) {
            location.reload();
        },
        error: function (error) {
            console.error('Error deleting item:', error);
            $('#delete-error-msg').text('Error deleting item.')
        }
    });
}

// Message
function hideMessages() {
    var messages = $('.messages');
    var messagesClose = $('#messages-close');
    if (messages.length) {
        messagesClose.on('click', function () {
            messages.remove()
        });
    }
}

hideMessages()

// Custom multi select
$(document).ready(function() {
    $('.select2').select2( { placeholder: "Select", maximumSelectionSize: 100  } );
})

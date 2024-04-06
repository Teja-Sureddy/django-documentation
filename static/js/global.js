document.body.addEventListener('htmx:load', function() {
    run_select2()
    hideMessages()
})

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
function run_select2(){
    $('.select2').select2( { placeholder: "Select", maximumSelectionSize: 100 });
    $('.select2').on("select2:select", function (e) { dispatchSelect() });
    $('.select2').on("select2:unselect", function (e) { dispatchSelect() });
}

function dispatchSelect(){
    var element = document.getElementById('id_gender');
    element.dispatchEvent(new Event('change'));
}

// Dont close the dropdown when clicked inside the navbarDropdown
function dropdownItemStopProp() {
  document.querySelectorAll('.dropdown-menu').forEach(function (dropdownMenu) {
    if (dropdownMenu.getAttribute('aria-labelledby') == 'navbarDropdown') {
      dropdownMenu.addEventListener('click', (event) => {
        if (event.delegateTarget) event.stopPropagation();
      })
    }
  });
}
dropdownItemStopProp()

// Close the current dropdown if the other dropdown is opened
function onDropdownShow() {
  var dropdownIds = ['#navbarPdfDropdown', '#navbarBgTaskDropdown'];
  dropdownIds.forEach((dropdownId) => {
    $(dropdownId).on('show.bs.dropdown', () => {
      dropdownIds.forEach((otherDropdownId) => {
        if (otherDropdownId !== dropdownId) $(otherDropdownId).dropdown('hide')
      });
    });
  });
}
onDropdownShow()

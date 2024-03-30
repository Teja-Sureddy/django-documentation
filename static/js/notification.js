function socketInit() {
    const notificationSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/notification/'
    );

    notificationSocket.onopen = function (event) { console.log('Connected to ws.') }
    notificationSocket.onmessage = function (e) { prependNotifications(e) }
    notificationSocket.onclose = function (e) { console.log(e) }
}
socketInit()

function prependNotifications(e) {
    const data = JSON.parse(e.data);
    var notificationsNa = document.querySelector('.notifications-na');
    if (notificationsNa) notificationsNa.remove();

    let unread_element = ''
    if (data.public) unread_element = '<span class="bg-primary-light rounded px-1">Public</span>'
    else if (data.unread && !data.public) {
        unread_element = '<i class="bi bi-dot"></i>'
        updateNotificationBadge(1)
    }

    var listItem = document.createElement("li");
    data.title = data.title.replace(/'/g, "").replace(/"/g, "")
    data.description = data.description.replace(/'/g, "").replace(/"/g, "")
    listItem.innerHTML = `<button data-bs-toggle="modal" data-bs-target="#notificationModal" data='${JSON.stringify(data)}'>
                              <h4>${data.title}</h4>
                              <p>${data.description}</p>
                              <div class="d-flex justify-content-between">
                                <span>${data.timesince} ago</span>
                                ${unread_element}
                              </div>
                          </button>`;

    var parentUl = document.querySelector('#notifications');
    parentUl.prepend(listItem);
}

function onNotifyDropdownMenuOpened() {
    document.getElementById('notificationModal').addEventListener('show.bs.modal', function (event) {
        var clickedElement = event.relatedTarget;
        var data_str = clickedElement.getAttribute('data');
        const data = JSON.parse(data_str)

        $('#notificationModal .modal-body h4').html(data.title)
        $('#notificationModal .modal-body span').html(data.timesince)
        $('#notificationModal .modal-body p').html(data.description)

        if(data.unread && !data.public) markNotificationAsRead(data.slug, clickedElement)
    });
}
onNotifyDropdownMenuOpened();

function onNotifyDropdownMenuClosed() {
    var myModal = new bootstrap.Modal(document.getElementById('notificationModal'));
    myModal._element.addEventListener('hidden.bs.modal', function (event) {
        document.getElementById('notificationBarDropdown').setAttribute('aria-expanded', 'true');

        let isMenuHidden = $('.notification-bar').find('.dropdown-menu').is(":hidden")
        if (isMenuHidden) $('#notificationBarDropdown').dropdown('toggle');
    });
}
onNotifyDropdownMenuClosed()

function markNotificationAsRead(slug, clickedElement) {
    var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/notification/mark-as-read/' + slug + '/',
        type: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        success: function (response) {
            var unreadElement = clickedElement.querySelector('div > i');
            if (unreadElement) unreadElement.remove();
            updateNotificationBadge(-1)
        },
        error: function (error) { console.error('Error:', error); }
    });
}

function updateNotificationBadge(by){
    var notifyBadge = $('.notify-badge');
    var currentValue = parseInt(notifyBadge.attr('data-count')) || 0;

    var updatedValue = currentValue + by;
    if (updatedValue > 9) notifyBadge.text('9+');
    else notifyBadge.text(updatedValue);
    notifyBadge.attr('data-count', updatedValue);
}
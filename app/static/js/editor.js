var rootRef = new Firebase('https://pair39.firebaseio.com/');
username = $('#username').text();
session_id = $('#session_id').text();
sessionsRef = 'https://pair39.firebaseio.com/'

$(document).ready(function() {
    url_ = '';
    setTimeout(function() {
        url_ = window.location.pathname + window.location.hash;
        console.log(session_id)
        // send session details to server
        $.ajax({
            type: 'POST',
            url: '/fromajax',
            data: JSON.stringify({
                id_: session_id,
                username: username,
                session_url: ('http://localhost:5000' + url_),
            }, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                console.log(result);
            }
        });

    }, 3000);

    var usersAddr = 'https://pair39.firebaseio.com/users';
    var onlineUsers = []
    var allUsers = []
    var showOnlineUsers = function(users, exists) {
        if (exists) {
            for (user in users) {
                allUsers.push(users[user]['user_id'])
            }
        }

        if (allUsers) {
            $.each(allUsers, function(a, b) {
                if ($.inArray(b, onlineUsers) === -1) onlineUsers.push(b)
            })
        }

    }
    setTimeout(function() {
        for (username in onlineUsers) {
            $('#online-users').html(username)

        }
    }, 3000)
    window['onlineUsers'] = onlineUsers

    $('.invite-btn').on('click', function(g) {

        g.preventDefault();
        var key = $(this).parent().parent().find("td:first-child").text();
        console.log(key)

        url_ = window.location.pathname + window.location.hash;

        // send invite details to server
        $.ajax({
            type: 'POST',
            url: '/sendmail',
            data: JSON.stringify({
                id_: session_id,
                username_: username,
                session_addr: '' + window.location.pathname + window.location.hash,
            }, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                console.log(result);
            }
        });
    });

    // Check for online users

    var pollUsers = function() {
        rootRef.child('users').once('value', function(snapshot) {
            var exists = (snapshot.val() !== null);
            showOnlineUsers(snapshot.val(), exists);
        });
    }

    pollUsers()
});

var configEditor = function() {
    // Get a firebase reference
    var firepadRef = getFirebaseRef();

    //// Create ACE
    var editor = ace.edit('firepad');
    editor.setTheme('ace/theme/monokai');
    editor.setFontSize(20)
    var session = editor.getSession();
    session.setUseWrapMode(true);
    session.setUseWorker(false);
    session.setMode('ace/mode/python');

    // start a firepad instance
    var firepad = Firepad.fromACE(firepadRef, editor, {
        defaultText: ''
    });
}

//get's a firebase ref, and adds a hash to the url
var getFirebaseRef = function() {
    var fbRef = new Firebase('https://pair39.firebaseio.com/');
    urlHash = window.location.hash.replace(/#/g, '');
    if (urlHash) {
        fbRef = fbRef.child(urlHash);
    } else {

        fbRef = fbRef.push(); // generate unique location.
        window.location = window.location + '#' + fbRef.key(); // add it as a hash to the URL.
    }
    setTimeout(saveUserSession, 5000)
    return fbRef;
}

var saveUserSession = function() {
    sessionInfo = {
        username: $('#username').text(),
        session: window.location.hash.replace(/#/g, '')
    }

    var rootRef = new Firebase('https://pair39.firebaseio.com/');
    childRef = $('#username').text();
    var sessionsRef = rootRef.child(childRef);
    pushOnline(sessionInfo, sessionsRef);
}

var pushOnline = function(object, ref) {
    var newRef = ref.push();
    newRef.set(object);
}

if (window.location.pathname.indexOf('session') != -1) {
    window.onload = configEditor;
}

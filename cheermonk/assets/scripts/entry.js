var moment = require('moment'); // included thru node_modules & nginx could serve it directly.

$(document).ready(function () {

    $('.from-now').each(function (i, e) {
        (function updateTime() {
            var time = moment($(e).data('datetime'));
            $(e).text(time.fromNow());
            $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
            setTimeout(updateTime, 1000);
        })();
    });

    $('.short-date').each(function (i, e) {
        var time = moment($(e).data('datetime'));
        $(e).text(time.format('MMM Do YYYY'));
        $(e).attr('title', time.format('MMMM Do YYYY, h:mm:ss a Z'));
    });
});

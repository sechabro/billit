

$(document).ready(function () {
    $("#update_modal").modal('show');
});

$("#update-cancel").click(function () {
    { window.history.back() };
});

$(".close").click(function () {
    { window.history.back() };
});
/*


$(".btn.btn-warning").click(function () {
    $("#update_modal").modal('toggle');
});


$(document).ready(function () {
    $(".btn.btn-warning").click(function () {
        $('form').submit()
    })
});



$('form').submit(function (event) {
    let url = "{{ url_for('inv_passthrough') }}";
    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'inv_id': $('.inv_id').val(),
            'client_id': $('.client_id').val(),
        }),
        error: function (error) {
            console.log(error);
        }
    })
    event.preventDefault();
});*/



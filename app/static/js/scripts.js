$(document).ready(function () {
    $("#make_modal").modal('show');
});

$(document).ready(function () {
    $('#paid_boolean_0').click(function () {
        $('#paid-date-picker').show();
    });
    $('#paid_boolean_1').click(function () {
        $('#paid-date-picker').hide();
    });
});


$(document).ready(function () {
    $("#update_modal").modal('show');
});

$(document).ready(function () {
    $("#delete_modal").modal('show');
});


$("#update-cancel").click(function () {
    { window.history.back() };
});

$("#delete-cancel").click(function () {
    { window.history.back() };
});

$(".close").click(function () {
    { window.history.back() };
});



$(document).ready(function () {
    $("#delete-submit").click(function () {
        $('form').submit()
        $('form').submit(function (event) {
            data = JSON.stringify({
                'inv_id': $('#inv_id').val(),
            });
            console.log(data)
            $.ajax('/delete-inv', {
                type: 'POST',
                cache: "no-cache",
                processData: false,
                dataType: "json",
                contentType: "application/json",
                data: data,
                success: function (r) {
                    console.log('Success');
                    console.log(r);
                },
                error: function (r) {
                    console.log('Error');
                    console.log(r);
                }
            })
            event.preventDefault();
        });
    });
});



$(document).ready(function () {
    $("#form-submit").click(function () {
        $('form').submit()
        $('form').submit(function (event) {
            const paidButton = $("input[type='radio']:checked").val(); //false;
            let paidValue = false;
            if (paidButton === "true") { paidValue = true; };
            //if ( $('#paid_boolean_0').checked == True) {paidRB=true;};
            data = JSON.stringify({
                'client_id': $('#client_id').val(),
                'inv_id': $('#inv_id').val(),
                'amount': $('#amount').val(),
                'services': $('#services').val(),
                'paid': paidValue
            });
            console.log(data)
            $.ajax('/update-inv', {
                type: 'POST',
                cache: "no-cache",
                processData: false,
                dataType: "json",
                contentType: "application/json",
                data: data,
                success: function (r) {
                    console.log('Success');
                    console.log(r);
                },
                error: function (r) {
                    console.log('Error');
                    console.log(r);
                }
            })
            event.preventDefault();
        });
    });
});


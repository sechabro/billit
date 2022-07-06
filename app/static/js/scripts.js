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




$("#cancel").click(function () {
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
    $("#make-submit").click(function () {
        $('form').submit()
        $('form').submit(function (event) {
            const paidButton = $("input[type='radio']:checked").val(); //false;
            let paidValue = false;
            let date_paid = null;
            if (paidButton === "true") { paidValue = true; };
            if (paidValue == true) {date_paid = $('#date-paid').val(); };
            //if ( $('#paid_boolean_0').checked == True) {paidRB=true;};
            data = JSON.stringify({
                'client_id': $('#client_id').val(),
                'inv_id': $('#inv_id').val(),
                'amount': $('#amount').val(),
                'services': $('#services').val(),
                'paid': paidValue,
                'date_paid': date_paid
            });
            console.log(data)
            $.ajax('/create-inv', {
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
    $("#update-submit").click(function () {
        $('form').submit()
        $('form').submit(function (event) {
            const paidButton = $("input[type='radio']:checked").val(); //false;
            let paidValue = false;
            let date_paid = null;
            if (paidButton === "true") { paidValue = true; };
            if (paidValue == true) {date_paid = $('#date-paid').val(); };
            data = JSON.stringify({
                'client_id': $('#client_id').val(),
                'inv_id': $('#inv_id').val(),
                'amount': $('#amount').val(),
                'services': $('#services').val(),
                'paid': paidValue,
                'date_paid': date_paid
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


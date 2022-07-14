$(document).ready(function () {
    $("#make_modal").modal('show');
});

// If date_sent invoice value is not null, "yes" is checked, date picker slides open after 600ms delay, and 'Paid?' radio choice slides open 100ms thereafter. 
$(document).ready(function() {
    const dateSent = $('#date-sent').val();
    if (dateSent != null) {
        $("input[name=sent_boolean_0]").prop("checked", true);
        $("input[name=sent_boolean_1]").attr("disabled", true);  
        $("input[name=sent_boolean_0").prop("checked", function() {
            $('#sent-date-picker').delay(600).slideDown(250);
            $('#paid').delay(700).slideDown(250);
        });        
    };
});

// slide-opening and closing sent-date picker
$(document).ready(function () {
    $('#sent_boolean_0').click(function () {
        $('#sent-date-picker').slideDown(250);
        $('#paid').delay(120).slideDown(250);
    })
    $('#sent_boolean_1').click(function () {
        $('#paid').slideUp(250);
        $('#sent-date-picker').delay(120).slideUp(250);

    });
});

// If date_paid invoice value is empty, "no" is checked. Else, "yes" is checked and paid-date picker slides open after 600ms delay.
$(document).ready(function() {
    const datePaid = $('#date-paid').val();
    if (datePaid == "") {
        $("input[id=paid_boolean_1]").prop("checked", true);

    } else {
        $("input[id=paid_boolean_0]").prop("checked", true);
        $("input[id=paid_boolean_1]").prop("disabled", true);
        $("input[id=paid_boolean_0]").prop("checked", function() {
            $('#paid-date-picker').delay(600).slideDown(250);
        });
    };
});


// slide-opening and closing paid-date picker
$(document).ready(function () {
    $('#paid_boolean_0').click(function () {
        $('#paid-date-picker').slideDown(250);
    });
    $('#paid_boolean_1').click(function () {
        $('#paid-date-picker').slideUp(250);
    });
});


/*$(document).ready(function () {
    $('#invoice_data').mouseover(function () {
        $('#overlay').show();
    });
    $('#invoice_data').mouseout(function (){
        $('#overlay').hide();
    });
});*/

$(document).ready(function () {
    $('#invoice_data').click(function () {
        $('#invoice_data_modal').modal('show');
    });
    $('#invoice_data').mouseout(function (){
        $('#overlay').hide();
    });
});

$(document).ready(function () {
    $('#top_ten_clients').click(function () {
        $('#top_ten_clients_modal').modal('show');
    });
    $('#invoice_data').mouseout(function (){
        $('#overlay').hide();
    });
});

$(document).ready(function () {
    $("#update_modal").modal('show');
});

$(document).ready(function () {
    $("#delete_modal").modal('show');
});




$("#cancel").click(function () {
    $('#update_modal').fadeOut(300);
    $('html').delay(300).fadeOut(300);
    $('html').fadeOut(function () {
        window.location.href = document.referrer;
    });
});

$("#close").click(function () {
    $('#update_modal').fadeOut(300);
    $('html').delay(300).fadeOut(300);
    $('html').fadeOut(function () {
        window.location.href = document.referrer;
    });
});





$(document).ready(function () {
    $("#delete-submit").click(function () {
        $('form').submit();
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
                    console.log(r);
                    $('html').fadeOut(300);
                    $('html').fadeOut(function (){
                        window.location.href = document.referrer;
                    })
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
        $('form').submit();
        $('form').submit(function (event) {
            const paidButton = $("input[type='radio']:checked").val();
            const sentButton = $("input[id='sent_boolean_0']:checked").val();
            let paidValue = false;
            let date_paid = null;
            let sentValue = false;
            let date_sent = null;
            if (paidButton === "true") { paidValue = true; };
            if (paidValue == true) { date_paid = $('#date-paid').val(); };
            if (sentButton === "true") { sentValue = true; };
            if (sentValue == true) { date_sent = $('#date-sent').val(); };
            //if ( $('#paid_boolean_0').checked == True) {paidRB=true;};
            data = JSON.stringify({
                'client_id': $('#client_id').val(),
                'inv_id': $('#inv_id').val(),
                'amount': $('#amount').val(),
                'services': $('#services').val(),
                'date_sent': date_sent,
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
                success: function () {
                    $('html').fadeOut(300);
                    $('html').fadeOut(function (){
                        window.location.href = document.referrer;
                    })
                },
                error: function (r) {
                    console.log('Error');
                    console.log(r);
                }
            })
            event.preventDefault();
        })
    });
});





$(document).ready(function () {
    $("#update-submit").click(function () {
        $('form').submit()
        $('form').submit(function (event) {
            const paidButton = $("input[id='id=paid_boolean_0']:checked").val(); //false;
            const sentButton = $("input[id='sent_boolean_0']:checked").val(); //false;
            let paidValue = false;
            let date_paid = null;
            let sentValue = false;
            let date_sent = null;
            if (paidButton === "true") { paidValue = true; };
            if (paidValue == true) { date_paid = $('#date-paid').val(); };
            if (sentButton === "true") { sentValue = true; };
            if (sentValue == true) { date_sent = $('#date-sent').val(); };
            data = JSON.stringify({
                'company': $('#client_company').val(),
                'inv_id': $('#inv_id').val(),
                'amount': $('#amount').val(),
                'services': $('#services').val(),
                'date_sent': date_sent,
                'paid': paidValue,
                'date_paid': date_paid,
            });
            console.log(data)
            $.ajax('/update-inv', {
                type: 'POST',
                cache: "no-cache",
                processData: false,
                dataType: "json",
                contentType: "application/json",
                data: data,
                success: function () {
                    $('html').fadeOut(300);
                    $('html').fadeOut(function (){
                        window.location.href = document.referrer;
                    })
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
    $("#add-client-submit").click(function () {
        $('form').submit()
        $('form').submit(function (event) {
            data = JSON.stringify({
                'company': $('#company').val(),
                'contact': $('#contact').val(),
                'email': $('#email').val(),
                'address': $('#address').val(),
                'city': $('#city').val(),
                'state': $('#state').val(),
                'zipcode': $('#zipcode').val()
            });
            console.log(data)
            $.ajax('/add-client', {
                type: 'POST',
                cache: "no-cache",
                processData: false,
                dataType: "json",
                contentType: "application/json",
                data: data,
                success: function () {
                    $('html').fadeOut(300);
                    $('html').fadeOut(function (){
                        window.location.href = document.referrer;
                    })
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
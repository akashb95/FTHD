$(document).ready(function () {
    let numberExtended = 0;     // Number of times headlines updated via AJAX.
    let currentPage = parseInt($('#page-number').text());

    // In the pagination section, indicate to user current page number.
    $('#' + currentPage).css({'text-color': 'black', 'font-weight': 'bold', 'font-size': '105%'});

    /*
    Posts query via AJAX and extends the headlines div to show more results on the same page.
     */
    $('#extend-button').on('click', function () {
        numberExtended++;
        let fetchPageNumber = currentPage + numberExtended;
        $.ajax({
            url: "/extend/" + fetchPageNumber,
            type: "POST",
            data: $('#q').serialize(),
            success: function (response) {
                // If no more headlines on topic, disable button and hide it.
                if (!response.extend) {
                    $('#extend-button').prop('disabled', 'true');
                    $('#extend-button-div').fadeOut(500);
                }
                $("#headlines").append(response.data);
            }
        });
    });
});
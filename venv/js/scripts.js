$(document).ready(function () {
    let loadingIcon = $('div.o-loading');

    loadingIcon.hide(300);

    function updateResultsPerPage() {
        resultsPerPage = parseInt($('#select-results-per-page option:selected').val());
    }

    let query = $('#q').val();
    let numberExtended = 0;     // Number of times headlines updated via AJAX.
    let currentPage = parseInt($('#page-number').text());
    let resultsPerPage = updateResultsPerPage();
    let totalArticles = parseInt($('#total-articles').text());
    let extendButton = $('#extend-button');
    let canExtend = true;

    // In the pagination section, indicate to user current page number.
    $('#' + currentPage).css({'text-color': 'black', 'font-weight': 'bold', 'font-size': '105%'});

    // When user selects number of results to view per page from dropdown.
    $(document).on('change', '#select-results-per-page', function() {
        loadingIcon.show(0);
        let oldResultsPerPage = resultsPerPage;
        resultsPerPage = updateResultsPerPage();
        let newPageNumber = ~~((currentPage * oldResultsPerPage) / resultsPerPage) + 1;
        $.ajax({
            url: "/search/" + newPageNumber,
            method: "POST",
            data: $('form').serialize(),
            success: function (response) {
                if (!response.extend) {
                    $('#extend-button').prop('disabled', 'true');
                    $('#extend-button-div').fadeOut(500);
                }
                $('#headlines-list').empty().append(response.data);
                $('div.pagination a').each(function () {
                    $(this).attr("href", "/search/" + $(this).attr('id') + "?q=" + query + "&select-results-per-page=" +
                        parseInt($('#select-results-per-page option:selected').val()));
                })
            }
        });
        loadingIcon.hide(300);
    });

    // Hide extend button if no more articles found.
    if (currentPage * resultsPerPage > totalArticles) {
        extendButton.prop('disabled', 'true');
        $('#extend-button-div').hide();
    }

    /*
    Posts query via AJAX and extends the headlines div to show more results on the same page.
     */
    extendButton.on('click', function () {
        canExtend = false;                      // Making sure only one POST request sent at a time!
        loadingIcon.show(0);
        numberExtended++;
        let fetchPageNumber = currentPage + numberExtended;
        $.ajax({
            url: "/search/" + fetchPageNumber,
            type: "POST",
            data: $('form').serialize(),
            success: function (response) {
                // If no more headlines on topic, disable button and hide it.
                if (!response.extend) {
                    $('#extend-button').prop('disabled', 'true');
                    $('#extend-button-div').fadeOut(500);
                }
                $("#headlines-list").append(response.data);
                loadingIcon.hide(300);
                canExtend = true;
            }
        });
    });

    // If nearing bottom of page, extend button clicked and new results loaded preemptively.
    $(window).scroll(function() {
        if ($(window).scrollTop() > $(document).height() - 2 * $(window).height()) {
            if (canExtend) extendButton.click();
        }
    })
});
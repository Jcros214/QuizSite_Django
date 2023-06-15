$('.checkbox').click(function () {
    if ($(this).hasClass('positive')) {
        $(this).removeClass('positive');
        $(this).addClass('negative');
        $(this).html('<svg id="i-close" viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentcolor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10.9375%"><path d="M2 30 L30 2 M30 30 L2 2" /></svg>');
        $(this).next().text('Negative');
    } else if ($(this).hasClass('negative')) {
        $(this).removeClass('negative');
        $(this).html('');
        $(this).next().text('Neutral');
    } else {
        $(this).addClass('positive');
        $(this).html('<svg id="i-checkmark" viewBox="0 0 32 32" width="20" height="20" fill="none" stroke="currentcolor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10.9375%"><path d="M2 20 L12 28 30 4" /></svg>');
        $(this).next().text('Positive');
    }
});

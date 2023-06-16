$('.checkbox-img').each(function () {
    if ($(this).hasClass('positive')) {
        $(this).html('✓');
    } else if ($(this).hasClass('negative')) {
        $(this).html('X');
    } else {
        $(this).html('');
    }
})


$('.checkbox-img').click(function () {
    if ($(this).hasClass('positive')) {
        $(this).removeClass('positive');
        $(this).addClass('negative');
        $(this).html('X');
    } else if ($(this).hasClass('negative')) {
        $(this).removeClass('negative');
        $(this).html('');
    } else {
        $(this).addClass('positive');
        $(this).html('✓');
    }
});

get_new_question = function () {
    $.ajax({
        url: "{% url 'quiz_games:match_verse_backend' %}",
        success: function (data, status, xhr) {
            console.log(data);
            $('#prompt').html(data.verse);
            $('.row#options input').each(function () {
                $(this).val(data['verse_ref_options'].shift());
            });
        },
        error: function (xhr, status, error) {
            console.log(xhr);
            console.log(status);
            console.log(error);
        }
    });
}

function delay(milliseconds) {
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}


check_answer = function (event) {
    var clickedElement = event.target;
    $.ajax({
        url: "{% url 'quiz_games:match_verse_backend' %}",
        type: 'POST',
        headers: {
            'X-CSRFToken': "{{ csrf_token }}",
        },
        data: {verse_ref: clickedElement.value},
        success: function (data, status, xhr) {
            let result_element = $('#result');

            result_element.html(data.result);
            result_element.css('display', 'block');

            let time;

            if (data.result === 'Correct!') {
                time = 1250;
                result_element.removeClass('alert-danger');
                result_element.addClass('alert-success');
            } else {
                time = 5000;
                result_element.removeClass('alert-success');
                result_element.addClass('alert-danger');
            }

            delay(time).then(() => {
                $('#result').css('display', 'none');
                get_new_question();
            });
        },
        error: function (xhr, status, error) {
            console.log(xhr);
            console.log(status);
            console.log(error);
        }
    });
}

$(document).ready(function () {
    get_new_question();
    $('#next_question').click(get_new_question);

    $('.row#options input').each(function () {
        $(this).click(check_answer);
    });
});

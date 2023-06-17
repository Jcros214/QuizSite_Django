function setCheckBox(checkbox, value) {
    // value = 'positive', 'negative', or 'neutral'

    if (value === 'positive') {
        checkbox.removeClass('negative');
        checkbox.addClass('positive');
        checkbox.html('✓');
    } else if (value === 'negative') {
        checkbox.removeClass('positive');
        checkbox.addClass('negative');
        checkbox.html('X');
    } else if (value === 'neutral') {
        checkbox.removeClass('positive');
        checkbox.removeClass('negative');
        checkbox.html('');
    }
}

function updateAllScores() {
    $(".individual-name").each(function () {
        // count the number of children with .positive .negative
        const correct = $(this).parent().find(".positive").length
        const incorrect = $(this).parent().find(".negative").length

        // update the score
        $(this).parent().find(".individual-score").html(correct + ":" + incorrect);
    });

    $(".team-name").each(function () {
        let teamScore = 40;
        const teamScoreElement = $(this).parent().find(".team-score");

        // count the number of children with .positive .negative
        $(this).parent().parent().find(".individual-score")
            .each(function () {
                    const score = $(this).html().split(":");
                    console.log(score)
                    teamScore += parseInt(score[0]) * 20;
                    teamScore += parseInt(score[1]) * -10;
                }
            );

        teamScoreElement.html(teamScore);

    });
}


$('.checkbox-img').each(function () {
    if ($(this).hasClass('positive')) {
        $(this).html('✓');
    } else if ($(this).hasClass('negative')) {
        $(this).html('X');
    } else {
        $(this).html('');
    }
})

updateAllScores()

$('.checkbox-img').click(function () {
    const quizzer_id = this.dataset.quizzerId;
    const question_id = this.dataset.questionId;

    let result = '';

    if ($(this).hasClass('positive')) {         // Make Negative
        result = 'negative'
    } else if ($(this).hasClass('negative')) {  // Make Positive
        result = 'neutral'
    } else {                                    // Make Neutral
        result = 'positive'
    }

    setCheckBox($(this), result);

    const csrftoken = Cookies.get('csrftoken');

    $.ajax({
        url: window.location.href,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: {
            quizzer_id: quizzer_id,
            question_id: question_id,
            result: result,
        },
        success: function (data, status, xhr) {
            console.log(data);
            console.log(status);
            console.log(xhr);
        },
        error: function (xhr, status, error) {
            console.log(xhr);
            console.log(status);
            console.log(error);
        }
    });

//     update scores
    updateAllScores();

});

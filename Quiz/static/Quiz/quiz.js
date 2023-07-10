const num_questions_per_quizzer = num_teams === 3 ? 4 : 6;

const csrftoken = Cookies.get('csrftoken');

const allCheckboxes = $('.checkbox-img');
const quizzerValidateCheckboxes = $('.quizzer-validate');
const submit_button = $('#submit');
const tiebreaker_button = $('#tiebreaker');


// Get only the unique question_ids from all checkboxes
const question_ids = [];

const team_ids = [];
quizzerValidateCheckboxes.each(function () {
    if (!team_ids.includes(this.dataset.teamId)) {
        team_ids.push(this.dataset.teamId);
    }
});

allCheckboxes.each(function () {
    if (!question_ids.includes(this.dataset.questionId)) {
        question_ids.push(this.dataset.questionId);
    }
});

question_ids.sort();

function setCheckBox(checkbox, value) {
    // value = 'positive', 'negative', or 'neutral'
    if (value === 'positive') {
        checkbox.removeClass('negative');
        checkbox.addClass('positive');
    } else if (value === 'negative') {
        checkbox.removeClass('positive');
        checkbox.addClass('negative');
    } else if (value === 'neutral') {
        checkbox.removeClass('positive');
        checkbox.removeClass('negative');
    } else {
        console.log('Error: value must be "positive", "negative", or "neutral"');
    }
}

function updateAllScores() {
    $(".individual-name").each(function () {
        // count the number of children with .positive .negative
        const correct = $(this).parent().find(".positive[data-question-type=normal]").length
        const incorrect = $(this).parent().find(".negative[data-question-type=normal]").length

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
                    teamScore += parseInt(score[0]) * 20;
                    teamScore += parseInt(score[1]) * -10;
                }
            );

        teamScoreElement.html(teamScore);

    });
}


function areScoresUnique() {
    const team_scores = [];

    $('.team-score').each(function () {
        team_scores.push(parseInt($(this).html()));
    });

    let tiebreaker_value = 2;

    $('.question-number').each(function () {
        if ($(this).html() === 'TIE') {
            const questions = $('.checkbox-img[data-question-id="' + $(this).data('question-id') + '"]');

            questions.each(function () {
                if ($(this).hasClass('positive')) {
                    team_scores[team_ids.indexOf(String($(this).data('team-id')))] += tiebreaker_value;
                    tiebreaker_value -= 1;
                } else if ($(this).hasClass('negative')) {
                    team_scores[team_ids.indexOf(String($(this).data('team-id')))] -= tiebreaker_value;
                    tiebreaker_value -= 1;
                }
            });
        }
    });
    return team_scores.length === new Set(team_scores).size;
}


function get_team_ids_with_unique_scores() {
    const team_scores = [];

    $('.team-score').each(function () {
        team_scores.push(parseInt($(this).html()));
    });


    const team_scores_by_occurrence = [[], [], []];

    $(".team-score").each(function () {
        const score = parseInt($(this).html());

        const team_id = parseInt($(this).parent().parent().data("team-id"));

        team_scores_by_occurrence[team_scores.filter(x => x === score).length - 1].push(team_id);
    });

    return team_scores_by_occurrence;
}

function disableAnyUnusableCheckboxes() {
    updateAllScores();
    // remove disabled-checkbox from all checkboxes
    allCheckboxes.each(function () {
        $(this).removeClass('disabled-checkbox')
    });


    // Disable all checkboxes not in the column of the first unasked question
    // Find the first unasked question
    let first_unasked_question = [...question_ids];

    let question_counter = 0;

    for (question_counter; question_counter < question_ids.length; question_counter++) {
        // find all checkboxes with that question_id
        const questionCheckboxes = $('.checkbox-img[data-question-id="' + question_ids[question_counter] + '"]');

        // find the first checkbox in that list that is not positive or negative
        const doesNotContainResponse = (questionCheckboxes.filter('.positive, .negative').length === 0) && ($('.not-answered.was-not-answered[data-question-id="' + question_ids[question_counter] + '"]').length === 0);

        if (doesNotContainResponse) {
            break;
        } else {
            questionCheckboxes.each(function () {
                if ($(this).hasClass('positive') || $(this).hasClass('negative')) {

                } else {
                    $(this).addClass('disabled-checkbox');
                }
            });
        }
    }

    const current_question_id = question_ids[question_counter];


    // TODO:
    // // If someone on a team has validated, then add 'invisible' class the the other teammate's validate checkbox
    // $('.quizzer-validate').each(function () {
    //
    // }


    ++question_counter;

    for (question_counter; question_counter < question_ids.length; question_counter++) {
        // find all checkboxes with that question_id
        const questionCheckboxes = $('.checkbox-img[data-question-id="' + question_ids[question_counter] + '"]');

        questionCheckboxes.each(function () {
            if ($(this).hasClass('positive') || $(this).hasClass('negative')) {

            } else {
                $(this).addClass('disabled-checkbox');
            }
        });

    }

    // Enable the not-answered checkboxes for the current question
    //      disable the others
    $('.not-answered:not(.was-not-answered)').each(function () {
        $(this).addClass('invisible');
    });

    $('.not-answered[data-question-id="' + current_question_id + '"]').each(function () {
        $(this).removeClass('invisible');
    });

    // Disable any checkboxes that are in the same row with 4 (or 6) answered questions
    $('.checkbox-img:not(.positive):not(.negative)').each(function () {
        const quizzer_id = this.dataset.quizzerId;
        const quizzerCheckboxes = $('.checkbox-img[data-quizzer-id="' + quizzer_id + '"]');
        const answeredCheckboxes = quizzerCheckboxes.filter('.positive, .negative');
        const unansweredCheckboxes = quizzerCheckboxes.filter(':not(.positive):not(.negative)');
        const answered = answeredCheckboxes.length;
        if (answered === num_questions_per_quizzer) {
            unansweredCheckboxes.each(function () {
                $(this).addClass('disabled-checkbox');
            });
        }
    });


    const current_checkboxes = $('.checkbox-img[data-question-id="' + current_question_id + '"]');

    if (current_checkboxes.first().data('question-type') === 'tiebreaker') {
        current_checkboxes.each(function () {
            $(this).removeClass('disabled-checkbox');
        });

        const current_scores = get_team_ids_with_unique_scores();

        // For each team with a unique score, disable all checkboxes for that team
        current_scores[0].forEach(function (team_id) {
            $('.checkbox-img[data-team-id="' + team_id + '"]').each(function () {
                $(this).addClass('disabled-checkbox');
            });
        });
    }

    // Check that all questions have been answered
    let any_unanswered = false;

    allCheckboxes.each(function () {
        if (!($(this).hasClass('positive') || $(this).hasClass('negative') || $(this).hasClass('disabled-checkbox'))) {
            any_unanswered = true;
        }
    });

    if (any_unanswered) {
        submit_button.attr('disabled', true);
        tiebreaker_button.attr('disabled', true);
        return;
    }

    // Proceeding, all questions have been answered

    if (!allow_ties && !areScoresUnique()) {
        submit_button.attr('disabled', true);
        tiebreaker_button.removeAttr('disabled');
        // submit_button.removeClass('btn-primary');
        // submit_button.addClass('btn-secondary');
        // tiebreaker_button.removeClass('btn-secondary');
        // tiebreaker_button.addClass('btn-primary');
        quizzerValidateCheckboxes.each(function () {
            $(this).addClass('invisible');
        });
    } else {
        // Check that all questions have been answered
        let any_unanswered = false;

        allCheckboxes.each(function () {
            if (!($(this).hasClass('positive') || $(this).hasClass('negative') || $(this).hasClass('disabled-checkbox'))) {
                any_unanswered = true;
            }
        });

        if (any_unanswered) {
            $(this).addClass('invisible');
        } else {
            quizzerValidateCheckboxes.each(function () {
                $(this).removeClass('invisible');
            });
        }

        // Enable the submit button, then if any team hasn't validated, disable the submit button
        submit_button.removeAttr('disabled');
        for (let i = 0; i < team_ids.length; i++) {
            const team_id = team_ids[i];
            const teamValidates = $('.quizzer-validate[data-team-id="' + team_id + '"]');
            const teamValidatesChecked = teamValidates.filter(':checked');
            if (teamValidatesChecked.length === 0) {
                submit_button.attr('disabled', true);
            }

            //     check for non-unique scores
        }
    }
}

tiebreaker_button.click(function () {
    $(this).attr('disabled', true);

    $.ajax({
        url: window.location.href,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: {
            add_tiebreaker: true,
        },
        success: function (data, status, xhr) {
            location.reload();
        },
        error: function (xhr, status, error) {
            console.log(xhr, status, error);
        }
    });
});
allCheckboxes.click(function () {

    if ($(this).hasClass('disabled-checkbox')) {
        return;
    }

    const quizzer_id = this.dataset.quizzerId;
    const question_id = this.dataset.questionId;

    let result;

    if ($(this).hasClass('positive')) {         // Make Negative
        result = 'negative'
    } else if ($(this).hasClass('negative')) {  // Make Positive
        result = 'neutral'
    } else {                                    // Make Neutral
        result = 'positive'
    }

    setCheckBox($(this), result);

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
            // console.log(data, status, xhr);
        },
        error: function (xhr, status, error) {
            console.log(xhr, status, error);
        }
    });

//     update scores
    updateAllScores();
    disableAnyUnusableCheckboxes();

});

$('.not-answered').click(function () {

    let result;

    if ($(this).hasClass('was-not-answered')) {
        result = 'neutral';
    } else {
        result = 'not answered';
    }

    $(this).toggleClass('was-not-answered');

    const quizzer_id = this.dataset.quizzerId;
    const question_id = this.dataset.questionId;


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
            console.log(data, status, xhr);
        },
        error: function (xhr, status, error) {
            console.log(xhr, status, error);
        }
    });

    // update scores
    updateAllScores();
    disableAnyUnusableCheckboxes();
});

quizzerValidateCheckboxes.click(disableAnyUnusableCheckboxes);

// Run on page load
allCheckboxes.each(function () {
    if ($(this).hasClass('positive')) {
        setCheckBox($(this), 'positive');
    } else if ($(this).hasClass('negative')) {
        setCheckBox($(this), 'negative');
    } else {
        setCheckBox($(this), 'neutral');
    }
    // Not reload????
})

submit_button.click(function () {
    $(this).attr('disabled', true);

    $.ajax({
        url: window.location.href,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: {
            quiz_validated_by_scorekeeper: true,
        },
        success: function (data, status, xhr) {
            location.reload();
        },
        error: function (xhr, status, error) {
            console.log(xhr, status, error);
        }
    });
});

quizzerValidateCheckboxes.click(function () {
    const quizzer_id = this.dataset.quizzerId;
    // TODO: Submit "unchecking" the box

    $.ajax({
        url: window.location.href,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: {
            quiz_validated_by_quizzer: quizzer_id,
        },
        success: function (data, status, xhr) {
        },
        error: function (xhr, status, error) {
            console.log(xhr, status, error);
        }
    });
});


// (function () {
//     let previous;
//
//     $('.team-select').on('focus', function () {
//         // Store the current value on focus and on change
//         previous = this.value;
//     }).change(function () {
//         // Do something with the previous value after the change
//         $.ajax({
//             url: window.location.href,
//             type: 'POST',
//             headers: {
//                 'X-CSRFToken': csrftoken,
//             },
//             data: {
//                 team_select: true,
//                 previous_team_id: previous,
//                 new_team_id: this.value,
//             },
//             success: function (data, status, xhr) {
//                 // location.reload();
//             },
//             error: function (xhr, status, error) {
//             }
//         });
//
//
//         // Make sure the previous value is updated
//         previous = this.value;
//     });
// })();
//

updateAllScores()
disableAnyUnusableCheckboxes()

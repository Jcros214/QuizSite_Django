SELECT rd.name as division
    , t.short_name as teamletter
    , t.name as teamname
    , i.name as individualname
    , t.type as teamtype
    , i.gender as gender
--    , rq.round as round
    , sum(CASE WHEN aq.ruling = 'correct' THEN 1 ELSE 0 END) as correct
    , sum(CASE WHEN aq.ruling = 'incorrect' THEN 1 ELSE 0 END) as incorrect
    , ip.quizzes as quizzes
    , sum(coalesce(aq.value, 0)) + (ip.quizzes *20) as points
from "Records_team" t
left join "Records_teammembership" tm on tm.team_id = t.id
left join "Records_division_teams" rdt on t.id = rdt.team_id
left join "Records_individual" i on tm.individual_id = i.id
left join "Records_quizparticipants" qp on qp.team_id = t.id
left join "Records_quiz" rq on qp.quiz_id = rq.id
left join "Records_event" e on rq.event_id = e.id
left join "Records_division" rd on rdt.division_id = rd.id and rd.event_id = e.id
left join "Records_askedquestion" aq on aq.individual_id = i.id and aq.quiz_id = rq.id
left join (
    SELECT qp.team_id, rqc.id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rqc on qp.quiz_id = rqc.id
    left join "Records_event" e on rqc.event_id = e.id
    where e.id = {} and cast(rqc.round as int) = (select min(cast(rq1.round as int)) from "Records_quiz" rq1 where e.id = {} and rq1."isValidated" = false)
) as cr on cr.team_id = t.id
left join (
    SELECT qp.team_id, rqn.id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rqn on qp.quiz_id = rqn.id
    left join "Records_event" e on rqn.event_id = e.id
    where e.id = {} and cast(rqn.round as int) = ((select min(cast(rq2.round as int)) from "Records_quiz" rq2 where e.id = {} and rq2."isValidated" = false) + 1)
) as nr on nr.team_id = t.id
left join (
    SELECT tm.individual_id, COUNT(qp.team_id) as quizzes
    from "Records_team" t
    left join "Records_teammembership" tm on tm.team_id = t.id
    left join "Records_quizparticipants" qp on qp.team_id = t.id
    left join "Records_quiz" rq on qp.quiz_id = rq.id
    left join "Records_event" e on rq.event_id = e.id
    where e.id = {}
    and cast(rq.round as int) <= (select min(cast(rq3.round as int)) from "Records_quiz" rq3 where e.id = {} and rq3."isValidated" = false)
    group by tm.individual_id
) as ip on ip.individual_id = i.id

where e.id = {} and rq.type = 'normal' and aq.type = 'normal'
group by rd.name
    , t.short_name
    , t.name
    , i.name
    , t.type
    , i.gender
--    ,rq.round
    , ip.quizzes
order by rd.name, short_name, i.name--, rq.round
   select
    t.short_name,
    t.name as teamname,
    t.division as division,
    cr.id as currentround,
    nr.id as nextround,
    i.id as individualid,
    i.name as individualname,
    sum(coalesce(aq.value, 0)) as points,
    cr2.attendancepoints as attendancepoints
from "Records_team" t
left join "Records_teammembership" tm on tm.team_id = t.id
left join "Records_individual" i on tm.individual_id = i.id
left join "Records_quizparticipants" qp on qp.team_id = t.id
left join "Records_quiz" rq on qp.quiz_id = rq.id
left join "Records_event" e on rq.event_id = e.id
left join "Records_askedquestion" aq on aq.individual_id = i.id and aq.quiz_id = rq.id
left join (
    SELECT qp.team_id, rqc.id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rqc on qp.quiz_id = rqc.id
    where cast(rqc.round as int) = (
            select min(cast(rq.round as int)) 
            from "Records_quiz" rq 
            left join "Records_event" e on rq.event_id = e.id
            where e.id = {} and rq."isValidated" = false)
) as cr on cr.team_id = t.id
left join (
    SELECT qp.team_id, rq.id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rq on qp.quiz_id = rq.id
    where cast(rq.round as int) = (
        (select min(cast(rq.round as int)) 
        from "Records_quiz" rq 
        left join "Records_event" e on rq.event_id = e.id
        where e.id = {} and rq."isValidated" = false) 
        + 1)
) as nr on nr.team_id = t.id
left join (
    SELECT qp.team_id, count(qp.team_id)*20 as attendancepoints
    from "Records_quizparticipants" qp
    left join "Records_quiz" rq on qp.quiz_id = rq.id
    left join "Records_event" e on rq.event_id = e.id
    where e.id = {} and cast(rq.round as int) <= (
        select min(cast(rq.round as int)) 
        from "Records_quiz" rq 
        left join "Records_event" e on rq.event_id = e.id
        where e.id = {} and rq."isValidated" = false)
    group by qp.team_id
) as cr2 on cr2.team_id = t.id
where e.id = {}
group by
    t.short_name,
    t.name,
    t.division,
    cr.id,
    nr.id,
    i.id,
    i.name,
    cr2.attendancepoints
order by t.short_name, i.id

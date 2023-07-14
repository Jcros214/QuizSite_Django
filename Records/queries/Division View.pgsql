SELECT
    t.short_name,
    t.name as teamname,
    rd.name as division,
    cr.id as currentround,
    nr.id as nextround,
    i.id as individualid,
    i.name as individualname,
    sum(COALESCE(aq.value, 0)) as points,
    COALESCE(cr2.attendancepoints,0) as attendancepoints
from "Records_team" t
left join "Records_teammembership" tm on tm.team_id = t.id
left join "Records_division_teams" rdt on t.id = rdt.team_id
left join "Records_individual" i on tm.individual_id = i.id
left join "Records_quizparticipants" qp on qp.team_id = t.id
left join "Records_quiz" rq on qp.quiz_id = rq.id
left join "Records_event" e on rq.event_id = e.id
left join "Records_division" rd on rdt.division_id = rd.id and rd.event_id = e.id
left join "Records_askedquestion" aq on aq.individual_id = i.id and aq.quiz_id = rq.id
left join "view_roundcurrentno" vrcn on e.id = vrcn.event_id
left join "view_rounds" cr on t.id = cr.team_id and COALESCE(vrcn.round,1) = cr.round
left join "view_rounds" nr on t.id = nr.team_id and (COALESCE(vrcn.round,1)+1) = nr.round
left join "view_attendancepointsindv" as cr2 on cr2.individual_id = i.id
where e.id = {event.id} and coalesce(rq.type, 'normal') = 'normal' and coalesce(aq.type, 'normal') = 'normal'
and rd.id = {division.id}
group by t.short_name
    , t.name
    , rd.name 
    , cr.id
    , nr.id 
    , i.id 
    , i.name 
    , cr2.attendancepoints
order by rd.name, short_name, i.name
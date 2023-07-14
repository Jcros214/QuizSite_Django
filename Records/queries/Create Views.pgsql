CREATE OR REPLACE VIEW view_roundcurrentno AS
    select rq.event_id as event_id, min(rq.round) as round
    from "Records_quiz" rq 
    where rq."isValidated" = false
    group by rq.event_id;

CREATE OR REPLACE VIEW view_rounds AS
    SELECT rq.event_id, rq.round, rq.id, qp.team_id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rq on qp.quiz_id = rq.id;

CREATE OR REPLACE VIEW view_attendancepointsindv AS
    SELECT rq.event_id, qp.team_id, tm.individual_id, CAST(count(COALESCE(qp.team_id,0))*20 as bigint) as attendancepoints
    from "Records_quizparticipants" qp
    left join "Records_quiz" rq on qp.quiz_id = rq.id
    left join "Records_teammembership" tm on qp.team_id = tm.team_id
    left join "Records_individual" i on tm.individual_id = i.id
    left join "view_roundcurrentno" vrcn on rq.event_id = COALESCE(vrcn.event_id,1)    
    where rq.type = 'normal' and rq.round <= COALESCE(vrcn.round,1)
    group by rq.event_id, qp.team_id, tm.individual_id
    order by rq.event_id, qp.team_id, tm.individual_id;

CREATE OR REPLACE VIEW view_attendancepointsteam AS
    SELECT vapi.event_id, vapi.team_id, CAST(sum(COALESCE(vapi.attendancepoints)) as bigint) as attendancepoints
    from "view_attendancepointsindv" vapi
    group by vapi.event_id, vapi.team_id
    order by vapi.event_id, vapi.team_id;
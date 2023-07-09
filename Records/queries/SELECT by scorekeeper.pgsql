SELECT * 
from "Records_quiz" rq
join "Records_room" rr on rq.room_id = rr.id
join "Records_individual" ri on rr.scorekeeper_id = ri.id
join "auth_user" au on ri.user_id = au.id
where au.username = 'David Crosby'
order by rq.event_id, rq.round

update "Records_quiz" 
set "isValidated" = false
where id = 478


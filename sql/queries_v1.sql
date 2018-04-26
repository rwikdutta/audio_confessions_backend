-- 1 Create view ask_content_type_id
create or replace view public.ask_content_type_id as
select id from django_content_type where app_label = 'ask';

-- 2 Create view confession_content_type_id
create or replace view confessions_content_type_id as
select id from django_content_type where app_label='confessions';

--3. view ask wise likes aggregate
create or replace view likes_ask_agg as
select count(id) as likes_count,likes_likes.object_id FROM likes_likes  WHERE likes_likes.content_type_id in (select id from ask_content_type_id) GROUP BY object_id;

-- 4. view confessions wise likes aggregate
create or replace view likes_confessions_agg as
select count(id) as likes_count,likes_likes.object_id FROM likes_likes  WHERE likes_likes.content_type_id in (select id from confessions_content_type_id) GROUP BY object_id;

--5. view ask wise comments aggregate
create or replace view comments_ask_agg as
select count(id) as comments_count,object_pk from django_comments where content_type_id in (select id from ask_content_type_id) group by object_pk;


-- 6. view confessions wise comments aggregate
create or replace view comments_confessions_agg as
select count(id) as comments_count,object_pk from django_comments where content_type_id in (select id from confessions_content_type_id) group by object_pk;

--7. materialized view ask posts ranking
create materialized view ask_post_rankings as
select t1.* from ask_ask as t1 left join (select comments_count,likes_count,object_id,coalesce(comments_count,0)+coalesce(likes_count,0) as score from comments_ask_agg full join likes_ask_agg on cast (object_pk as integer)=object_id) t2 on t1.id=t2.object_id order by coalesce(t2.score,0) desc,t1.id desc
with data;

--8. materialized view confession posts ranking
create materialized view confession_post_rankings as
select t1.* from confessions_confessions as t1 left join (select comments_count,likes_count,object_id,coalesce(comments_count,0)+coalesce(likes_count,0) as score from comments_confessions_agg full join likes_confessions_agg on cast (object_pk as integer)=object_id) t2 on t1.id=t2.object_id order by coalesce(t2.score,0) desc,t1.id desc
with data;

--9. materialized view counts of tags
create materialized view tags_tag_count as
select t1.* from taggit_tag as t1 left join (select tag_id,count(id) as tags_count from taggit_taggeditem group by tag_id order by tags_count desc) t2 on t1.id=t2.tag_id where t2.tags_count is not null order by tags_count desc, id desc
with data;


--10. Updating likes_count ( one time initialization ) for confessions_confessions
UPDATE confessions_confessions
SET likes_count=likes_confessions_agg.likes_count
FROM
likes_confessions_agg
where
confessions_confessions.id=likes_confessions_agg.object_id;

--11. Updating comments_count ( one time initialization ) for confessions_confessions
UPDATE confessions_confessions
SET comments_count=comments_confessions_agg.comments_count
FROM
comments_confessions_agg
where
confessions_confessions.id=cast(comments_confessions_agg.object_pk as integer);

--12. Updating likes_count ( one time initialization ) for ask_ask
UPDATE ask_ask
SET likes_count=likes_ask_agg.likes_count
FROM
likes_ask_agg
where
ask_ask.id=likes_ask_agg.object_id;

--13. Updating comments_count ( one time initialization ) for ask_ask
UPDATE ask_ask
SET comments_count=comments_ask_agg.comments_count
FROM
comments_ask_agg
where
ask_ask.id=cast(comments_ask_agg.object_pk as integer);

--14. Reordering confessions_confessions by most popular
select * from confessions_confessions order by (likes_count + comments_count) desc,id desc;

--15. Reordering confessions_confessions by most popular
select * from ask_ask order by (likes_count + comments_count) desc,id desc;

--16. Count of tags by tag_id for one time initialization of hashtags_tagcount
delete from hashtags_tagcount;

insert into hashtags_tagcount(tag_id,count)
select t2.id as tag_id,coalesce(t1.count,0) as count from (select tag_id,cast(count(id) as integer) as count from taggit_taggeditem group by tag_id) t1 right join taggit_tag t2 on t1.tag_id=t2.id;
create table game_user(
	username varchar2(50),
	bal number default 1500,
	points number default 0,
	PRIMARY key(username)

);

insert into game_user(username) values('sakib101');

create table seller
(
	points number,
	acc_bal number default 0
);

insert into seller(points) values (500);

create table get_order
(
	order_id varchar2(50),
	u_name varchar2(50),
	required_points number,
	tcost number,
	primary key(order_id),
	FOREIGN KEY (u_name) REFERENCES game_user(username)
	);



create or replace function cost_calculation( points number )
return NUMBER
IS

BEGIN
	if points>=1 and points<=9 THEN
		return points*7;
	elsif points>=10 and points<=49 THEN
		return points*6;
	elsif points>=50 and points<=99 THEN
		return points*5;
	elsif points>=100 and points<=449 THEN
		return points*4;
	elsif points>=500 THEN
		return points*3;
	end if;
	
end;
/
	
create or replace trigger t_point
after INSERT
on get_order
for each row

declare 
	seller_current_points_available number;
	seller_updated_points number;
	
	seller_curr_bal number;
	seller_updated_bal number;
	
	buyer_curr_bal number;
	buyer_curr_points number;
	
	updated_curr_bal number;
	updated_curr_points number;
	
BEGIN
	
	select points into seller_current_points_available
	from seller;
	seller_updated_points:= seller_current_points_available- :NEW.required_points;
	
	
	select acc_bal into seller_curr_bal 
	from seller;
	seller_updated_bal:= seller_curr_bal + :NEW.tcost;
	
	select bal into buyer_curr_bal
	from game_user
	where username= :NEW.u_name;
	updated_curr_bal:= buyer_curr_bal - :NEW.tcost;
	
	select points into buyer_curr_points
	from game_user
	where username= :NEW.u_name;
	updated_curr_points:= buyer_curr_points + :NEW.required_points;
	
	if seller_updated_points>=0 THEN
		--dbms_output.put_line(seller_current_points_available);
		UPDATE seller
		set points = seller_updated_points;
		
		update seller
		set acc_bal= seller_updated_bal;
		
		update game_user
		set bal= updated_curr_bal
		where username = :NEW.u_name;
		
		update game_user
		set points =updated_curr_points
		WHERE username = :NEW.u_name;

	ELSE 
		dbms_output.put_line('points are not available as you expected');
	end if;	
end;
/


create or replace procedure p1( u_name in varchar2,  points in number)
is 
	user_balance number;
	cost number;
	
begin
	select bal into user_balance 
	from game_user 
	where username=u_name;
	
	cost:=cost_calculation(points);
	
	if cost<=user_balance THEN
		
		dbms_output.put_line('you are eligible to buy');
		insert into get_order values('o-101',u_name, points,cost);
		
	ELSE
		dbms_output.put_line('Not sufficient balance!');
	end if;
end;
/

execute p1('Ahiad',52);
 
 

 


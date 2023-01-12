from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from users.models import Log
from django.db import connection


# Create your views here.
def homepage(request):
    current_user = request.user
    superuser = User.objects.get(is_superuser=True)
    logs = Log.objects.all()
    sum=0
    for log in logs:
        sum+=log.amount

    if request.method == 'POST':
        data = request.POST
        points = data.get('getPoints')
        query = """
            CREATE OR REPLACE FUNCTION public.cost_calculation(
            point numeric)
            RETURNS numeric
            LANGUAGE 'plpgsql'
            COST 100
            VOLATILE PARALLEL UNSAFE
        AS $BODY$
        BEGIN
            if point>=1 and point<=9 THEN
                return point*7;
            elsif point>=10 and point<=49 THEN
                return point*6;
            elsif point>=50 and point<=99 THEN
                return point*5;
            elsif point>=100 and point<=449 THEN
                return point*4;
            elsif point>=500 THEN
                return point*3;
            end if;
            
        end;
        $BODY$;

        ALTER FUNCTION public.cost_calculation(numeric)
            OWNER TO postgres;
            
        CREATE OR REPLACE PROCEDURE public.buy_points(
            u_id numeric,
            points numeric)
        LANGUAGE 'plpgsql'
        AS $BODY$
        Declare
            bal numeric := 0;
        begin
            select tk into bal from public.users_profile where u_id = users_profile.user_id;
            if cost_calculation(points)<= bal THEN
                
                update users_profile set tk = tk- cost_calculation(points)
                where user_id = u_id;
                
                insert into users_log values(nextval('log_seq'), cost_calculation(points), points, now(), u_id);
                
            end if;
        end;
        $BODY$;
    """
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.execute('CALL public.buy_points(%s, %s)', [current_user.id, points])
        
        #trigger
        cursor.execute("DROP TRIGGER update_points ON users_log")
        cursor.execute("""
        CREATE OR REPLACE FUNCTION update_points_function()
        RETURNS TRIGGER
        AS $$
        BEGIN
            UPDATE users_profile SET point = point - NEW.buy_point WHERE user_id = (SELECT id FROM auth_user WHERE is_superuser = true);
            UPDATE users_profile SET point = point + NEW.buy_point where user_id = new.user_id;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        """)
        cursor.execute("""
        CREATE TRIGGER update_points
        AFTER INSERT ON users_log
        FOR EACH ROW
        EXECUTE PROCEDURE update_points_function();
        """)
        cursor.close()
        # query1 = """CALL public.update_user_credits(, );"""
        # query_formatted=query1.format(current_user.id, 40)
        # db.engine.execute(query+query_formatted)
    return render(request, 'tapp/home.html', {'point': superuser.profile.point, 'earnings': sum})
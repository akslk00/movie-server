from flask import request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import validate_email,EmailNotValidError
from utils import check_password, hash_password

class MoviesResources(Resource):
    
    @jwt_required(optional=True)
    def get(self):
        try:
            connection = get_connection()
            query = '''select m.title,count(r.id) as count,ifnull((r.rating),0) as avg_rating
                    from movie m
                    left join review r
                    on r.movieId=m.id
                    left join favorite f
                    on f.moviesId = r.movieId
                    group by m.id
                    order by count desc;'''
        
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
    
        return{'result':'seccess',
               'items':result_list,
               'count':len(result_list)},200
    
    def post(self):
        connection =get_connection()
        data = request.get_json()
        try:
            query = '''select m.title,count(m.id) as count,ifnull((r.rating),0) as avg
                        from movie m
                        left join review r
                        on r.movieId=m.id
                        where title like %s
                        group by m.id;'''
            record = (data['title'],)
    
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            
            result_list = cursor.fetchall()
            print(result_list)

            i =0
            for row in result_list:
                result_list[i]['avg']=str(row['avg'])
                i = i + 1

            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
    
        return{'result':'seccess',
               'item':result_list,
               'count':len(result_list)},200
    

class MovieResources(Resource):

    def get(self,moveId):
        connection =get_connection()
        
        
        try:
            query = '''select m.id,m.title,m.summary,m.year,m.attendance,ifnull(avg(r.rating),0) as avg
                            from movie m
                            left join review r
                            on r.movieId=m.id
                            group by r.movieId
                            having m.id= %s
                            
                            ;'''
            record = (moveId,)
    
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            

            result_list = cursor.fetchall()
            print(result_list)

            i =0
            for row in result_list:
                result_list[i]['year']=row['year'].isoformat()
                result_list[i]['avg']=str(row['avg'])
                i = i + 1

            #result_list = str(result_list)

            print(result_list)

            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
    
        return{'result':'seccess',
               'item':result_list},200

class MovieReviewResources(Resource):

    def get(self):

        connection =get_connection()
        moveId = request.args.get('movieId')
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        
        try:
            query = '''select m.title,u.nickname,u.gender,r.rating
                        from movie m
                        left join review r
                        on m.id=r.movieId
                        join user u
                        on r.userId=u.id
                        where m.id=%s
                        limit '''+str(offset)+''','''+str(limit)+''';'''
            record = (moveId,)
    
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            
            result_list = cursor.fetchall()
            print(result_list)



            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
    
        return{'result':'seccess',
               'item':result_list,
               'count':len(result_list)},200
    





    

from flask import request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

from email_validator import validate_email,EmailNotValidError
from utils import check_password, hash_password

class MoviesResources(Resource):
    #모든 영화리스트 가져오기
    @jwt_required()
    def get(self):
        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')
        user_id = get_jwt_identity()
        try:
            connection = get_connection()
            query = '''select m.id,m.title,count(m.id) as reciew_count,if(avg(r.rating) is null,0,avg(r.rating)) as avg,
                        if(f.id is null,0,f.isLove) as isLove
                        from movie m
                        left join review r
                        on m.id=r.movieId
                        left join favorite f
                        on m.id=f.moviesId and f.userId= %s
                        group by m.id
                        order by '''+order+''' desc
                        limit '''+offset+''','''+limit+''';'''
            record =(user_id,)
        
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
        
        i =0
        for row in result_list:
            result_list[i]['avg']=str(row['avg'])
            i = i + 1
    
        return{'result':'seccess',
               'items':result_list,
               'count':len(result_list)},200
    #특정영화 검색
    def post(self):
        connection =get_connection()
        data = request.get_json()
        try:
            query = '''select m.title,count(m.id) as count,ifnull((r.rating),0) as avg
                        from movie m
                        left join review r
                        on r.movieId=m.id
                        where title like %s or m.summary like %s
                        group by m.id;'''
            record = (data['title'],data['title'])
    
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
    #특정영화 상세 설명
    @jwt_required(optional=True)
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
                result_list[i]['avg']=float(row['avg'])
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
    #특정영화 리뷰 갯수
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


class MovieSearchResource(Resource):
    #특정 영화 검색
    @jwt_required(optional=True)
    def get(self):
        keeyword=request.args.get('keeyword')
        offset=request.args.get('offset')
        limit=request.args.get('limit')

        try:
            connection =get_connection()
            query = '''select m.title,m.summary,count(m.id) as count,ifnull((r.rating),0) as avg
                        from movie m
                        left join review r
                        on r.movieId=m.id
                        where title like '%'''+keeyword+'''%' or m.summary like '%'''+keeyword+'''%'
                        group by m.id
                        limit '''+offset+''','''+limit+''';'''
    
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,)
            
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


    

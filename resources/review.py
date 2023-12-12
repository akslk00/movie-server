from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

class ReviewResources(Resource):

    @jwt_required()
    def post(self,moveId):
        data =request.get_json()
        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''insert into review
                        (movieId,userId,rating,content)
                        values
                        (%s,%s,%s,%s);'''
            record = (moveId,user_id,data['rating'],data['content'])

            cursor =connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
    
        return{'result':'seccess'},200
    
class MyReviewResources(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        try:
            connection = get_connection()
            query ='''select *
                        from review
                        where userId = %s;'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)
            
            result_list = cursor.fetchall()
            print(result_list)

            i =0
            for row in result_list:
                result_list[i]['createdAt']=row['createdAt'].isoformat()
                result_list[i]['updatedAt']=row['updatedAt'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()
        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return{'error':str(e)}, 500
        return{'result':'success',
               'items':result_list,
               'count':len(result_list)},200
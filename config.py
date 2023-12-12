
class Config:
    HOST='yhdb.c2cef2c1yefx.ap-northeast-2.rds.amazonaws.com'
    DATABASE='movie_db'
    DB_USER='movie_db.user'
    DB_PASSWORD='1010'
    

    PASSWORD_SALT ='yh1206hello'


    ### JWT 관련 변수 셋팅 => 셋팅후에는
    ### app.py 파일에서, 설정해줘야 한다.
    JWT_SECRET_KEY = 'yh1206hello##bye~~'
    JWT_ACCESS_TOKEN_EXPIRES = False
    #access_token을 만들때 유효기간을 가지게 만들경우
    #JWT_ACCESS_TOKEN_EXPIRES = True
    PROPAGATE_EXCEPPTIONS = True
import cx_Oracle


#通用查询
def select(sql, ORACLE_CONNECT):
    try:
        conn = cx_Oracle.connect(ORACLE_CONNECT)
        curs = conn.cursor()
        curs.execute(sql)
        resurt = curs.fetchall()
        curs.close()
        conn.close()
        return resurt
    except Exception as e:
        return "查询出现异常，请检查sql语句和连接字符串", e


# 其他通用修改方法
def update(sql, ORACLE_CONNECT):
    try:
        conn = cx_Oracle.connect(ORACLE_CONNECT)
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception as e:
        return "执行异常，请检查sql语句和连接字符串", e


def insert(sql, ORACLE_CONNECT):
    try:
        conn = cx_Oracle.connect(ORACLE_CONNECT)
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception as e:
        return "执行异常，请检查sql语句和连接字符串", e


def delete(sql, ORACLE_CONNECT):
    try:
        conn = cx_Oracle.connect(ORACLE_CONNECT)
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception as e:
        return "执行异常，请检查sql语句和连接字符串", e


if __name__ == '__main__':
    print("Welcome to qamanage")
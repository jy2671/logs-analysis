#!/usr/bin/env python

import psycopg2


def db_connnect():
    # create and return a database connection and cursor
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    return cursor, conn


def db_disconnect():
    # disconnect connection
    cursor, conn = db_connnect()
    cursor.close()
    del cursor
    conn.close()


def execute_query(query):
    # execute_query returns the results of an SQL query
    cursor, conn = db_connnect()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as error:
        print('error execute_query "{}", error: {}'.format(query, error))
        return None
    finally:
        db_disconnect()


def print_top_articles():
    # Print out the top 3 articles of all time.
    query = ("""
        SELECT a.title, a.slug, count(*) as num
        FROM log l, articles a
        WHERE a.slug = substring(l.path, 10, 34)
        GROUP BY (a.slug, a.title)
        ORDER BY num desc limit 3;
        """)

    results = execute_query(query)

    # loop over each row
    print
    print("Results for question 1 - "
          "What are the most popular three articles of all time?")
    print
    for result in results:
        print(' "{}" - {} views'.format(result[0], result[2]))
    print


def print_top_authors():
    # Print out a list of authors ranked by article views.

    query = ("""
        SELECT au.name, count(*) as num
        FROM log l, articles a, authors au
        WHERE a.slug = substring(l.path, 10, 34) AND au.id = a.author
        GROUP BY (au.name)
        ORDER BY num desc;
        """)

    results = execute_query(query)

    # loop over each row
    print
    print("Results for question 2 - "
          "Who are the most popular article authors of all time?")
    print
    for result in results:
        print result[0],  " - ", result[1], "views"
    print


def print_errors_over_one():
    ''' print out the error report.

    This function prints out the days and that day's error percentage
    where more than 1% of logged access requests were errors
    '''
    query = ("""
        SELECT to_char(lt.time, 'FMMonth dd, yyyy') as date,
        round(((l.sum404/(lt.total*1.00))*100),1) as num
        FROM log_total lt, log_404 l
        WHERE lt.time = l.time AND ((l.sum404/(lt.total*1.00))*100)>1;
        """)

    results = execute_query(query)

    # loop over each row
    print
    print("Results for question 3 - "
          "On which days did more than 1% of requests lead to errors?")
    print
    for result in results:
        print('{} - {}% errors'.format(result[0], result[1]))
    print


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_errors_over_one()

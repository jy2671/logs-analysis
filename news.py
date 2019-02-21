import psycopg2

conn = psycopg2.connect("dbname=news")

cursor = conn.cursor()
cursor.execute("select a.title, a.slug, count(*) as num from log l, articles a where a.slug = substring(l.path, 10, 34) group by (a.slug, a.title) order by num desc limit 3;")

results1 = cursor.fetchall()

#print "Row data:"
#print results

#loop over each row
print
print "Results for question 1 - What are the most popular three articles of all time?"
print
for result1 in results1:
	#print " ", "\"", result1[0], "\"", " - ", result1[2], "views"
	print " ", ('"%s"' % result1[0]), " - ", result1[2], "views"
print


cursor.execute("select au.name, count(*) as num from log l, articles a, authors au where a.slug = substring(l.path, 10, 34) and au.id = a.author group by (au.name) order by num desc;")

results2 = cursor.fetchall()

#loop over each row
print
print "Results for question 2 - Who are the most popular article authors of all time?"
print
for result2 in results2:
	print " ", result2[0],  " - ", result2[1], "views"
print

cursor.execute("select to_char(lt.time, 'Month dd, yyyy') as date, round(((l.sum404/(lt.total*1.00))*100),1) as num from log_total lt, log_404 l where lt.time = l.time and ((l.sum404/(lt.total*1.00))*100)>1;")

results3 = cursor.fetchall()

print
print "Results for question 3 - On which days did more than 1% of requests lead to errors?"
print
for result3 in results3:
	print " ", result3[0], " - ", "{0:.1f}%".format(result3[1]), "errors" 
print

conn.close
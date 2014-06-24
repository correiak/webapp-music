#!/usr/bin/python

import MySQLdb

conn = MySQLdb.connect(db="django_music", user="correiak", passwd="password", host="localhost")
cursor = conn.cursor()

f = open("initial_import.txt", "r")
songs = []

for line in f:
	line = line.strip().split("\t")
	
	for i in range(1, len(line)):
		if line[i] not in songs and line[i] != "":
			songs.append(line[i])
		else:
			continue

f.close()

q = """INSERT INTO songs_song (title, source_id) VALUES """
for song in songs:
	val = """("%s", %s),""" %(song, 1)
	q += val

q = q[:-1] + ";"

cursor.execute(q)
conn.commit()

cursor.close()
conn.close()

print "done"
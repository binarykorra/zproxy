#! /usr/bin/env python
import socket, sys
from thread import *


try:
	lp = int(raw_input("[*] Listener:"))
except KeyboardInterrupt:
	print("\n[*] Disturbed!")
	sys.exit()

def start(lp):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', lp))
		s.listen(5)
		print("[*] OK: 200")
	except Exception, e:
		print("[*] FAILED: 404")
		sys.exit(2)

	while(1):
		try:
			conn, addr = s.accept()
			data = conn.recv(4096)
			start_new_thread(conn_string, (conn,data,addr))
		except KeyboardInterrupt:
			s.close()
			print("[*] Signing Off!")
			sys.exit(1)
	s.close()
def conn_string(conn, data, addr):
	try:
		first_line = data.split("\n")[0]

		url = first_line.split(" ")[1]

		print("[*] Streaming Website: " + url)

		http_pos = url.find("://")
	
		if(http_pos == 4):
			temp = url
			print("[*] Running on Port 80.")
			port = 80
		elif(http_pos == -1):
			temp = url[(http_pos+3):]
			print("[*] Running on Port 443.")
			port = 443
		proxy_server(url, port, conn, addr, data)
	except Exception, e:
		pass
def proxy_server(webserver, port, conn, data, addr):
	print(webserver)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((webserver, port))
		s.send(data)
		while(1):
			reply = s.recv(4096)
			if(len(reply) > 0):
				conn.send(reply)
				dar = float(len(reply))
				dar = float(dar / 1024)
				dar = "%.3s" % (str(dar))
				dar = "%s KB" % (dar)
				print("[*] Request Done: %s => %s <=" % (str(addr[0]),str(dar)))
			else:
				break
		s.close()
		conn.close()
	except socket.error, (value, message):
		s.close()
		conn.close()
		sys.exit(1)
start(lp)

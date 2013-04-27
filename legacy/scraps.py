
		else:
			raise Exception("Currently, a valid range is required.")
			range_dec = data_in[0].strip()

			if(range_dec=="num"):
				self.gen_min = ord("0")
				self.gen_max = ord("9")
			elif(range_dec=="letter"):
				self.gen_min = ord("A")
				self.gen_max = ord("z")
			elif(range_dec=="uppercase"):
				self.gen_min = ord("A")
				self.gen_max = ord("Z")
			elif(range_dec=="lowercase"):
				self.gen_min = ord("a")
				self.gen_max = ord("z")
			elif(range_dec=="symbol"):
				self.gen_min = ord("!")
				self.gen_max = ord("/")
			else:
				self.gen_min = gen_max = ord(range_dec)

		if(len(data_in) > 1):
			value = data_in[1]
			try:
				self.gen_repeat = int(data_in[1])
			except ValueError:
				print "Invalid value '"+data_in[1]+"' for range generation"
				raise
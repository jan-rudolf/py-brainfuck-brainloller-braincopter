def copter_encode (value, r, g, b):
	i = 0
	while (((65536 * r + 256 * g + b) % 11) != value):
		r += 1
		g += 1
		b += 1
		i += 1
	return (i, r, g, b)


i,r,g,b = copter_encode (3, 252, 246, 170)

print("pocet iteraci {}, ({},{},{})".format(i,r,g,b))

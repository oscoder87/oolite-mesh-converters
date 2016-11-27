#!/usr/bin/python 

""" 
This script takes a .dat file from the Elite/Oolite source 
and exports a .obj file containing the same geometry. 

Material for the faces is created from the dat file.
Only 1 texture can be handled at this time.

""" 

import sys, string, math

def tex_index(tex, vts):
	"""function that retrurns the first index in a list that
matches the tex provided
"""
	for i in range(len(vts)):
		if vts[i]==tex:
			return i
	return -1

# here the main program

inputfilenames = sys.argv[1:] # list of filenames provided
print("converting...", inputfilenames)

for inputfilename in inputfilenames: # for each file provided 1
	outputfilename = inputfilename.lower().replace(".dat",".obj") 
	materialfilename = inputfilename.lower().replace(".dat",".mtl") 
	mtllibname = materialfilename.split("/")[-1]
	objname=mtllibname.replace(".mtl","")
	texname=objname+'_auv'
	inputfile = open(inputfilename,"r") 
	lines = inputfile.read().splitlines(0) 

	mode = 'SKIP' 
	vertex_lines_out = [] 
	tex_lines_out = [] 
	faces_lines_out = ['g '+objname+'_'+texname+'\n'] 
	faces_lines_out.append ('usemtl '+texname) 
    
	n_verts = 0 
	n_faces = 0 
	skips = 0 
	vertex=[] 

	texfile=''
	vts=[]
	texForFace={}
	texErr=0

	for line in lines: #1
		if (line[:8] == 'TEXTURES'): #2
			mode = 'TEXTURE' #3
		if (mode == 'TEXTURE'):#2
			tokens = line.split('\t')	# split line by tabs 3
			if (len(tokens) > 3):#3
				if texfile == '':#4
					texfile=tokens[0]#5
				else:#4
					if tokens[0] != texfile:#5
						print('')#6
						print(inputfilename,': more than 1 texture, cannot convert. Use Dat2Obj instead.')
						print('')
						texErr=1
						break

				points = tokens[2:]#4
				tff=[]
				for point in points:
					v=point.split()#5
					vt = ('%.6f %.6f' % (float(v[0]),1-float(v[1])))
					if not(vt in vts):
						vts.append(vt)#6
						tex_lines_out.append('vt '+vt+'\n')
					tff[len(tff):]=[tex_index(vt, vts)]#5
				texForFace[n_faces]=tff#4
				#print tff
				n_faces=n_faces + 1
	if texErr==0:#1
		n_faces=0#2
		for line in lines: 
			if (mode == 'VERTEX'): #3
				coordinates = line.split(',')   # split line by commas 4
				if (len(coordinates) == 3): 
					n_verts = n_verts + 1 #5
					x = -float(coordinates[0]) 
					y = float(coordinates[1]) 
					z = float(coordinates[2]) 
					vertex.append( (x, y, z) ) 
					vertex_lines_out.append('v %.6f %.6f %.6f\n' % ( x, y, z)) 
					vertex.append( (x, y, z ) ) 
			elif (mode == 'FACES'): #3
				tokens = line.split(',')   # split line by commas 4
				if (len(tokens) > 9) : 
					color_data = tokens[0:3] #5
					normal_data =tokens[3:6] 
					n_points = tokens[6] 
					point_data = tokens[7:] 

					faces_lines_out.append ('\nf ') 
					for i in range( 0,int(n_points)) :
						faces_lines_out.append ('%i/%i/ ' % (int(point_data[i])+1,texForFace[n_faces][i]+1))#6
					n_faces = n_faces + 1 #5
				# 

			elif (mode == 'SKIP'): #3
				skips = skips + 1 #4
			# 
			if (line[:6] == 'NVERTS'): #3
				mode = 'SKIP' #4
			if (line[:6] == 'NFACES'): #3
				mode = 'SKIP' #4
			if (line[:6] == 'VERTEX'): #3
				mode = 'VERTEX' #4
			if (line[:5] == 'FACES'): #3
				mode = 'FACES' #4
			if (line[:8] == 'TEXTURES'): #3
				mode = 'TEXTURE' #4
			# 
		outputfile = open(outputfilename,"w") #2
		outputfile.write('# Exported with Dat2ObjTex.py (C) Giles Williams 2005 - Kaks 2008\n') 
		outputfile.write('mtllib %s\n' % mtllibname) 
		outputfile.write('o '+objname+'\n')
		outputfile.write('# %d vertices,' % n_verts) 
		outputfile.write(' %d faces\n' % n_faces) 
		outputfile.writelines(vertex_lines_out) 
		outputfile.writelines(tex_lines_out) 
		outputfile.writelines(faces_lines_out) 
		outputfile.writelines('\n\n') 
		outputfile.close(); 

		materialfile = open(materialfilename,"w") 
		materialfile.write('# Exported with Dat2ObjTex.py (C) Giles Williams 2005 - Kaks 2008\n') 
		materialfile.write('newmtl '+texname+'\nNs 100.000\n') 
		materialfile.write('d 1.00000\nillum 2\n') 
		materialfile.write('Kd 1.00000 1.00000 1.00000\nKa 1.00000 1.00000 1.00000\n') 
		materialfile.write('Ks 1.00000 1.00000 1.00000\nKe 0.00000e+0 0.00000e+0 0.00000e+0\n') 
		materialfile.write('map_Kd '+texfile+'\n\n') 
		materialfile.close();
		print(inputfilename+"->"+outputfilename+" & "+materialfilename)

print("done")
print("")
# 
#   end 
# 

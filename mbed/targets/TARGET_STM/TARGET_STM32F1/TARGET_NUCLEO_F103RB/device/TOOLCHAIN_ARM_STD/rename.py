import os;

def rename():
	path=".\\"
	
	filelist=os.listdir(path)	#获取该文件夹下所有的文件
	for files in filelist:		#遍历所有文件
		olddir=os.path.join(path,files);	#原来的文件路径
		if os.path.isdir(olddir):			#如果是文件夹则跳过
			continue;
		filename=os.path.splitext(files)[0];	#文件名
		filetype=os.path.splitext(files)[1];	#文件拓展名
		print("类型为:%s %s" % (filename,filetype))
		#litt='.s'
		if filetype!='.s':
			continue;
		newdir=os.path.join(path,filename+".S");	#新的文件路径
		os.rename(olddir,newdir);				#重命名
		
rename();
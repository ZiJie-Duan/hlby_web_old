import os
import uuid
import piexif
from PIL import Image
import requests

def getfilenamelist():
	print("正在生成图片名称列表")
	gzlj = os.path.realpath(__file__) 
	gzlist = gzlj.split("/")
	gzlist.remove("upload_mac.py")
	gzlist.remove("")
	gzljx1 = "/".join(gzlist)
	lj = "/" + gzljx1


	newname_list = []
	name_list = []

	for root, dirs, files in os.walk(lj):
		name_list = files

	rename_list = []
	listzc1 = []

	for x in name_list:
		if x == "upload_mac.py":
			print("去除程序本体在列表中")
		else:
			a = lj + "/" + x
			listzc1.append(a)

			uid = str(uuid.uuid4())
			b = lj + "/" + uid + ".jpg"
			listzc1.append(b)
			uidx = uid + ".jpg"
			newname_list.append(uidx)

			rename_list.append(listzc1)
			listzc1 = []

	return rename_list, newname_list


def renamefile(lista):
	print("正在重命名图片")
	new_name_list = []

	for oldname,newname in lista:
		os.rename(oldname,newname)
		new_name_list.append(newname)

	return new_name_list


def changejpgexif(listb):
	print("开始移除照片其他信息")
	for x in listb:
		try:
			zc = 1

			exif_dict = piexif.load(x)

			if exif_dict is not None:
				print("已检测照片属性")
				if exif_dict["0th"][274] == 3:
					zc = 3
					print("照片旋转参数为3")

				if exif_dict["0th"][274] == 6:
					zc = 6
					print("照片旋转参数为6")

				if exif_dict["0th"][274] == 8:
					zc = 8
					print("照片旋转参数为8")

				im = Image.open(x)

				exif_dict["0th"][274] = 1

				bit = piexif.dump(exif_dict)

				if zc == 3:
					im = im.transpose(Image.ROTATE_180)

				if zc == 6:
					im = im.transpose(Image.ROTATE_270)

				if zc == 8:
					im = im.transpose(Image.ROTATE_90)

				im.save(x, exif=bit,quality=95)
		except:
			print("图片未检测到附加属性")

		else:
			print("图片未检测到附加属性")


def update_jpg(listc):

	for x in listc:
		url = "https://haileybury.top/api/upload/"
		newname = x.split('\\')
		s = newname[len(newname)-1]

		files = {'file':(s,open(x,'rb'),'image/jpg')}
		#files = {'file':(s,open(r"C:\Users\lucycore\Desktop\IMG_0810.JPG",'rb'),'image/jpg')}

		r = requests.post(url,files = files, verify=False)
		result = r.text
		print(result)


def apiput():

	actname = input("活动名称：")
	actms = input("活动描述：")
	actfil = input("uuid(随机标记符):")

	a, wnl = getfilenamelist()
	b = renamefile(a)
	changejpgexif(b)

	wnln = "!".join(wnl)

	hostsend = "https://haileybury.top/api/?config=" + actname + "*" + actms + "*" + actfil + "*" + wnln

	response = requests.get(hostsend, verify=False)

	
	update_jpg(b)



apiput()
print("程序运行完成！")
input()
#os.rename()
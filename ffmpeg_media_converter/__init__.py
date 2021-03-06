"""
用途
	将一个文件夹下**指定扩展名（可指定多个）**的**所有**媒体文件转换为**指定**的格式

原理
	调用 ffmpeg 进行转换，故必须要在环境变量中设置 ffmpeg

缺陷
	无法转换 ffmpeg 不支持的文件
	无法自定义更多参数，只能让 ffmpeg 自行决定或者使用 ffmpeg 的默认值（具体情况取决于 ffmpeg）
	delete 方法删除文件时只能通过判断相同文件名、对应扩展名的文件是否存在而决定是否删除，无法判断是否转换成功，若转换失败但对应文件存在，源文件也会被删除
		- 解释：假设文件夹下存在 a.gif ，试图转换为 a.png ，转换失败了，但是 a.png 被创建了，delete 方法检测到 a.png 存在就会删除 a.gif
		- 判断的文件名的依据：文件名与源文件一致，如源文件为 a 那么就判断是否存在 a ，扩展名为设置的 toExt ，如设置了 .png 则判断是否存在 a.png，若存在则删除 a.gif
		- 可能被删除的文件的扩展名必须在在 extensions 列表中

类
	`Image` 用于转换图片，默认源扩展名列表可通过 `.image` 获取，默认转换至的扩展名为 `.webp`
	`Audio` 用于转换音频，默认源扩展名列表可通过 `.audio` 获取，默认转换至的扩展名为 `.webm`
	`Video` 用于转换图片，默认源扩展名列表可通过 `.video` 获取，默认转换至的扩展名为 `.webm`
	其实三个 class 代码都非常类似，功能完全一致
	不同的仅仅是默认源扩展名列表和默认转换至的扩展名
	三个类完全可以互换，只要源扩展名列表和转换至扩展名配置正确即可

实例方法
	`convert`
		- 遍历指定的文件夹，调用 ffmpeg 转换扩展名在源扩展名列表中的文件至配置的扩展名
		- 由于此方法要调用 ffmpeg ，请确保 ffmpeg 已加入环境变量
	`delete`
		- 将遍历文件夹，删除满足条件的文件
		- 此方法无需 FFmpeg
		- 无法单独保留某个文件，满足条件的将会全部删除
		- 条件：
			- 扩展名在源扩展名列表中
			- 缺陷 3 中介绍到的判断规则
"""

from .Converter import Converter
from .extensions import image, audio, video

def dealParams(root, extensions, toExt):
	if str(type(extensions)) == "<class 'int'>":
		extensions = [str(extensions)]
	elif str(type(extensions)) == "<class 'str'>":
		extensions = [extensions]
	elif str(type(extensions)) == "<class 'NoneType'>":
		extensions = []
	return [str(root), list(extensions), str(toExt).lower()]

class All(Converter):
	def __init__(self, extensions, toExt, root='.'):
		self.root, self.extensions, self.toExt = dealParams(root, extensions, toExt)

class Image(Converter):
	def __init__(self, root='.', extensions=image, toExt='.webp'):
		self.root, self.extensions, self.toExt = dealParams(root, extensions, toExt)

class Audio(Converter):
	def __init__(self, root='.', extensions=audio, toExt='.webm'):
		self.root, self.extensions, self.toExt = dealParams(root, extensions, toExt)

class Video(Converter):
	def __init__(self, root='.', extensions=video, toExt='.webm'):
		self.root, self.extensions, self.toExt = dealParams(root, extensions, toExt)
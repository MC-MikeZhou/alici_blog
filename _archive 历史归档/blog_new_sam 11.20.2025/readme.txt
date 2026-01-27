
项目说明：
你需要为网站生成页面的内容（json数组）。核心是服务于页面AEO和SEO。

网站的内容是：
alici.ai正在建立自己的blog系统，初步设想包含3个部分：alici news（新功能上新介绍）、tutorial（热门ai工具的使用、热门关键词相关的教程等）、一些list推荐（比如最好用的ai video模型介绍、最好用的ai thumbnail工具等等。）
项目目标：服务于网站的SEO和AEO。创建有品质的内容，提升alici网站在google搜索上的权重。关键词和长尾关键词的尽可能覆盖，提升网站本身的增长。


单个blog的详情页的内容样式，请看图：./doc/blog.png
blog生成的素材来源：
纯文本素材：./input/ 里面的txt文本。  可同时放入多个文本 （如果发现./input/ 不存在，创建一个）
图文素材： notion的公开网页链接 和 其他链接。  可同时提供多个url


最终你生成的内容是一个json数组， 一个元素就是一篇文章blog。 
这是一个完善模版示例：./doc/blog.json




字段说明
slug: 网站地址，前缀是alici.ai/blog/slug
title：blog文章的标题
TLNR：首屏摘要，面向AEO快速理解文章本身，比如：解决什么场景、适配哪些平台、1句话亮点（AEO视角，有核心关键词、有长尾关键词）
sub_title: blog文章的副标题
cover: 博客封面，是个链接，需要生成，具体要求参考【待补充】文件
cover:alt ： 需要根据博客内容本身的定位，设计文案，让seo和aeo能更好增强理解
date：默认是创建这个文章的时间，除非用户指定其他时间
main_category: 从3类中选择：news、tutorial、list
category_for_recommend: 推荐关联blog文章，从上述3类中选择
read_time: 基于这篇文章的长度，推测看完这篇文章要花费的时间（单位是“分钟”）
CTA_alici_link：展示在blog hero区域（标题区域）的一个按钮，一般是跳转到alici相关功能区域。默认值是alici.ai。每次任务启动前，需要向用户确认
CTA button: 同上的位置，展示在按钮上的文案，默认是Try It NOW。 可以向用户确认是否有其他要求
article_body_content：文章正文。正文是某种framer cms的html相关的格式。示例中这个字段里，基本涵盖所有支持的格式（6号标题、正文、子弹、序号、表格、链接、图片等）。如果正文中有图片，要求见文档【待补充】
meta_title：用于SEO，写在网站页面用于搜索展示的Title
meta_description：用于SEO，写在网站页面用于搜索展示的description，可以在TLNR的基础上做SEO/AEO增强
tag_for_SEO：基于博客文章提取4-6个关键词。逗号分隔。参考./doc/blog.json中对应的字段


生成字段过程中，一定要参考示例 ： ./doc/blog.json中对应的字段填写格式，不要将string 填成数组。
填写的内容以提升网站SEO为目标。 

注意：
1  ./gen_images/ 文件夹只能存放图片
2  整个流程过程中，生成的临时文件，除了我指定位置的文件，其余的都必须放在./tmp/ 文件夹中。里面有可能保留着之前项目的临时文件，不要混淆。在询问阶段结束，流程开始前，可以考虑情况./tmp/
（./tmp/不存在就创建一个）
3  网页爬取，正常方式爬取不到时，才尝试  https://r.jina.ai/${url} 的方式。



工作流程：
1  确认生成blog 属于哪个分类
从3类中选择：news、tutorial、list

2  确认生成blog的原始素材。
./input/ 中的所有txt文本。
用户提供的链接。
都可以作为原始素材。可以同时多个组合
在执行下一步之前，你需要输出跟用户确认。列出你目前看到的素材。


3  确认素材后，检索查看素材和链接。并输出素材的可用性。比如url无法爬取，就需要提示用户是否还要继续。


4  询问用户blog文章，
——是否由你来帮忙，根据源素材上下文来决定，是否需要配图。
——还是由用户指定，是否需要AI配图。

不需要则跳过
如果需要，下面有具体的生图方式和流程：
创建临时图片文件夹 ./gen_images/ ， 如果已存在，清空文件夹。
创建 ./tmp_image.json ，是一个空字典，用来关联本地图片和它的云端链接。如果已存在，使用空字典覆盖。

以下是生图api，供参考：
const falKey = 'b5ea47d3-5d30-4423-b9c9-85a185752042:828167dcf4beacefd4df6b3b4d03e99f'
response=$(curl --request POST \
  --url https://queue.fal.run/fal-ai/nano-banana \
  --header "Authorization: Key $falKey" \
  --header "Content-Type: application/json" \
  --data '{
     "prompt": "",
     "num_images": 1,
     "aspect_ratio": "x:x",   //生图支持比例请查看： ./doc/image_ratio.png   尽量生成宽大于高的图，如2:1  16:9
     "output_format": "png",
     "sync_mode": false
   }')
REQUEST_ID=$(echo "$response" | grep -o '"request_id": *"[^"]*"' | sed 's/"request_id": *//; s/"//g')

这是异步接口，只能获取到requestId，然后还要通过获取结果api来得到这个requestId的生成结果，需要轮询。
这个链接有详细的生图 api 使用方式 ：https://fal.ai/models/fal-ai/nano-banana/api


生成一张图片后存入 ./gen_images/文件夹， 图片使用英文命名，${image_name}.png
 同时在./tmp_image.json记录一下，
按下面的形式，
{
	${image_name1} : https://ct2.alici.ai/static/image/other/gen_images/ + ${image_name1}.png,
	${image_name2} : https://ct2.alici.ai/static/image/other/gen_images/ + ${image_name2}.png,
}

所有图片完毕后，进行批量上传图片获得url。上传方式：
ssh命令：
rsync -a -r -v -p -e 'ssh -p 22'  --exclude='.DS_Store'  --progress ${项目绝对路径}/gen_images root@45.76.70.215:/var/www/static/static/image/other/
password:  5A_p@cjpX74H(LJM
需要获取此项目的绝对路径，然后拼接上相对路径。

补充配图的原则：
——文章头部不需要配图。
——在文章中间可添加配图，但不要和源素材网页本身自带的配图冲突




5 根据用户提供的原始素材，生成中文预览的图文blog，用html格式。保证用户能用浏览器打开，看到图文样式。 

注意：对于原素材中如果有图片，一定要保留这些图片。比如链接网页有图文，图片必须保留。
比如notion 链接网页的图片，就可能是下面的格式：
![Image 1](https://confirmed-dry-356.notion.site/image/attachment%3Aa58acf28-
  94f7-4da8-8aba-4ea039cc6348%3Aimage2.png?table=block&id=2b0a03e6-
  1954-81a5-9d42-f2162e787a13&spaceId=563bbd41-df20-42ae-bd04-
  eb3f6a7a5e6f&width=1600&userId=&cache=v2)
其他url，可能是传统img标签。总之，要检测富文本可能的图片格式，无论是markdown还是html。
对于AI生成的配图，将它们的云链接合理的插入到对应的上下文位置。

生成内容的规则，请按不同分类查看文档：
./doc/4_Tutorial类内容规范.md
./doc/5_List类内容规范.md
./doc/6_News类内容规范.md
生成路径为  ./chinese_preview.html （如果路径已存在文件，覆盖它）
然后等待用户确认 预览版是否ok。
如果需要修改，按用户要求调整预览结果。



6  预览版通过用户审核后，为blog的生成封面图片（对应到最终json数组中，单个元素的item.cover 字段）
生成方式和上传获取链接的方式参考步骤4。
封面的比例用 16:9


7  生成最终的json数组。
本次生成的blog数据，是数组中的一个元素。生成字段过程中，一定要参考示例 ./doc/blog.json中对应的字段填写格式，不要将string 填成数组。
内容必须是全英文。需要你根据前面生成预览版的上下文来完成各个字段的填写，注意是为了SEO AEO服务。

关于blog正文的内容，你前面输出的是中文预览版，需要换成英文版。 
参考输出示例：./doc/blog.json ， 其中数组元素 item.article_body_content 填入的就是blog正文的内容。你需要参考它的html格式填写进去。而不是中文预览版的html格式。

最终输出： ./output/${title}_${时间戳}_output.json  (title：blog文章英文标题)
如果./output 文件夹不存在，创建一个。










   

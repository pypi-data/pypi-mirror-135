<div align="center"><img src="https://gitee.com/cyrxdzj/PyCheer/raw/master/PyCheer/logo/logo.png" alt="logo"></div>

## 一、前言

PyCheer是一个代码编辑器，基于flask，支持在浏览器端（不一定要在同一台机器上，但必须互相联网）访问，为只用终端而没有桌面环境的服务器提供代码编辑帮助。同时也支持 Markdown的编辑。

## 二、安装

请输入以下命令以安装：

```bash
pip install PyCheer
```

## 三、启动

进入对应目录后，请输入以下命令（二选一）启动：

```bash
pycheer run
python -m PyCheer run
```

此时，PyCheer会输出一行蓝色字体（部分终端不支持颜色），代表Token（在进入网页时需要使用），请复制下来。

使用浏览器访问：

```
http://localhost:1111
```

将Token粘贴进输入框里，即可开始使用PyCheer。

对于没有复制功能的终端，请输入以下命令启动：

```bash
pycheer run -b
```

其中 `-b` 参数代表“自动启动浏览器”。

如果1111端口已被占用或你想同时启动多个PyCheer，请加上 `-p <端口>` 参数以指定启动端口。

## 四、基础使用

#### 1、基本页面与操作

如图：

![终端控制台界面](https://images.gitee.com/uploads/images/2021/0720/144252_42dda5e4_7354699.png "屏幕截图.png")

其中，蓝色字体为Token，绿色字体为网页地址。

然后再访问第一个网址，结果如图：

![首页](https://images.gitee.com/uploads/images/2021/0819/134609_fd2376b4_7354699.png "屏幕截图.png")

此时，您可以查看当前目录下的文件。

也可以访问 `localhost:<端口，默认为1111>` ，然后在如图输入框中输入Token或解锁密码，点击“确定”。

![锁定页面](https://images.gitee.com/uploads/images/2021/0819/134642_174bdd3c_7354699.png "屏幕截图.png")

点击一个文件夹可以进入这个文件夹，点击一个文件可以打开或编辑这个文件。

目前支持编辑的文件：

|文件后缀|文件类型|
|:--:|:--:|
|`.py`|Python 源文件|
|`.html`|HTML 源文件|
|`.js`|JavaScript 源文件|
|`.css`|CSS 样式文件|
|`.md`|Markdown 文件|
|`.txt`|文本文档|
|`.c`|C语言源文件|
|`.cpp`|C++语言源文件|
|`.h`|C/C++语言头文件|
|`.hpp`|C/C++语言头文件|
|`.json`|JSON文件|
|`.java`|Java语言源文件|

支持查看（但不支持编辑）的文件：

|文件后缀|文件类型|
|:--:|:--:|
|`.png`|PNG 图像文件|
|`.jpg`|JPG 图像文件|
|`.jpeg`|JPEG 图像文件|
|`.mp3`|MP3 音频文件（播放时可能会有亿点点诡异）|

对于其它类型的文件，则会根据设置打开。如果这恰好是二进制文件，就会报500 Internal Server Error错误。

#### 2、退出

在右上角有一个“退出PyCheer”按钮，可以暂时退出（但不会关闭）PyCheer。再次输入Token或解锁密码即可再次进入PyCheer。

#### 3、关闭

点击“关闭PyCheer”按钮即可关闭PyCheer服务。

#### 4、编辑文件

点击支持编辑的文件，即可进入编辑页面。

![编辑页面图片](https://images.gitee.com/uploads/images/2021/0716/203400_3140499c_7354699.png "屏幕截图.png")

如图，中间为代码编辑区，可以编辑代码。

下方为状态栏，指示当前状态。一旦代码被编辑，状态栏就会有所改变。

编辑完毕后，记得点击“保存”！

#### 5、新建文件（夹）

在目录页面中点击“新建文件（夹）”按钮，即可新建文件（夹）。

#### 6、重命名文件

点击目录页面中文件名右边的图标，即可进行重命名。

如果操作迟迟没有返回结果（比如，保存时状态栏一直显示“保存中，请稍后”），那多半就是出了BUG。一般情况下，您可以查看服务终端控制台或浏览器Console。

您也可以[提交ISSUE](https://gitee.com/cyrxdzj/PyCheer/issues)，帮助我们修复此问题。

## 五、进阶使用：Git版本控制系统

从PyCheer 1.0.2版本开始支持Git版本控制系统。

需要注意，如果在启动PyCheer时出现如下输出：

```
Failed to introduce Git module. This may be because Git is not installed on your computer.
If you don't want to start Git using PyCheer, you can ignore this information.
```

则说明PyCheer引入Git时失败了，有可能是Git未安装，也有可能是其他原因。

如果PyCheer检测到启动目录下存在.git` 文件夹并且引入模块成功，则会在目录页面右上角显示“启动Git”按钮。点击即可启动Git。

如图：

![Git版本控制系统](https://images.gitee.com/uploads/images/2021/0720/144744_cf281937_7354699.png "屏幕截图.png")

![Git版本控制系统](https://images.gitee.com/uploads/images/2021/0720/144811_13faf49e_7354699.png "屏幕截图.png")

#### 1、暂存与提交：文件编辑信息

如果文件被编辑，使用 `git status` 命令即可查看。而信息框显示的，就是该命令的输出。

点击“刷新”可以刷新状态。

点击“将所有已编辑的文件移至暂存区”相当于执行 `git add .`。

点击“提交”，即可提交文件。需要注意，暂不支持多行提交信息。此按钮相当于执行 `git commit -m "<提交信息>"`。

#### 2、本地分支：本地分支信息

这个板块显示与本地分支，绿底白字的为当前所在的分支，白底黑字的为可以切换的分支。

点击分支右边的“切换”图标即可切换分支。相当于执行 `git checkout <分支名>`。

 **需要注意，在文件已编辑但未提交的情况下，不可以切换分支。**

点击“在当前分支的基础上新建本地分支”，即可新建一个分支。注意，请确认当前所在的分支，再进行此操作。

#### 3、远程仓库：远程分支信息

这个板块显示与远程仓库有关的信息。

这里显示了所有远程分支，相当于 `git remote`。每个远程分支有3个按钮，分别代表“推送”“拉取”“删除”。

比如，现在正在dev分支。

- 点击origin旁边的第1个按钮“推送”，相当于执行 `git push origin dev`。

- 点击origin旁边的第2个按钮“拉取”，相当于执行 `git pull origin dev`。

- 点击origin旁边的第3个按钮“删除”，相当于执行 `git remote remove origin`。

点击下方的“新建远程分支”可以连接到一个远程仓库，相当于执行 `git remote add <远程分支名> <URL>`。

推送或拉取都需要一定的时间，请耐心等待。

 **暂时不支持账号密码登录。请在本机上配置好SSH，并将SSH公钥在Gitee或Github上设置好后，再使用推送/拉取功能。** 

## 六、进阶使用：系统语言

请参阅同目录下的LANGUAGE.md。

## 七、进阶使用：PyCheer主题

请参阅同目录下的PYCHEERTHEME.md。

## 八、设置

从PyCheer 1.0.8版本开始支持设置。

目前，设置支持：

1. 编辑器样式。

2. 解锁密码。

3. 对于不支持的文本文件，采取何种方式打开？

4. 系统语言。

5. PyCheer主题。

## 九、花絮

#### 1、文件图标总览

进入 `seeicon` 页面，您就可以看到所有支持的文件图标总览。如图：

![文件图标总览](https://images.gitee.com/uploads/images/2021/0805/154732_99bba217_7354699.png "屏幕截图.png")

#### 2、hello 页面

进入 `hello` 页面，您就可以查看到关于当前PyCheer运行的有关信息和关于PyChee。

#### 3、首页

直接输入：pycheer，不带任何参数，你就可以看到关于PyCheer的一些信息。

#### 4、版本

输入 `pycheer version` 可以查看PyCheer的版本。

##  十、赞赏与贡献

如果您认为此项目不错，给个Star并赞赏一下呗~

您可以[提交ISSUE](https://gitee.com/cyrxdzj/PyCheer/issues)以帮助我们修复问题，或提出改进建议。

您也可以将本项目克隆到本地，再进行修改后提交Pull Requests。

祝您使用愉快！

开源不易，赞赏一下呗~

![赞赏码](https://images.gitee.com/uploads/images/2021/0717/205650_6249d470_7354699.png "屏幕截图.png")
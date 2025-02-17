## 序言
在操作系统层面，I/O系统有文件、网络、标准输入输出、管道等，Java提供的I/O类库就是用来读写这些I/O系统的。

Java I/O 类库有两个：`java.io` 和 `java.nio`，本节主要介绍 `java.io`的分类及其作用。

### 输入流和输出流

- 输入流：`InputStream, Reader`
- 输出流：`OutputStream, Writer`

### 字符流和字节流

- 字符流：`Reader, Writer`
- 字节流：`InputStream, OutputStream`

#### 字节流和字符流的区别
字符流在读写I/O系统时，多了一个字符编码规则装换的环节。

如下例子，打开文件，可以看到`星期天`文本，使用16进制查看器，可以发现字符编码为`UTF8`。
```
//Java默认编码：UTF16
String str = "星期天";
//假设系统默认编码为：UTF8
Write write = new FileWriter("a.txt");
write.write(str);
write.close();
```
而字节流只需要组个字节写入，不需要进行字符编码规则装换。
```
FileOutputStream outputStream = new FileOutputStream("a.txt");
String str = "星期天";
byte[] strUTF8 = str.getBytes(StandardCharsets.UTF_8);
outputStream.write(strUTF8);
outputStream.close();
FileOutputStream outputStream = new FileOutputStream("a.txt");
```

### 原始类和装饰器类

#### 原始类
1. 文件：`FileInputStream FileOutputStream FileReader FileWriter`
2. 内存：`ByteArrayInputStream ByteOutputStream StringReader StringWriter CharArrayReader CharArrayWriter`

大部分情况下不需要用到，主要作用是兼容，比如调用第三方库的某个函数来处理byte数组，而函数只接受InputStreaml类型
```
byte[] bytes = "今天是个好日子".getBytes(StandardCharsets.UTF_8);
InputStream inputStream = new ByteArrayInputStream(bytes);
```
还有一个作用就是在写单元测试时用来替换文件I/O和网络I/O。

3. 管道：`PipedInputStream PipedOutputSteam PipedReader PipedWriter`

主要用于线程间通信
```
PipedOutputStream pipedOutputStream = new PipedOutputStream();
PipedInputStream pipedInputStream = new PipedInputStream(pipedOutputStream);

new Thread(() -> {
    try {
        pipedOutputStream.write("Hello World".getBytes(StandardCharsets.UTF_8));
    } catch (IOException e) {
        e.printStackTrace();
    }
}).start();

new Thread(() -> {
    try {
        byte[] buffer = new byte[1024];
        int len = pipedInputStream.read(buffer);
        System.out.println(new String(buffer, 0, len, StandardCharsets.UTF_8));
    } catch (IOException e) {
        e.printStackTrace();
    }
}).start();
```

4. 网络I/O：InputStream OutputStream：需要配合 `java.net` 类库一起使用

5. 标准输入输出

在操作系统中，一般有三个标准I/O系统：标准输入、标准输出、标准错误。

标准输入对应键盘，标准输出和错误对应屏幕。

```
//获取标准输入
Scanner scanner = new Scanner(System.in);
//将标准输入的一行输出到标准输出
System.out.println(scanner.nextLine());
//将标准输入的一行输出到标准错误
System.err.println(scanner.nextLine());
```

#### 装饰器类
1. 支持缓存功能的装饰器类：`BufferedInputStream BufferedOutputStream BufferedReader BufferedWriter`

- 默认缓存：8192 bit
- 作用：减少系统调用，提高读写性能

2. 支持基本类型数据读写的装饰器类：`DataInputStream DataOutputStream`
3. 支持对象读写的装饰器类：`ObjectInputStream ObjectOutputStream`
4. 支持格式化打印的装饰器类：`PrintStream PrintWriter`
5. 其他：`PushbackInputStream、PushbackReader、SequenceInputStream、LineNumberReader`

#### 类似装饰器的原始类
InputStreamReader 和 OutputStreamReader
```
OutputStream outputStream = new FileOutputStream("a.txt");
//指定字节流的编码
OutputStreamWriter outputStreamWriter = new OutputStreamWriter(outputStream, StandardCharsets.UTF_8);
outputStreamWriter.write("今天是个好日子");
```
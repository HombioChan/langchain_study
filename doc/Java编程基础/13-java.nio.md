## 序言
`JDK1.4`，`Java` 引入了 `java.nio`库，既然有了 [java.io](12-java.io.md) 库，为什么还要引入 `java.nio` 库呢，这两者有什么区别？

本节简单通过介绍`java.nio`引入的新特性：`channel、buffer、selector、异步channel` 来回答这个问题。

### Buffer
`Buffer`本质上是一块内存，相当于`java.io`编程时读取数据前申请的`byte[]`数组。

常见的 `Buffer` 有：`ByteBuffer CharBuffer ShortBuffer IntBuffer LongBuffer FloatBuffer DoubleBuffer MappedByteBuffer`，顾名思义，这些`Buffer`的不同之处就是解析数据的方式不同，比如`CharBuffer`以字符的形式解析数据，类似`java.io`中的字符流。

### Channel
不同于`java.io`的`Stream`，`Channel`既可以读，也可以写，常见的channel有：

- 文件读写：FileChannel
- 网络编程：DatagramChannel SocketChannel ServerSocketChannel

`Channel`有两种运行模式：阻塞和非阻塞。

#### 什么是阻塞模式，什么是非阻塞模式
线程在在调用read()和write()对I/O进行读写时，如果数据不可读或者不可写，在阻塞模式下，`read()`和`write()`会等待，直到读取到数据或者写入完成时才放回；在非阻塞模式下，read()和write()会直接返回，并报告读取和写入不成功。

> 网络，管道，标准输入输出才有阻塞和非阻塞两种模式，文件不存在不可读不可写的情况，所以没有非阻塞模式。

除了 read() 和 write()，accept()也支持阻塞和非阻塞模式。

非阻塞的`Channel`一般搭配`Selector`，用于实现非阻塞的多路复用I/O模型。

### Selector
如果不使用`Selector`，网络编程写出的非阻塞模式代码风格如下
```

ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
serverSocketChannel.configureBlocking(false);
SocketChannel client = null;
//线程非阻塞自旋，直到接受到一条连接
while (client == null) {
    client = serverSocketChannel.accept();
}

ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
//线程非阻塞自旋，直到读到输入流
while ((client.read(byteBuffer) == -1));

byteBuffer.flip(); // 从读模式切换到写模式
while (byteBuffer.hasRemaining()) {
    //echo，接收什么回复什么
    client.write(byteBuffer);
}
```
上述代码充斥着while循环，不是特别优雅，使用`Selector`可以解决这个问题
```
ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
serverSocketChannel.configureBlocking(false);

Selector selector = Selector.open();
serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    //其实线程自旋的逻辑封装到 select() 方法里面
    int count = selector.select();
    if (count == 0) {
        continue;
    }
    Set<SelectionKey> selectionKeys = selector.selectedKeys();
    Iterator<SelectionKey> iterator = selectionKeys.iterator();
    while (iterator.hasNext()) {
        SelectionKey selectionKey = iterator.next();
        if (selectionKey.isAcceptable()) {
            // 连接请求
        } else if (selectionKey.isReadable()) {
            // I/O可读
        } else if (selectionKey.isWritable()) {
            // I/O可写
        }
        iterator.remove();
    }
}
```
上述代码已经相对优雅，不过对于不熟悉I/O的人来说，使用 Selector 进行网络编程，难度还是比较大，实际上现在的网络编程多用 `Netty` 框架。

#### 什么是 I/O 多路复用
即一个线程监控多个网络I/O，当 I/O 可读、可写、或者有新连接到来的时候发起通知，执行相应的任务。可大大提高服务端的客户端可连接数。

#### I/O 多路复用的实现
`Selector` 只是 Java 对于底层 I/O 多路复用实现的抽象，不同的的平台的实现不一样

- Unix：epoll
- Windows：iocp
- BSD：kqueue

### 异步Channel
尽管程序可以通过 `Selector` 避免手写轮询代码，但是 `Selector` 的底层仍然使用轮询实现，如何才能真正避免轮询代码呢？

在`JDK7`，`Java`对`java.nio`库进行升级，引入了支持异步模式的Channel：`AsynchronousFileChannel、AsynchronousSocketChannel、AsynchronousServerSocketChannel`。

#### 什么是异步模式
线程调用一个方法，注册一个事件`handle`，当事件发生后，通知线程处理，期间线程可以去做其他的事情，或者什么也不做，这种模式称为异步模式。

```
AsynchronousServerSocketChannel serverChannel = AsynchronousServerSocketChannel.open();
serverChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
serverChannel.accept(null, new CompletionHandler<AsynchronousSocketChannel, Object>() {
    @Override
    public void completed(AsynchronousSocketChannel client, Object attachment) {
        // 处理连接请求
    }

    @Override
    public void failed(Throwable exc, Object attachment) {

    }
});
```

## 问题解答

### 为什么引入`java.nio`？

1. `java.io` 设计不太合理，`java.nio`通过多用组合少用继承的设计思想，实现更加优雅
2. `java.io` 只支持阻塞I/O，`java.nio`支持阻塞I/O、非阻塞I/O、异步I/O

### 什么时候用`java.nio`，什么时候用`java.io`？
对于网络编程，首选`java.nio`，对于文件读写，都可以。


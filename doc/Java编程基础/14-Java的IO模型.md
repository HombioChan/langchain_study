## 序言
`I/O`模型一般用于网络编程，所以`I/O模型`的全称是`网络I/O模型`，常用于指导服务端程序开发。

在`Java`中，常被提起的 `I/O` 模型有三种
1. 阻塞I/O
2. 非阻塞I/O
3. 异步I/O

下面依次使用这三个模型来实现一个echo服务器。

### 阻塞I/O
简称`BIO`，使用`阻塞模式`来实现服务器, `java.io`库和 `java.nio`库都可以实现`BIO`。

#### `java.io`
```java
public class OldBIO {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket();
        serverSocket.bind(new InetSocketAddress("127.0.0.1", 8080));
        while (true) {
            //线程阻塞，直到有客户端发起连接
            Socket client = serverSocket.accept();
            new Thread(()-> {
                handleConnect(client);
            }).start();
        }
    }

    private static void handleConnect(Socket client) {
        try {
            InputStream inputStream = client.getInputStream();
            OutputStream outputStream = client.getOutputStream();
            byte[] buffer = new byte[1024];
            int len = -1;
            // 如果OS内核读缓存为空，那么 read() 会阻塞当前线程
            while ((len = inputStream.read(buffer)) != -1) {
                // 如果OS内核缓存已经满，那么 write() 会阻塞当前线程
                outputStream.write(buffer, 0, len);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### `java.nio`
```java
public class NewBIO {
    public static void main(String[] args) throws IOException {
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
        serverSocketChannel.configureBlocking(true);
        while (true) {
            // 当前线程阻塞，直到有客户端发起连接
            SocketChannel client = serverSocketChannel.accept();
            new Thread(() -> {
                handleConnect(client);
            }).start();
        }
    }

    private static void handleConnect(SocketChannel client) {
        try {
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            while (client.read(buffer) != -1) {
                buffer.flip();
                while (buffer.hasRemaining()) {
                    client.write(buffer);
                }
                buffer.clear();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

#### BIO 的优点和缺点

- 优点：编程简单
- 缺点：每个客户端连接都需要分配一个线程处理，当连接非常多时，会创建大量的线程，系统资源占用大，线程上下文切换比较频繁。

### 非阻塞IO
简称`NIO`，即使用`非阻塞模式`来实现服务器，对于系统调用`read() write() accept()`，如果不可读/不可写/无连接请求，直接返回失败，不会阻塞当前线程。

`NIO` 只能通过 `java.nio`库来实现。

```java
public class NewNio {

    public static void main(String[] args) throws IOException, InterruptedException {
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
        serverSocketChannel.configureBlocking(false);
        while (true) {
            //如果没有连接请求，直接放回null
            SocketChannel client = serverSocketChannel.accept();
            // 控制每1s轮询一次
            if (client == null) {
                TimeUnit.SECONDS.sleep(1);
                continue;
            }
            new Thread(() -> {
                handleConnect(client);
            }).start();
        }
    }

    private static void handleConnect(SocketChannel client) {
        try {
            //配置非阻塞
            client.configureBlocking(false);
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            while (true) {
                // 如果OS内核读缓存为空，直接返回0，不会阻塞当前线程
                int len = client.read(buffer);
                // 控制每1s轮询一次
                if (len == 0) {
                    TimeUnit.SECONDS.sleep(1);
                    continue;
                }
                buffer.flip();
                while (buffer.hasRemaining()) {
                    // 如果OS内核写缓存已经满，直接返回0，不会阻塞当前线程
                    // 所以如果返回0，重复写，知道成功为止
                    while (client.write(buffer) == 0) {}
                }
                buffer.clear();
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```
#### 与 BIO 的比较
相比BIO，唯一的改变就是由阻塞模式改成非阻塞模式的，线程虽然没被阻塞，但是一直在轮询，不能去做其他事情，所以性能上没什么提高。

所以NIO一般和Selector一起使用，利用多路复用机制，再搭配上线程池，可以提高服务器并发连接的数量和服务可伸缩性。

```java
public class NewNio {

    //根据硬件条件控制线程池大小，提高程序可伸缩性
    private static final ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors()+1);

    public static void main(String[] args) throws IOException, InterruptedException {
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        serverSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
        serverSocketChannel.configureBlocking(false);

        Selector selector = Selector.open();
        serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);

        while (true) {
            //控制一下速度，每1s轮询一次
            int count = selector.select(1000);
            if (count == 0) {
                continue;
            }
            Set<SelectionKey> selectionKeys = selector.selectedKeys();
            Iterator<SelectionKey> iterator = selectionKeys.iterator();
            while (iterator.hasNext()) {
                SelectionKey key = iterator.next();
                if (key.isAcceptable()) {
                    SocketChannel client = serverSocketChannel.accept();
                    client.configureBlocking(false);
                    client.register(selector, SelectionKey.OP_READ, client);
                } else if (key.isReadable()) {
                    SocketChannel client = (SocketChannel)key.attachment();
                    executor.submit(new ReadTask(client));
                }
                iterator.remove();
            }
        }
    }

    private static class ReadTask implements Runnable {

        private SocketChannel socketChannel;

        public ReadTask(SocketChannel socketChannel) {
            this.socketChannel = socketChannel;
        }

        @Override
        public void run() {
            try {
                ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
                int read = socketChannel.read(byteBuffer);
                if (read != 0) {
                    byteBuffer.flip();
                    socketChannel.write(byteBuffer);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

}
```

#### 使用 Selector 的 NIO 优势

1. 多路复用，由一个线程负责轮询注册到`Selector`的所有网络I/O事件，相对于BIO一个连接一个线程的模式，大大降低了系统资源占用。
2. 后续的 读取、处理、写入任务，可以引入线程池处理，一方面，线程池可以提高系统的可伸缩性；另一方面， 必要时才从线程池拿线程执行任务，也提高了线程的工作效率。

### 异步I/O
简称`AIO`，不管是`BIO`还是`NIO`，都需要调用方主动去获取I/O消息，这为**同步**模式；对于异步I/O，线程在调用I/O接口时会注册一个`handler`，然后就可以去干其他事情，当发生相应的事件时，由被调用方执行事先注册好的`handler`。

和`NIO`一样，`AIO`只能使用`java.nio`库实现。 

```java
public class AIO {
    
    public static void main(String[] args) throws IOException, InterruptedException {
        CountDownLatch countDownLatch = new CountDownLatch(1);
        AsynchronousServerSocketChannel asynchronousServerSocketChannel = AsynchronousServerSocketChannel.open();
        asynchronousServerSocketChannel.bind(new InetSocketAddress("127.0.0.1", 8080));
        asynchronousServerSocketChannel.accept(null, new AcceptCompletionHandler(asynchronousServerSocketChannel));
        countDownLatch.await();;
    }

    public static class AcceptCompletionHandler implements CompletionHandler<AsynchronousSocketChannel, Object> {

        private AsynchronousServerSocketChannel serverSocketChannel;

        public AcceptCompletionHandler(AsynchronousServerSocketChannel serverSocketChannel) {
            this.serverSocketChannel = serverSocketChannel;
        }

        @Override
        public void completed(AsynchronousSocketChannel client, Object attachment) {
            //handler已经被消耗，需要重新注册，以便接受其他连接
            serverSocketChannel.accept(attachment, this);
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            client.read(buffer, buffer, new ReadCompletionHandler(client));
        }

        @Override
        public void failed(Throwable exc, Object attachment) {
            System.out.println("接受失败");
        }
    }

    private static class ReadCompletionHandler implements CompletionHandler<Integer, ByteBuffer> {
        private AsynchronousSocketChannel client;

        public ReadCompletionHandler(AsynchronousSocketChannel client) {
            this.client = client;
        }

        @Override
        public void completed(Integer result, ByteBuffer buffer) {
            buffer.flip();
            client.write(buffer, null, new WriteCompletionHandler());
            buffer.clear();
            //与accept一样，重新注册读监听器
            client.read(buffer, buffer, this);
        }

        @Override
        public void failed(Throwable exc, ByteBuffer attachment) {
            System.out.println("读失败");
        }
    }

    public static class WriteCompletionHandler implements CompletionHandler<Integer, Object> {
        @Override
        public void completed(Integer result, Object attachment) {

        }

        @Override
        public void failed(Throwable exc, Object attachment) {

        }
    }

}
```

## 总结
实际上，不同的操作系统有不同的 I/O 模型，Java作为一种跨平台语言，为了屏蔽各个操作系统 I/O 模型的差异，设计了3中新的 I/O 模型：`BIO NIO AIO`，并提供了类库来支持这3种 I/O 模型的实现。
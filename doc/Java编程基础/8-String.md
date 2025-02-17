### 原理
在 `JDK8` 中，底层使用 `char[]` 数组来记录使用 `UTF16` 编码 的 `Unicdoe` 字符。

### 常量池技术
String常量池技术即缓存使用过的字符串，以供后续复用，起到节省内存的作用。

#### 如何触发常量池机制

1. 使用字符串常量赋值

```
String str1 = "abc";
String str2 = "abc";
System.out.println(str1 == str2); //输出：true
```

2. 使用`intern`方法

`intern`会到字符串常量池中查找该字符串，如果存在，直接返回引用，如何不存在，将字符串加入常量池并返回引用。
```
String str1 = "abc";
String str2 = new String("abc");
String str3 = str2.intern();
System.out.println(str1 == str2); //输出：false
System.out.println(str1 == str3); //输出：true
```

#### 什么时候可以利用常量池机制
当相同的字符串常量频繁出现时，可以使用常量池技术。

### 压缩技术
在`JDK8`中，`String`底层使用`char[]`数组存储`Unicode`字符，如果项目中频繁使用的字符都是`ASCII`字符，实际上只需要一个字节存储即可，使用2个字节会造成一半的内存消耗，所以在`JDK9`中，对`String`实现进行了优化，使用`byte[]`数组替代了`char[]`数组。

原理如下：
- 当字符串中都是`ASCII`字符，使用1个字节保存编码
- 否则，还是使用2个字节保存编码

### 不可变性
`String`类被设计为一个不可变类，主要原因有以下3点

1. 使用了常量池技术
2. 固定hash值，有利于使用`HashMap`
3. `String`贴近基本类型，延续 `Interger、Long` 的设计风格

#### 如何应对字符串可变的需求
使用 `StringBuidler` 或者 `StringBuffer`。

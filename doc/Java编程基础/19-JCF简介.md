## 序言
`JCF`全称`Java Collection Framework`，翻译为 Java 集合框架。

本节主要对 `JCF` 进行一个分类并按照分类进行简单介绍，让你对`JCF`有一个全局的了解。

### 分类
从数据结构的角度上看，可以将`JCF`划分为4类
1. List（线性表）: `LinkedList、ArrayList、Vector`
2. Stack（栈）：`Stack LinkedList ArrayDeque`
3. Queue（队列）：`ArrayDeque、LinkedList、PriorityQueue`
4. Map（哈希表）: `HashMap、LinkedHashMap、TreeMap、HashTable`

`Set`是组合`Map`实现的，可以理解为`value`为`null`的`Map`，对应的实现有`HashSet、LinkedHashSet、TreeSet`，搞懂了`Map`就搞懂了`Set`，所以就不划入这个分类中。

> JCF 容器除了 `Vector、Stack、Hashtable`，都是线程不安全的。

### List
#### LinkedList
一个基于双向链表实现的线性表。

```
List<String> list = new LinkedList<>();
list.add("abc");
list.add("edf");
System.out.println(list.get(1));
```

#### ArrayList
一个基于数组实现的线性表。

```
List<String> list = new ArrayList<>();
list.add("abc");
list.add("edf");
System.out.println(list.get(1));
```

#### Vector
是`JDK 1.0`的容器类，线程安全的，现在已经不推荐使用，可以使用 `LinkedList` 和 `ArrayList`替代。

#### LinkedList VS ArrayList 
就是 [数组和链表的比较](../hblog/数据结构和算法/4-数组和链表的比较.md)

### Stack
与 `Vector` 一样是`JDK 1.0`的容器类，现在已经不推荐使用，可以使用`LinkedList`或者`ArrayDeque`替代。前者是基于链表的实现，后者是基于数组的实现。

```
Deque<Integer> stack1 = new LinkedList<>();
stack1.push(1);
stack1.push(2);
stack1.push(3);
while (!stack1.isEmpty()) {
    System.out.println(stack1.poll()); // 输出 3 2 1
}

Deque<Integer> stack2 = new ArrayDeque<>();
stack2.push(1);
stack2.push(2);
stack2.push(3);
while (!stack2.isEmpty()) {
    System.out.println(stack2.poll()); // 输出 3 2 1
}
```

### Queue
#### LinkedList
一个基于双向链表实现的队列。
```
Queue<Integer> queue = new LinkedList<>();
queue.offer(1);
queue.offer(2);
queue.offer(3);
while (!queue.isEmpty()) {
    System.out.println(queue.pop()); // 输出：1 2 3
}
```

#### ArrayDeque
一个基于数组实现的队列。
```
Queue<Integer> queue = new ArrayDeque<>();
queue.offer(1);
queue.offer(2);
queue.offer(3);
while (!queue.isEmpty()) {
    System.out.println(queue.pop()); // 输出：1 2 3
}
```

#### PriorityQueue
一个基于堆实现的队列，顾名思义，优先级队列，规则不再是向普通队列那样先进先出，而是优先级高的先出队列，使用时需要传入比较函数，用于优先级排序。

```
//默认小顶堆，通过比较函数改成大顶堆
PriorityQueue<Integer> priorityQueue = new PriorityQueue<>((o1,o2) -> o2 - o1);
priorityQueue.offer(3);
priorityQueue.offer(1);
priorityQueue.offer(2);
while (!priorityQueue.isEmpty()) {
    System.out.println(priorityQueue.poll()); // 输出：3 2 1
}
```


### Map
#### HashMap
就是最基本的哈希表实现，基于数组、链表、红黑树实现。
```

Map<String, String> map = new HashMap<>();
//支持key=null
map.put(null, "null");
map.put("hello", "world");
System.out.println(map.get(null)); // 输出：null
System.out.println(map.get("hello")); // 输出：world
```

#### LinkedHashMap
在 `HashMap` 的基础上，再引入一个双向链表，从而支持按插入顺序、访问顺序有序访问。

默认情况下按插入顺序访问
```
LinkedHashMap<String, String> linkedHashMap = new LinkedHashMap<>();
linkedHashMap.put("a", "aaa");
linkedHashMap.put("b", "bbb");
linkedHashMap.put("c", "ccc");
// 输出：a=aaa b=bbb c=ccc
linkedHashMap.forEach((k,v)-> System.out.printf("%s=%s\n", k,v));
linkedHashMap.get("a");
// 输出：a=aaa b=bbb c=ccc
linkedHashMap.forEach((k,v)-> System.out.printf("%s=%s\n", k,v));
// 输出：a=aaa b=bbb c=ccc
linkedHashMap.get("b");
linkedHashMap.forEach((k,v)-> System.out.printf("%s=%s\n", k,v));
```

按照访问顺序访问
```
LinkedHashMap<String, String> linkedHashMap = new LinkedHashMap<>(16, 0.75f, true);
linkedHashMap.put("a", "aaa");
linkedHashMap.put("b", "bbb");
linkedHashMap.put("c", "ccc");

// 输出：a=aaa b=bbb c=ccc
linkedHashMap.forEach((k,v)-> System.out.printf("%s=%s\n", k,v));
linkedHashMap.get("a");
// 输出：b=bbb c=ccc a=aaa 
linkedHashMap.forEach((k,v)-> System.out.printf("%s=%s\n", k,v));
linkedHashMap.get("b");
// 输出：c=ccc a=aaa b=bbb 
linkedHashMap.forEach((k,v)-> System.out.printf("%s=%s\n", k,v));
```


#### TreeMap
基于红黑树实现的一个**key值有序**的哈希表，不同于上面两种`Map`实现，`TreeMap`直接实现的是`SortedMap`接口，相对于`Map`接口，提供了更丰富的接口。

> 在红黑树中，key为比较数据，value为卫星数据

```
SortedMap<String,String> treeMap = new TreeMap<>();
treeMap.put("a", "aaa");
treeMap.put("c", "ccc");
treeMap.put("b", "bbb");
//按序输出：a=aaa b=bbb c=ccc
treeMap.forEach((k,v) -> System.out.printf("%s=%s\n", k, v));
//输出：a
System.out.println(treeMap.firstKey());
//输出：c
System.out.println(treeMap.lastKey());
//获取子Map，不包括当前指定键值对
SortedMap<String, String> headMap = treeMap.headMap("b");
//获取子Map，包括当前指定键值对
SortedMap<String, String> tailMap = treeMap.tailMap("b");
//输出：a=aaa
headMap.forEach((k,v) -> System.out.printf("%s=%s\n", k, v));
//输出：b=bbb c=ccc
tailMap.forEach((k,v) -> System.out.printf("%s=%s\n", k, v));
```
#### Hashtable
`jdk 1.0`的容器类，现在不推荐使用，可以使用`HashMap`或者`LinkedHashMap`替代。
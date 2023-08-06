## 背景

就 protobuf 而言是一个语言无关的负载描述语言，由于其是面向二进制的所以相比 json 这样的自描述的格式来讲在性能上要好一些。 现在要解决的问题是在底层通信协议是 tcp、 websocket 的时候代码要怎么写的问题。


需求：实现一个序列号发生器

---

## 服务端
```bash
sequence-server run 

2022-01-20 23:51:47,683 - root - MainThread - INFO - 50 - sequence-server start listen on 127.0.0.1:10352 .
2022-01-20 23:51:47,690 - root - MainThread - INFO - 55 - seqense-server started .
2022-01-20 23:52:14,834 - root - ThreadPoolExecutor-0_0 - INFO - 34 - revice request from ipv4:127.0.0.1:56801 offset = 0 .
2022-01-20 23:52:14,834 - root - ThreadPoolExecutor-0_0 - INFO - 35 - current = 0 .
```

---

## 客户端
```bash
sequence-client
1

sequence-client
2
```

---

## 编译安装
```bash
python3 setup.py sdist

pip3 install dist/seqence-server-demo-0.0.1.tar.gz
```

---
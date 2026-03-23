#!/bin/bash
cd "/Users/james/00Tool/Prompt MS"
# 启动应用
"./start.sh" &

# 等待应用启动
sleep 2

# 打开浏览器
open http://localhost:8080
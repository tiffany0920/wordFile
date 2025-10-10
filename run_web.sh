#!/bin/bash
echo "启动智能文档生成器 Web 界面..."
echo ""
echo "请确保已安装依赖: pip install -r requirements.txt"
echo "请确保已配置环境变量: 复制 .env.example 为 .env 并填入API密钥"
echo ""
read -p "按回车键继续..."
streamlit run web_app.py

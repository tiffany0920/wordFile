@echo off
setlocal
echo 启动智能文档生成器 Web 界面...
echo.
echo 请确保已安装依赖: pip install -r requirements.txt
echo 请确保已配置环境变量: 复制 .env.example 为 .env 并填入API密钥
echo.

REM 在当前目录运行，固定端口 8501，并关闭 CORS/基本检查以避免端口占用问题提示
cd /d %~dp0

REM 关闭首次运行收集信息提示，绑定到本机，固定端口
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
set STREAMLIT_SERVER_PORT=8501
set STREAMLIT_SERVER_ADDRESS=localhost

REM 如果需要代理或自定义端口，请在下行添加参数
streamlit run web_app.py --server.port 8501 --server.address localhost --server.headless true

if errorlevel 1 (
  echo.
  echo 启动失败，请检查上面的错误日志。
  echo 常见问题：
  echo 1) 端口被占用：请修改端口参数为 --server.port 8502 等
  echo 2) 依赖未安装：pip install -r requirements.txt
  echo 3) 环境变量未设置：检查 .env 中的 DASHSCOPE_API_KEY
  pause
)

endlocal

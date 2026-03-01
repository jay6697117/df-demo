import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """    /* 【史诗级大重构】：在手机端将 <table> 断开，化身为直观的多行卡片列表 */
    table, thead, tbody, th, td, tr { 
      display: block; 
    }"""
    
new_css = """    /* 【史诗级大重构】：在手机端将 <table> 断开，化身为直观的多行卡片列表 */
    table, thead, tbody, th, td, tr { 
      display: block !important; 
      width: 100% !important;
    }
    
    /* 强行取消表格的 overflow-x 滚动特性 */
    .table-box {
      overflow-x: hidden !important;
      border: none !important;
    }
    table {
      border-collapse: separate !important;
      border-spacing: 0 !important;
    }"""

content = content.replace(old_css, new_css)


old_css2 = """    /* 每一行 TR 变成一个带阴影和圆角的卡片 */
    tr {
      background: #ffffff !important;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      margin-bottom: 16px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05);
      padding: 12px;
    }"""

new_css2 = """    /* 每一行 TR 变成一个带阴影和圆角的卡片 */
    tr {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 12px !important;
      margin-bottom: 16px !important;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
      padding: 12px !important;
      display: block !important;
      width: 100% !important;
    }"""

content = content.replace(old_css2, new_css2)


old_css3 = """    /* TD 变成卡片里的每一行小属性 */
    td { 
      border: none;
      border-bottom: 1px solid #f1f5f9; 
      position: relative;
      padding: 10px 0 10px 40%; 
      text-align: right;
      min-height: 48px;
    }"""

new_css3 = """    /* TD 变成卡片里的每一行小属性 */
    td { 
      border: none !important;
      border-bottom: 1px solid #f1f5f9 !important; 
      position: relative !important;
      padding: 10px 0 10px 40% !important; 
      text-align: right !important;
      min-height: 48px !important;
      display: flex !important;
      justify-content: flex-end;
      align-items: center;
      white-space: normal !important; /* 允许换行，覆盖之前 pc 端的 nowrap */
    }"""

content = content.replace(old_css3, new_css3)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Repair completed.")

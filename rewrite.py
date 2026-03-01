import re

with open('2026年全国门店开发进度追踪总表_3.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .module styles
module_old = """.module{
    border-radius:12px;
    border:1px solid #dee2e6;
    padding:20px;
    margin-bottom:20px;
    -webkit-border-radius:12px;
    -moz-border-radius:12px;
  }"""
module_new = """.module{
    border-radius:16px;
    border:1px solid #edf2f7;
    background:#ffffff;
    box-shadow:0 4px 12px rgba(0,0,0,0.03);
    padding:20px;
    margin-bottom:20px;
    transition:box-shadow 0.3s ease;
    -webkit-border-radius:16px;
    -moz-border-radius:16px;
  }
  .module:hover{
    box-shadow:0 6px 16px rgba(0,0,0,0.08);
  }"""
content = content.replace(module_old, module_new)

# 2. Update table styles
table_old = """.table-box{
    overflow-x:auto;
    border-radius:10px;
    border:1px solid #eee;
    -webkit-border-radius:10px;
    -moz-border-radius:10px;
  }
  table{
    width:100%;
    border-collapse:collapse;
    font-size:14px;
    table-layout:fixed; /* 固定表格布局，避免列宽错乱 */
  }
  th{
    background:#007bff;
    color:white;
    padding:12px 8px;
    position:sticky;
    top:0;
    -webkit-position:sticky; /* 兼容Safari */
    z-index:10; /* 确保表头在滚动时置顶 */
  }
  td{
    padding:10px 8px;
    text-align:center;
    border-bottom:1px solid #eee;
    min-width:80px;
    vertical-align:middle;
    word-wrap:break-word; /* 自动换行，避免内容溢出 */
    word-break:break-all;
  }"""

table_new = """.table-box{
    overflow-x:auto;
    border-radius:12px;
    border:1px solid #edf2f7;
    -webkit-border-radius:12px;
    -moz-border-radius:12px;
  }
  /* 滚动条美化 */
  .table-box::-webkit-scrollbar {
    height: 10px;
    width: 10px;
  }
  .table-box::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 5px;
  }
  .table-box::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 5px;
  }
  .table-box::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
  table{
    width:100%;
    border-collapse:collapse;
    font-size:14px;
    /* 移除 table-layout: fixed，让表格根据内容自然伸展，解决列过多挤压的问题 */
  }
  th{
    background:#f8fafc; /* 高级浅灰底色 */
    color:#334155;      /* 深灰字体 */
    font-weight:600;
    padding:14px 10px;
    position:sticky;
    top:0;
    -webkit-position:sticky;
    z-index:10;
    white-space:nowrap; /* 表头不换行 */
    border-bottom: 2px solid #e2e8f0;
  }
  td{
    padding:12px 10px;
    text-align:center;
    border-bottom:1px solid #f1f5f9;
    min-width:80px;
    vertical-align:middle;
    white-space:nowrap; /* 不换行，靠横向滚动查看 */
  }
  /* 隔行变色 */
  tbody tr:nth-child(even) {
    background-color: #fafbfc;
  }
  tbody tr:hover {
    background-color: #f1f5f9;
  }
  
  /* 针对核心大表格的固定列支持 */
  .main-table th:nth-child(1), .main-table td:nth-child(1){
    position: sticky; left: 0; z-index: 11; background: inherit;
    box-shadow: 2px 0 5px rgba(0,0,0,0.02);
  }
  .main-table th:nth-child(2), .main-table td:nth-child(2){
    position: sticky; left: 50px; z-index: 11; background: inherit;
    box-shadow: 2px 0 5px rgba(0,0,0,0.02);
  }
  .main-table th:nth-child(3), .main-table td:nth-child(3){
    position: sticky; left: 200px; z-index: 11; background: inherit;
    box-shadow: 2px 0 5px rgba(0,0,0,0.02);
  }
  /* 为表头叠加 z-index 保证在固定列滚动时也在最上方 */
  .main-table th:nth-child(1), .main-table th:nth-child(2), .main-table th:nth-child(3){
    z-index: 12;
    background: #f8fafc;
  }"""
content = content.replace(table_old, table_new)

# 3. Add class="main-table" to the core table
table_html_old = """      <table>
        <thead>
          <tr>
            <th>选择</th><th>门店名称</th><th>区域</th>"""
table_html_new = """      <table class="main-table">
        <thead>
          <tr>
            <th style="min-width: 50px;">选择</th><th style="min-width: 150px;">门店名称</th><th style="min-width: 100px;">区域</th>"""
content = content.replace(table_html_old, table_html_new)

# 4. Update button styles
btn_old = """  button{
    padding:10px 14px;
    border:none;
    border-radius:8px;
    background:#007bff;
    color:white;
    cursor:pointer;
    transition:opacity 0.2s;
    font-size:14px;
    -webkit-border-radius:8px;
    -moz-border-radius:8px;
    -webkit-transition:opacity 0.2s;
  }
  button:hover{
    opacity:0.9;
  }
  .btn-red{background:#dc3545;}
  .btn-green{background:#28a745;}
  .btn-blue{background:#17a2b8;}
  .btn-purple{background:#6f42c1;}"""

btn_new = """  button{
    padding:10px 16px;
    border:none;
    border-radius:8px;
    background:#3b82f6;
    color:white;
    cursor:pointer;
    transition:all 0.2s ease;
    font-size:14px;
    font-weight:500;
    -webkit-border-radius:8px;
    -moz-border-radius:8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  button:hover{
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    filter: brightness(1.05);
  }
  button:active{
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .btn-red{background:#ef4444;}
  .btn-green{background:#10b981;}
  .btn-blue{background:#0ea5e9;}
  .btn-purple{background:#8b5cf6;}"""
content = content.replace(btn_old, btn_new)

# 5. Fix card styles
card_old = """  .card{
    padding:18px;
    border-radius:12px;
    border-left:4px solid #9ca3af;
    background:#fafafa;
    -webkit-border-radius:12px;
    -moz-border-radius:12px;
    /* grid兼容：每个card占25%宽度 */
    -webkit-box-flex:1;
    -ms-flex:1 0 22%;
    flex:1 0 22%;
    margin:0 5px 10px;
  }"""
card_new = """  .card{
    padding:20px;
    border-radius:12px;
    border-left:4px solid #9ca3af;
    background:#ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    -webkit-border-radius:12px;
    -moz-border-radius:12px;
    /* grid兼容：每个card占25%宽度 */
    -webkit-box-flex:1;
    -ms-flex:1 0 22%;
    flex:1 0 22%;
    margin:0 5px 10px;
  }
  .card:hover{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
  }"""
content = content.replace(card_old, card_new)

# 6. Global scrollbar (for body)
body_old = """  body{
    background:#f5f7fa;
    padding:20px;
    margin:0;
    -webkit-font-smoothing:antialiased; /* 抗锯齿，让字体更清晰 */
    -moz-osx-font-smoothing:grayscale;
  }"""
body_new = """  /* 全局滚动条美化 */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
  body{
    background:#f8fafc;
    padding:20px;
    margin:0;
    color: #334155;
    -webkit-font-smoothing:antialiased; /* 抗锯齿，让字体更清晰 */
    -moz-osx-font-smoothing:grayscale;
  }"""
content = content.replace(body_old, body_new)

with open('2026年全国门店开发进度追踪总表_3.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Rewrite script completed.")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix grid display order in the 3 occurrences
def fix_grid_order(match):
    original = match.group(0)
    # Move `display: grid;` to immediately after the fallback rules
    fallback = "    display:-webkit-box;\n    display:-ms-flexbox;"
    if fallback in original:
        clean = original.replace("    display:grid;\n", "").replace(fallback, fallback + "\n    display:grid;")
        return clean
    return original

text = re.sub(r'    display:grid;[\s\S]+?display:-ms-flexbox;', fix_grid_order, text)

# 2. Fix the flex properties to have grid max-width override so they behave properly locally
text = text.replace(
    "-ms-flex:1 0 18%;\n    flex:1 0 18%;",
    "-ms-flex:1 0 18%;\n    flex:1 0 18%;\n    /* Fallback width logic for grid items if grid isn't applied correctly */"
)

# Actually, the best way to prevent the grid problem is to just reset the flex basis to auto inside the media queries!
media_query_fix = """.year-stat-item, .month-stat-card, .card {
      -webkit-box-flex: auto !important;
      -ms-flex: auto !important;
      flex: auto !important;
      max-width: none !important;
    }"""
# Wait, let's insert it inside the mobile media queries
text = text.replace(
    "@media (max-width: 1024px) {",
    "@media (max-width: 1024px) {\n    " + media_query_fix
)

# 3. For the horizontal scrollbar issue: Remove width: 100% !important; from td.
old_responsive_table = """    /* 【史诗级大重构】：在手机端将 <table> 断开，化身为直观的多行卡片列表 */
    table, thead, tbody, th, td, tr { 
      display: block !important; 
      width: 100% !important;
    }"""
new_responsive_table = """    /* 【史诗级大重构】：在手机端将 <table> 断开，化身为直观的多行卡片列表 */
    table, thead, tbody, th, td, tr { 
      display: block !important; 
    }
    table { width: 100% !important; box-sizing: border-box; }
    """
text = text.replace(old_responsive_table, new_responsive_table)

old_tr = """    /* 每一行 TR 变成一个带阴影和圆角的卡片 */
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
new_tr = """    /* 每一行 TR 变成一个带阴影和圆角的卡片 */
    tr {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 12px !important;
      margin-bottom: 16px !important;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
      padding: 12px !important;
      display: block !important;
      box-sizing: border-box;
    }"""
text = text.replace(old_tr, new_tr)

old_td = """    /* TD 变成卡片里的每一行小属性 */
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
new_td = """    /* TD 变成卡片里的每一行小属性 */
    td { 
      border: none !important;
      border-bottom: 1px solid #f1f5f9 !important; 
      position: relative !important;
      padding: 10px 0 10px 38% !important; 
      text-align: right !important;
      min-height: 48px !important;
      display: flex !important;
      justify-content: flex-end;
      align-items: center;
      white-space: normal !important;
      box-sizing: border-box;
      width: auto !important;
    }"""
text = text.replace(old_td, new_td)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("CSS Fix Applied.")

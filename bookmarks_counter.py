from bs4 import BeautifulSoup

def count_bookmarks(html_file):
    """计算HTML书签文件中的书签总数。"""
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        bookmarks = soup.find_all('a')
        return len(bookmarks)
    except FileNotFoundError:
        print(f"文件 {html_file} 未找到。")
        return 0
    except Exception as e:
        print(f"处理文件时发生错误: {e}")
        return 0

# 替换下面的路径为您的HTML书签文件路径
html_file_path = 'bookmarks.html'
total_bookmarks = count_bookmarks(html_file_path)
print(f"书签总数: {total_bookmarks}")


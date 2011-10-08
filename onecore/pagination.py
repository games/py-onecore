# coding=utf-8

def build_pagination(currPage, totalRows, url_builder, perPageSize = 10):
    pagination = ['<div class="__pagination__">']
    totalPage = totalRows / perPageSize if totalRows % perPageSize == 0 else totalRows / perPageSize + 1
    left_count, right_count = 3, 3
    
    start_page, end_page = 2, totalPage - 1
    
    if currPage > 1:
        pagination.append(__build_element(currPage, currPage - 1, u'上一页', url_builder))
    
    pagination.append(__build_element(currPage, 1, '1', url_builder))
    
    if currPage > 2 + left_count and totalPage > 2 + left_count:
        pagination.append('<span>...</span>')
        start_page = currPage - left_count
    
    if currPage + right_count < totalPage:
        end_page = currPage + right_count

    for i in range(start_page, end_page + 1):
        pagination.append(__build_element(currPage, i, str(i), url_builder))
    
    if currPage + right_count < totalPage - 1:
        pagination.append('<span>...</span>')
        
    if totalPage > 1:
        pagination.append(__build_element(currPage, totalPage, str(totalPage), url_builder))
        
    if currPage < totalPage:
        pagination.append(__build_element(currPage, currPage + 1, u'下一页', url_builder))
        
    pagination.append('</div>')
    return ''.join(pagination)

def __build_element(curr, page, name, url_builder):
    if page == curr:
        element = '<span class="curr">' + name + '</span>'
    else:
        element = '<a href="' + url_builder(page) + '">' + name + '</a>'
    return element

if __name__ == '__main__':
    
    def url_builder(page):
        return '/page=%d' % page
    
    print build_pagination(5, 20, url_builder)
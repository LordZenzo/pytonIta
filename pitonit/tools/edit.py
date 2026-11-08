def sub(path, old, new, count=1):
    s = open(path, encoding='utf-8', newline='').read()
    crlf = '\r\n' in s
    if crlf:
        old = old.replace('\r\n', '\n').replace('\n', '\r\n')
        new = new.replace('\r\n', '\n').replace('\n', '\r\n')
    assert old in s, (path, old[:60])
    s = s.replace(old, new, count)
    open(path, 'w', encoding='utf-8', newline='').write(s)

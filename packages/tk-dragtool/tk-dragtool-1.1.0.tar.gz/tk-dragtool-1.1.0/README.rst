NAME
    tk_dragtool

DESCRIPTION
    �ṩ������϶�������tkinter�ؼ����ߵ�ģ�顣
    A module which supplies tools to drag and resize
    tkinter window and widgets with the mouse.

FUNCTIONS
    bind_drag(tkwidget, dragger)
        ����ҷ�¼���
        tkwidget: ���϶��Ŀؼ��򴰿�,
        dragger: ��������¼��Ŀؼ�,
        ����bind_drag��,�������dragger���϶�ʱ, tkwidget�ᱻ�϶�, ��dragger
        ��Ϊ��������¼��Ŀؼ�, λ�ò���ı䡣

    bind_resize(tkwidget, dragger, anchor, min_w=0, min_h=0, move_dragger=True)
        �������¼���
        anchor: ���ŵķ�λ, ȡֵΪN,S,W,E,NW,NE,SW,SE,�ֱ��ʾ���������ϡ�����
        min_w,min_h: �÷���tkwidget���ŵ���С���(��߶�)��
        move_dragger: ����ʱ�Ƿ��ƶ�dragger��
        ����˵��ͬbind_drag������

    draggable(tkwidget)
        ����draggable(tkwidget) ʹtkwidget���϶���
        tkwidget: һ���ؼ�(Widget)��һ������(Wm)��

    getpos()
        ��ȡ��굱ǰλ�á�

    move(widget, x=None, y=None, width=None, height=None)
        �ƶ��ؼ��򴰿�widget, �����Կ�ѡ��

Ч��ͼ:

.. image:: https://tiebapic.baidu.com/forum/pic/item/3b87e950352ac65c87c2d7a2bef2b21192138a18.jpg
    :alt: Ч��ͼ

����:``�߷ֳ��� qq:3076711200 �ٶ��˺�:�쵤34``
������ҳ: <https://blog.csdn.net/qfcy\_/>`_
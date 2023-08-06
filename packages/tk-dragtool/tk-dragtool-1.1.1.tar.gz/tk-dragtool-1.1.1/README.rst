NAME
    tk_dragtool

DESCRIPTION
    提供用鼠标拖动、缩放tkinter控件工具的模块。
    A module which supplies tools to drag and resize
    tkinter window and widgets with the mouse.

FUNCTIONS
    bind_drag(tkwidget, dragger)
        绑定拖曳事件。
        tkwidget: 被拖动的控件或窗口,
        dragger: 接收鼠标事件的控件,
        调用bind_drag后,当鼠标在dragger上拖动时, tkwidget会被拖动, 但dragger
        作为接收鼠标事件的控件, 位置不会改变。

    bind_resize(tkwidget, dragger, anchor, min_w=0, min_h=0, move_dragger=True)
        绑定缩放事件。
        anchor: 缩放的方位, 取值为N,S,W,E,NW,NE,SW,SE,分别表示东、西、南、北。
        min_w,min_h: 该方向tkwidget缩放的最小宽度(或高度)。
        move_dragger: 缩放时是否移动dragger。
        其他说明同bind_drag函数。

    draggable(tkwidget)
        调用draggable(tkwidget) 使tkwidget可拖动。
        tkwidget: 一个控件(Widget)或一个窗口(Wm)。

    getpos()
        获取鼠标当前位置。

    move(widget, x=None, y=None, width=None, height=None)
        移动控件或窗口widget, 参数皆可选。

效果图:

.. image:: https://tiebapic.baidu.com/forum/pic/item/3b87e950352ac65c87c2d7a2bef2b21192138a18.jpg
    :alt: 效果图

作者:``七分诚意 qq:3076711200 百度账号:徐丹34``
作者主页: <https://blog.csdn.net/qfcy\_/>`_
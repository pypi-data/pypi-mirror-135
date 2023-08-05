import sys
from direct.showbase.ShowBase import ShowBase
from p3dit.editor import TextEditorNode


def main():
    base = ShowBase()
    base.win.set_clear_color((0.1,0.1,0.1,1))
    base.accept('control-q', sys.exit)
    base.text = render2d.attach_new_node(TextEditorNode("Editor"))
    base.text.set_scale(0.05)
    base.text.set_pos((-0.95,0,0.9))
    base.run()

if __name__ == '__main__':
    main()

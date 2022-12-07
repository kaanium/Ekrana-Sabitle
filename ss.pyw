import cv2
from numpy import array as ar
from pyautogui import screenshot, position
import win32gui
import win32com.client
import win32api
import win32con

sss = screenshot()
sss = cv2.cvtColor(ar(sss), cv2.COLOR_RGB2BGR)
cv2.imwrite("Adsiz.png", sss)
img = cv2.imread("Adsiz.png", 1)
point1 = (0, 0)
activate = False
prev_x = 0
prev_y = 0
coordinates = []
small = False
origin = []
switch = False
index = -1
liste = []


def click(event, x, y, _flags, _params):
    global activate, point1, sub_img, glo_img

    if event == cv2.EVENT_LBUTTONDOWN:
        activate = True
        point1 = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and activate:
        img_copy = img.copy()
        cv2.rectangle(img_copy, point1, (x, y), (0, 0, 255), 1)
        cv2.imshow("SS", img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        activate = False
        if y > point1[1]:
            sub_img = img[point1[1]:y, point1[0]:x]
        else:
            sub_img = img[y:point1[1], x:point1[0]]
        minimize = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(minimize, win32con.SW_MINIMIZE)
        cv2.namedWindow("a", cv2.WINDOW_AUTOSIZE)
        window_handle = win32gui.FindWindowEx(None, None, None, "a")

        current_style = win32gui.GetWindowLong(window_handle, -16)

        current_style = current_style & ~0x00C00000
        current_style = current_style & ~0x00080000
        current_style = current_style & ~0x00040000
        current_style = current_style & ~0x20000000
        current_style = current_style & ~0x00010000

        win32gui.SetWindowLong(window_handle, -16, current_style)
        current_style = win32gui.GetWindowLong(window_handle, -20)
        win32gui.SetWindowLong(window_handle, -20, current_style | 0x1)
        win32gui.SetWindowPos(window_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOSIZE | win32con.SWP_NOMOVE | win32con.SWP_FRAMECHANGED)
        cv2.imshow("a", sub_img)
        cv2.setMouseCallback("a", click2)
        glo_img = sub_img.copy()


def paint_draw(event, former_x, former_y, _flags, _param):
    global current_former_x, current_former_y, activate, glo_img, index, liste

    win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_UPARROW))
    if event == cv2.EVENT_LBUTTONDOWN:
        liste.append(glo_img.copy())
        index += 1
        activate = True
        current_former_x, current_former_y = former_x, former_y
    elif event == cv2.EVENT_MOUSEMOVE and activate:
        
        cv2.line(glo_img, (current_former_x, current_former_y), (former_x, former_y), (0, 0, 255), 2)
        current_former_x = former_x
        current_former_y = former_y
        cv2.imshow("a", glo_img)
    elif event == cv2.EVENT_LBUTTONUP:
        activate = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        glo_img = liste[index].copy()
        index -= 1
        liste.pop()
        cv2.imshow("a", glo_img)



def click2(event, _x, _y, _flags, _params):
    global activate, prev_x, prev_y, coordinates, small, origin
    if event == cv2.EVENT_LBUTTONDOWN:
        activate = True
        prev_x, prev_y = position()
        window_handle = win32gui.FindWindowEx(None, None, None, "a")
        coordinates = win32gui.GetWindowRect(window_handle)
    elif event == cv2.EVENT_MOUSEMOVE and activate:
        current_x, current_y = position()
        current_x -= prev_x
        current_y -= prev_y
        new_x = coordinates[0] + current_x
        new_y = coordinates[1] + current_y
        cv2.moveWindow("a", new_x, new_y)
    elif event == cv2.EVENT_LBUTTONUP:
        activate = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        if not small:
            window_handle = win32gui.FindWindowEx(None, None, None, "a")
            coordinates = win32gui.GetWindowRect(window_handle)
            origin = coordinates
            win32gui.MoveWindow(window_handle, coordinates[0], coordinates[1], 90, 90, True)
            small = True
        else:
            window_handle = win32gui.FindWindowEx(None, None, None, "a")
            coordinates = win32gui.GetWindowRect(window_handle)
            win32gui.MoveWindow(window_handle, coordinates[0], coordinates[1], origin[2] - origin[0],
                                origin[3] - origin[1], True)
            small = False


cv2.namedWindow("SS", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("SS", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("SS", click)

cv2.imshow("SS", img)

shell = win32com.client.Dispatch("WScript.Shell")
shell.SendKeys('%')

win32gui.SetForegroundWindow(win32gui.FindWindowEx(None, None, None, "SS"))

while 1:

    key = cv2.waitKey(0)
    if key == 27:
        break
    if key == 32:
        switch = not switch
        if switch:
            cv2.setMouseCallback("a", paint_draw)
        else:
            cv2.setMouseCallback("a", click2)

cv2.destroyAllWindows()
